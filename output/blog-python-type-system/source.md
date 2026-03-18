---
emoji: "🐍"
title: "Python<br>类型系统"
subtitle: "从无到有，写Agent够用"
description: "写了多年 C++ 和 Java，跳槽到 AI 公司开始用 Python 做 Agent 开发。接手同事的无类型代码后痛苦不堪，趁架构重构的机会调研了 Python 类型系统，设计了一套强类型机制。这是我在这个过程中的发现。"
---

## 为什么写这篇文章

我之前一直写 C++ 和 Java，跳槽到一家 AI 公司之后开始写 Python，负责 Agent 方向的开发。

刚上手的时候真的很痛苦。看同事之前写的代码，到处都是裸的 `dict`、没有类型标注的函数、传进来什么类型全靠猜。写了这么多年静态语言，习惯了编译器帮我兜底，突然到了一个什么都不可信的世界，每天都提心吊胆。

最近这个 Agent 架构要重构——原来的设计撑不住了，需要加更多灵活的功能。我是重构的负责人，趁这个机会好好调研了一遍 Python 的类型系统，自己设计了一套强类型、写起来又很舒服的机制。

这篇文章就是我在这个过程中的一些发现和感悟。

---

## 第一个问题：我看不懂任何一个函数

接手代码后最大的痛苦不是逻辑复杂，而是**不知道数据长什么样**。一个函数接收 `data`，返回 `result`——`data` 里有哪些 key？`result` 是 dict 还是 list？只能跑一遍才知道。

Python 3.5 加了类型标注，3.10 语法变得现代化（`list[int]`、`str | None`）。但关键是——**运行时完全忽略这些标注**：

```python
x: int = "hello"  # 不报错，正常运行！
```

类型标注本质上是**注释**。配合 Pyright 可以在 IDE 里做静态检查，但从外部进来的数据——API 请求、LLM 输出——标注管不了。

不过，至少我能看懂代码了。这是第一步。

---

## 第二个问题：到处都是 .get("key")

原来的项目其实能跑，LLM 调用也用了格式化输出。但数据在节点之间传来传去，全是 `dict`。到处都是 `result.get("title")`、`data["pages"][0].get("content", "")`——key 写错了不会报错，拿到 `None` 悄悄往下走，直到很远的地方才炸。

对写 C++ 出身的人来说，这种代码让我非常难受。**我想要的是：拿到一个对象，IDE 能告诉我它有什么字段，传错类型编辑器立刻标红。**

Pydantic 做的事情就是这个——读取你写的类型标注，在运行时生成对应的验证和转换逻辑：

```python
from pydantic import BaseModel

class StoryPage(BaseModel):
    title: str
    content: str
    scene: str = ""

page = StoryPage(**raw_dict)  # 自动校验+转换
page.title    # IDE 补全，类型确定
page.titl     # Pyright 立刻报错
```

更强大的是 `model_json_schema()`——自动把 Python 类型转成 JSON Schema，可以直接传给 LLM 的 `response_format` 约束输出格式。

把核心数据结构从 `dict` 换成 Pydantic 模型之后，体感完全不一样了——**写代码终于有了在 C++ 里的那种确定感。**

---

## 真正的突破：让每个 Capability 成为类型化的积木

我们的 Agent 是一个多步骤的工作流——Planner 生成执行计划，Coordinator 调度多个能力节点（写故事、渲染图片、编辑等）协同完成任务。

重构前，这些节点之间怎么传数据全靠约定。重构时我做了一个关键决策：**每个 Capability 用 Pydantic 声明输入输出**，Protocol 定义协议、不需要继承基类：

```python
@runtime_checkable
class SelfDescribingCapability(Protocol):
    @property
    def capability_id(self) -> str: ...
    @property
    def task_input_type(self) -> type[BaseModel]: ...
    @property
    def task_output_type(self) -> type[BaseModel]: ...
```

新增一个 Capability？只需要定义 Pydantic I/O 模型然后注册——系统自动发现它、自动把它的签名暴露给 Planner。不需要写一行胶水代码。

---

## 类型内省：让 Python 的类型变成可编程的数据

**这是 Python 类型系统最独特的地方**，也是我在 C++ 里做不到的事。

