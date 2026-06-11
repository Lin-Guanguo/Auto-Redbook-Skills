---
emoji: "⚙️"
title: "理解 Agent，<br>核心很简单"
subtitle: "通用守上限，专用守下限"
---

从工程实践上看，Agent 的核心并不复杂：模型在上下文里判断下一步，要么调用工具并观察结果，要么输出结果并结束。**真正复杂的是外层系统**：怎样把模型的不确定性，放进一个可观察、可约束、可恢复的工程结构里。

最近读 Anthropic / OpenAI 的 Agent 工程文章、研究 Claude Code / Codex / OpenClaw 等系统之后，我的判断是：**通用 Agent 的主形状已经基本收敛**，专用 Agent 则开始比拼业务组装和效果评估。

---

## 1. Agent 的最小模型

现代 tool-calling Agent 的底层循环可以简化成：

```text
model -> tool call -> observation -> model
```

模型看到上下文，决定要不要调用工具。Runtime 执行工具，把结果放回上下文。模型再根据新的 observation 决定下一步。

这个思想最早可以追溯到 **ReAct**：让模型交替生成 reasoning trace 和 action。今天的模型把 tool call 做成了一等公民，但**核心循环没有变太多**。Claude Code、Codex、OpenClaw、LangChain `create_agent`，内层都可以近似看成这种 loop。

> Agent 的核心循环很简单，复杂的是外层 harness。

这里的 harness 指的不只是 prompt，而是 prompt 外面的运行系统。它决定模型能看到什么、能做什么，以及每一步结果如何被约束、恢复和评估。过去我们说 prompt engineering，后来说 context engineering，现在很多真实系统其实是在做 **harness engineering**。

---

## 2. Tool Surface 决定产品形态

复杂 Agent 的下一步，不是让模型"想得更多"，而是设计模型到底**能做哪些 action**。

这里的 tool 不只是普通 API。文件读写、shell、计划管理、skill、subagent、长程任务，都可以被包装成模型可调用、runtime 可约束、结果可回到上下文的**行动接口**。这就是 **tool surface**。同样是 model-tool-observation loop，不同产品差异很大一部分来自 tool surface。

### Coding Agent

软件任务的不确定性很高，模型一开始通常不知道真实计划是什么，需要先观察文件系统和运行结果。它的 tool surface 通常围绕：

- **文件读写**：读代码、改文件、写新文件
- **搜索定位**：按文件名、文本、符号或引用查上下文
- **命令执行**：跑测试、构建、脚本、诊断命令
- **计划管理**：维护 todo、计划、任务进度
- **委托执行**：启动 subagent，分担搜索、分析、实现或 review
- **后台任务**：让长时间运行的子任务在另一个生命周期里继续

**shell 几乎成了开放式软件任务的标准行动接口。**

---

### Personal Agent

OpenClaw 这类 personal agent 不是把 Agent 放进代码仓库，而是放进**长期运行的个人助理环境**。它的 tool surface 更关心：

- 记忆、长期偏好和会话连续性
- 多渠道消息、浏览器、外部应用和设备
- 定时任务、heartbeat、子会话和后台生命周期
- 用户身份、权限和副作用边界

它的难点不是单次任务计划，而是 **continuity 和 access boundary**：它要知道"谁在和我说话""哪些记忆相关""哪些动作需要确认"。

### 异步 Tool

普通 tool 更像函数调用：结果立刻作为 observation 回到上下文。但 cron、heartbeat、subagent、background task 更像**异步 tool**：一次 tool call 启动一个长生命周期执行，真实工作在另一个生命周期里并发进行。

这说明 tool surface 不只是"函数集合"。**它决定模型能触达什么空间**：文件系统、shell、记忆、会话、后台任务、未来时间点、外部系统，甚至其他 Agent。这也是通用 Agent 继续演化的主要方向。

---

## 3. 范式沉淀成控制原语清单

有些文章会把 Agent 架构拆成很多种：Reflection、Tool Use、ReAct、Planning、PEV、Multi-Agent、Blackboard、Memory、ToT、Dry-Run、Self-Improve……

这些分类有价值，但**不应该当成互斥 taxonomy**。很多模式并不在同一个抽象层级，也经常可以组合。我更倾向于把它们看成**控制原语清单**，而不是互相排斥的"17 种架构"。它们的价值在于提醒你：当系统出现某类失败模式时，可以引入哪种 state、control flow、router 或 evaluator。

更有用的看法是：**每种设计都在解决一个具体问题**。可以问四个问题：

1. 新增了什么 **state**？
2. 新增了什么 **control flow**？
3. 新增了什么 **router / gate**？
4. 新增了什么 **evaluator**？

---

## 控制原语清单