Python 的类型标注不会在编译期被擦除，它们作为**普通对象**存在于运行时。我利用这个特性，从 Pydantic 模型自动提取 Capability 签名：

```python
for name, field in model.model_fields.items():
    CapabilityFieldSignature(
        name=name,
        required=field.is_required(),
        value_type=_describe_annotation(
            field.annotation),
        description=field.description or "",
    )
```

提取的签名自动渲染成 Planner 能理解的文本，注入到 prompt 里。**开发者定义 Pydantic 模型的那一刻，LLM 就能看到并使用这个 Capability**——类型即文档，文档即接口。

---

## LLM 生成的执行计划也是类型安全的

Planner LLM 看到所有 Capability 的签名后，生成 `ExecutionPlan`——一组步骤通过 `input_bindings` 连接的 DAG。问题是，LLM 会产生幻觉——引用不存在的字段、类型不匹配、循环依赖。

我设计了三层保障：

1. **Few-shot 示例**：精心编写的计划范例，教 LLM 正确的绑定语法
2. **PlanValidator**：利用 Pydantic 类型信息校验 6 类错误（未知 capability、缺失绑定、类型不匹配、循环依赖……）
3. **自动重试**：校验失败时把 `ValidationIssue` 反馈给 LLM，让它自己修正

关键在第二层——**类型信息不只是给人看的，是运行时正确性检查的基础**。Pydantic 的 `CapabilitySignature` 里存着每个字段的类型，PlanValidator 拿它来校验 LLM 生成的绑定是否合法。

这是整个系统里我最得意的设计。

---

## Discriminator：事件系统的类型安全反序列化

Agent 运行时会产出大量事件——步骤开始、完成、出错、LLM 调用等。每种事件结构不同，怎么从 JSON 反序列化成正确的类型？

```python
class StepStarted(WorkflowEvent):
    event_type: Literal["step_started"] = "step_started"
    step_id: str

class StepFinished(WorkflowEvent):
    event_type: Literal["step_finished"] = "step_finished"
    output: dict

AnyWorkflowEvent = Annotated[
    StepStarted | StepFinished | ...,
    Discriminator("event_type"),
]
```

`TypeAdapter[AnyWorkflowEvent].validate_python(data)` ——一行代码，Pydantic 自动根据 `event_type` 分派到正确的类型。不需要 if-else，不需要手写工厂。

---

## 和静态语言比，还差什么？

| | 静态语言 | Python + Pydantic |
|---|---|---|
| **校验时机** | 编译期全链路 | 数据边界（对象创建时） |
| **运行时开销** | 零（编译时擦除） | 微秒级（V2 用 Rust 重写） |
| **确定性** | 编译通过=类型正确 | Pyright + Pydantic 两层 |

最根本的差距：静态语言承诺**编译通过 = 类型正确**。Python 只能做到接近，`# type: ignore` 一行就能跳过任何检查。

但在 Agent 开发里，**最大的不确定性不是类型，而是模型输出本身**。Pydantic 的"运行时校验 + 自动重试"策略，反而比编译期检查更适合这个场景。我用它做到了：LLM 输出不合法？Schema 约束 + 自动重试。执行计划有错？PlanValidator + 反馈修正。

---

## 总结

| 阶段 | 能力 | 局限 |
|------|------|------|
| 早期 Python | 纯鸭子类型 | 防御性编程 |
| PEP 484 + 3.10 | 类型标注 + 静态检查 | 运行时不校验 |
| Pydantic | 运行时校验 + JSON Schema | 只守边界 |
| 静态语言 | 编译期全链路 | 开发效率低 |

Pydantic 没有让 Python 变成 Rust，但它在 Python 的约束下找到了一个务实的平衡点。

在我的 Agent 架构里，Pydantic 不只是一个"数据校验库"——它是类型安全的脊柱。Capability 签名靠它自动提取，LLM 输出靠它约束，执行计划靠它校验，事件系统靠它分派。**一个库，撑起了整个类型化的 Agent 框架。**

作为一个写静态语言出身的程序员，我终于在 Python 里找到了一点安全感。

#Python #类型系统 #Pydantic #Agent开发 #技术分享 #架构设计 #LLM