| 问题 | 常见设计 | 本质 |
|---|---|---|
| 输出质量不稳 | Reflection / Self-Improve | 增加 critique 和质量闭环 |
| 模型无法触达外部世界 | Tool Use / ReAct | 增加行动接口和 observation loop |
| 多步任务容易失忆 | Todo / Plan / Workflow | 把步骤、进度和终止条件显式化 |
| 工具失败会静默传播 | PEV / Validator | 把验证接入主回路 |
| 单个 prompt 角色太多 | Multi-Agent / Subagent | 拆成角色或上下文隔离单元 |
| 跨轮状态丢失 | Memory / Session / Blackboard | 把历史状态和中间产物显式保存 |
| 副作用风险高 | Dry-run / Approval Gate | 把真实动作放进闸门 |
| 路径会分叉且需要回溯 | ToT / Search / Simulation | 把推理变成搜索或预演 |

这些设计本质上是在处理 **LLM 进入工作流之后带来的不确定性**。它们不是越多越好，而是要在**问题真的出现时才引入**。

---

## 两条优化路线

最小 tool loop 适合开放探索，因为模型可以根据 observation 自由调整路径；**约束加得太早，可能限制模型发挥**。

所以通用 Agent 会尽量保留这个最小 loop。它不是没有 plan、没有 memory、没有 subagent，而是不把所有任务都强行编译成一个标准 workflow。**它宁愿多花 token、多做 observation，也要保留开放任务里的动态性。**

但专用场景不同。面对会被重复执行成千上万次的流程，系统不能只追求少数情况下的高上限，还要**保证大多数情况下的质量下限**。这时就需要把原本靠模型临场判断的东西，逐步变成显式 state、workflow、validator、repair、fallback 和 evaluation。

于是形成两条优化路线：

> **通用 Agent 守能力上限**：保持最小 loop，持续扩展 tool surface 和 harness。
> **专用 Agent 守质量下限**：把高频、可验证的业务流程收束成显式控制流，用程序负责验证、调度和恢复。

---

## 4. Plan 是通用和专用的分水岭

Plan 解决的不是"模型会不会想"，而是复杂过程中 Agent 还能不能**稳定把事做完**：不要失忆、不要跑偏、不要重复劳动、不要不知道什么时候停止。

它有点像人在按 SOP 做事。SOP 未必提高能力上限，但能减少低级错误，**提高交付质量下限**。从"搭积木"的角度看，**Plan 是最关键的中间件**：它决定模型的自由探索，什么时候变成 runtime 能验证、调度和恢复的结构。我倾向于把 Plan 分成三类。

### 4.1 Context Plan

计划主要**给模型和用户看**，不是 runtime 的标准调度协议。常见形式是 todo list、文字计划、plan mode、manager ledger。

例如很多 coding agent 会维护一个 todo list，让用户看到进度，也让模型不要忘记任务。但 runtime 通常不会读取 todo list 自动调度——**下一步做什么，仍然由模型根据上下文判断**。

优点是灵活，适合开放任务。缺点是 runtime 很难证明它真的完成了。这是**通用 Agent 最常见的计划形态**：plan 帮助模型和用户协作，但主控制权仍然留给模型。

---

### 4.2 Workflow

计划由**开发者写成 graph、DAG 或代码**。节点、边、条件、循环、人工确认点都由开发者明确设计，runtime 按图执行。

优点是**稳定、可审计、容易恢复**。缺点是动态性弱：对高度开放的任务，如果一开始就强行写死 workflow，系统会变重，也会牺牲模型根据 observation 动态调整的能力。

Workflow 适合稳定流程：客服工单分类、邮件处理、审批流、数据清洗、固定生产管线。模型负责局部判断或内容生成，runtime 负责流程。

### 4.3 Dynamic Workflow

workflow 不完全由开发者预先写死，而是**在运行时由模型、planner 或其他程序生成、选择或修复**，再交给 runtime 执行。Claude Code 的 Dynamic Workflows 是典型例子：Claude 生成 JavaScript orchestration script，runtime 在后台执行。

它试图同时拿到两件事：**模型带来的动态性，runtime 带来的稳定性**。代价是系统复杂度上升：plan schema、binding、validator、state management、replay、resume 都要设计。这也是**专用 Agent 最值得关注的区域**。

---

## 5. Planned DAG Workflow

先交代定位：它属于 Dynamic Workflow——planner 在运行时生成执行结构，runtime 负责验证和执行。不是公开的权威方案，而是**我根据自己所在业务的流程设计的一套实践**。

以一个内容创作类业务 Agent 为例，它要把用户输入转换成多步骤生产流程：理解意图、选风格、写脚本、增强页面、生成角色参考、生成图片、生成音频、汇总返回。

如果每一步都让模型重新判断下一步，系统会非常灵活，但**成本和不确定性都高**。模型可能重复做事、跳过必要步骤、错误引用历史产物、或在业务边界之外"发挥"。这时，问题不再是"Agent 有没有能力调用这些工具"，而是**这些工具该按什么顺序组合，哪些输出必须被验证，失败后怎么恢复**。

所以这类系统更适合一种 Plan-and-Execute：

```text
planner 生成 workflow DAG
-> runtime 验证并执行
-> 内部的能力模块完成具体步骤
```

顶层不是一个自由行动的 LLM manager，而是**程序化 workflow runtime**。LLM 参与其中，但主要产出结构化的产物。

---

一个脱敏后的 plan 大致像这样（节选）：

```json
{
  "execution_steps": [
    {
      "step_id": "style_select_0",
      "capability_id": "style_select",
      "input_bindings": {
        "intent": "input.user_text"
      }
    },
    {
      "step_id": "page_enhance_0",
      "capability_id": "page_enhance",
      "input_bindings": {
        "style": "style_select_0.style_description"
      }
    }
  ]
}
```

这个 Plan 不是给模型看的步骤文本，而是 **runtime 可以验证、调度和执行的 contract**。Runtime 可以检查：引用的能力模块是否存在、输入绑定是否指向可用的输出、DAG 是否有环、必要步骤是否缺失。

还有一个实际设计点：专用 Agent 往往不应该让同一个 planner prompt 覆盖所有对话场景。把端上的入口差异（闲聊、正式生成、首次引导、编辑调整）作为 **request mode** 传入 Agent，先做一次**场景收束**：让 planner 在更小、更明确的场景里生成 DAG，牺牲一点通用性，换来更清晰的 planner policy 和更稳定的输出下限。

---

## 6. 靠程序化设施兜底

真正落到生产系统里，Plan 不能只是"模型生成出来的一段结构"。它必须能**被验证、修复、观测和评估**。至少有三层设施。

### Plan-level Validation

Planner 产出的 workflow DAG 要先被检查：能力模块是否存在、输入绑定是否合法、依赖是否可达、当前业务模式下是否允许这些步骤。它保护的是：**这一轮 workflow 能不能被 runtime 执行**。

### Step-level Validation and Repair

某个步骤即使输出了合法 JSON，也可能在业务语义上错：编错了序号、引用错了对象。

> structured output 只解决"可解析"，不保证"业务正确"。

有时更好的解法不是在 prompt 里反复强调"不要弄错"，而是**改变任务表示**：不让模型直接输出容易漂移的数字下标，而是给每个对象一个稳定代号。Repair 也要非常克制：

> Repair must be narrower than validation.

repair 只能修 runtime 能证明意图的错误。不能证明的，就应该 retry、fallback、drop 或显式失败。

---

### Evaluation and Telemetry

生产化 Agent 不能只看单次 demo。**搭积木搭得好不好，最后必须落到指标上**，持续记录三类信号：

- **计划质量**：valid plan rate 和 one-shot success
- **执行健康度**：step failure、repair 路径、replan 和 fallback 频率
- **最终效果**：人工介入率、用户侧真实完成率和 token 成本

没有这些指标，系统会停留在"看起来能跑"，但不知道为什么成功，也不知道为什么失败。

## 7. 最大难点：模型和程序的边界

难点不是让模型输出 JSON，而是**持续定义模型和程序各自负责什么**：哪些自由度允许交给模型，哪些必须被 runtime 收回；哪些错误可以自动修，哪些必须重试或交给人。

这条边界不是一次划完的。**模型聪明的地方，往往也是它最容易越界的地方**：看起来更贴心的发挥，可能正好破坏了系统依赖的稳定结构。

通用 Agent 更像"给聪明人一堆工具，让他自己解决问题"。专用 Agent 更像"让聪明人参与流程设计和局部判断，但**关键协议、状态、验证和副作用由系统接管**"。

---

## 8. 结论

计算机长期给人的默认印象是：程序虽然可能写错，但**执行本身是确定、可重复的**。LLM 进入程序主循环之后，这个前提被打破了一部分。程序开始带上人的特征：会理解、会迁移、会补全，也会误解、遗忘、过度泛化。

所以很多 Agent 工程问题，本质上像是在**把过去用来管理人的方法搬进程序系统**。人会通过计划、检查、审批、复盘和 SOP 来降低协作中的不确定性；Agent 系统也需要类似机制，只是这些机制最终要落到 runtime 里。

最后，我对 Agent 架构演进的判断是：

> 通用 Agent 的形状已经基本固定：保持最小 loop，把复杂度放进 tool surface 和 harness。专用 Agent 则进入组装和评估阶段：积木已经齐全，竞争的是业务组合能力、模型契合度和效果评估能力。

真正高级的 Agent，不是更敢做事，而是**更知道什么时候继续、什么时候停、什么时候重试、什么时候拒绝、什么时候让程序或人接管**。
