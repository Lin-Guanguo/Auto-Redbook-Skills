---
title: Agent Runtime 与 PL
subtitle: Typed effectful workflow runtime with explicit failure semantics
description: 关于 Agent runtime、FP/PL、类型化 effect、失败语义与研究切入点的讨论记录。
last_updated: 2026-05-08
---

# Agent Runtime 与 PL

## 背景

这篇 topiclog 记录我们围绕 Agent、函数式编程、PL 研究、LangGraph、BOC、ZIO、失败语义和个人 Agent 框架设计形成的讨论。前两篇 topiclog 已经分别保存了外部材料：

- [Agent、FP 与 Harness 资料记录](agent-fp-harness-notes-2026-05-07.md)
- [编程语言谱系](编程语言谱系-2026-05-07.md)

本篇只记录我们自己的理解和推理，不再复制外部文章。

---

## 讨论过程

### 1. 从 BOC 和 Actor 进入并发模型

我们从 Microsoft 的 BOC / `bocpy` 开始，先把它和 Actor Model 做对照。

Actor Model 的直觉是：每个资源或状态对象有一个长期管理者，所有操作都通过这个 actor 的 mailbox 进入；同一个 actor 内部顺序处理，不同 actor 之间可以并发。它的安全性来自 ownership：状态只由所属 actor 修改。

BOC 的直觉不同：资源本身是 `Cown`，操作以 behavior 的形式提交，并声明自己需要哪些资源；runtime 等这些资源都可用后，再调度 behavior 执行。它不是“资源在某个状态下自动触发操作”，而是“操作声明资源集合，runtime 根据资源可用性调度”。

因此可以把两者放进同一个大框架：

```text
Actor:
资源有长期管理者，消息进入管理者队列。

BOC:
资源没有长期管理者，操作临时声明需要哪些资源。
```

进一步抽象后，我们得到一个重要判断：很多并发模型本质上都是资源访问控制模型。它们不只是把锁藏起来，而是把“资源访问意图”提升成 runtime 可理解的结构，然后由 runtime 负责互斥、调度、恢复和观测。

### 2. Agent 执行图不是普通图

随后讨论转向 Agent。我们确认了一个基本判断：Agent 执行确实可以看成图，但不是单一 DAG，而是多张图叠在一起：

- control-flow graph：下一步执行谁，何时 stop / retry / replan；
- dataflow graph：哪些 state、message、artifact 被读写；
- effect graph：哪些步骤调用 LLM、tool、文件、网络、人类审批；
- resource graph：哪些步骤占用 repo、browser、terminal、memory、calendar；
- provenance graph：结论来自哪些 tool、source、trace；
- recovery graph：失败后从哪里恢复，哪些 effect 不能重放；
- delegation graph：parent agent、subagent、handoff、result merge。

这也是 FP / PL 概念重新变得有价值的原因：Agent 把普通程序里被编译器、runtime、OS、数据库隐藏的状态、副作用、解释器、恢复问题暴露到了应用层。

### 3. LangGraph 的语义

我们讨论了 LangGraph：它的节点通常读取当前 state，执行一段逻辑，然后返回 state update；下一步可以由固定 edge、conditional edge，或 `Command(update=..., goto=...)` 决定。

抽象形状大概是：

```text
Node: State -> Effect[Update]
Command Node: State -> Effect[Update + Goto]
```

LangGraph 的核心不是普通函数调用链：

```text
A output -> B input -> C input
```

而更像：

```text
A 读 State -> 写 State delta -> runtime 合并
runtime 根据 edge/goto 选择下一个节点
B 再读新的 State
```

所以 LangGraph 可以理解为一个 stateful graph interpreter：

```text
Graph = 程序描述
Node = effectful step
State = 共享上下文
Reducer = state merge 语义
Edge / Command = 控制流
Runtime = interpreter
```

但我们也指出：LangGraph 包装得很好，但语义并不强。它没有把 type、effect、error、resource、replay safety 这些东西变成严格的一等公民。它是工程化的 stateful graph runtime，不是强理论的 FP / PL runtime。

### 4. FP 不是因为“图”才有价值

一个关键修正是：FP 不是因为 Agent 是图才有价值，而是因为 Agent 是长时间运行、容易失败、充满副作用、部分不可预测的程序。

我们把一些 FP / PL 概念映射到 Agent 问题：

| FP / PL 概念 | Agent 中的问题 |
|---|---|
| ADT | 清楚表达等待、调用工具、失败、审批、取消、完成等状态 |
| Effect / IO | LLM、tool、file、network、human approval 都是副作用 |
| Kleisli / Monad | 上一步结果决定下一步 tool call |
| Applicative | 多个独立 tool call 可以并行 |
| Resource | browser、terminal、sandbox、DB connection 的生命周期 |
| Interpreter | 同一份 plan 可以执行、dry-run、trace、replay、估成本 |
| Reducer / Monoid | LangGraph state update 的合并语义 |

Kleisli 的直觉也被明确下来：

```text
普通函数: A -> B
Kleisli arrow: A -> F[B]
```

Agent step 通常不是 `Input -> Output`，而是：

```text
Input -> Effect[Output]
```

也就是说，每一步都可能失败、超时、花钱、访问外部系统、产生 trace。

### 5. 类型化是 FP 和 Agent runtime 的交叉点

我们进一步讨论了类型化。强类型 FP 传统强调用类型表达程序语义，不只是为了“写得高级”，而是为了把约定固化成结构。

你自己的 Agent 实践已经有了 typed input / typed output，也就是：

```text
Input -> Output
```

下一步可以升级为：

```text
Input -> Effect[Error, Output]
```

或更完整地借用 ZIO 的形状：

```text
ZIO[R, E, A]
```

翻译成 Agent：

```text
R = 这个 step 需要哪些环境、资源、工具、权限
E = 这个 step 可能失败成什么
A = 这个 step 成功产生什么
```

因此我们提炼出一个可作为个人 Agent 框架演进方向的模型：

```text
AgentStep[I, O, E, R]

I = 输入类型
O = 输出 / state update / command 类型
E = 错误类型
R = 资源需求 / capability / effect requirement
```

这个模型把几条线接到一起：

```text
ZIO       -> typed env / error / result
BOC       -> required resources and scheduling
LangGraph -> state update / command
FP        -> effect boundary and composition
Temporal  -> retry / replay / durable execution
```

---

## LLM 带来的真正差异

我们最后把“Agent workflow 与传统 workflow 的差别”收敛到两个核心点：

1. 大模型输出不稳定；
2. 大模型调用高延迟。

传统 workflow 的失败多是网络抖动、服务 500、数据库死锁、临时限流，通常可以 retry with backoff。LLM 节点的失败不只是执行失败，还包括：

- 输出格式错；
- 工具参数错；
- 理解任务错；
- 引用不存在的信息；
- 走错方向；
- 看似合理但其实错；
- 成本或延迟超预算；
- 上下文污染；
- 同样输入重试得到另一种错误。

这意味着 LLM effect 不能当作普通 HTTP effect。它更像：

```text
高延迟、概率性、语义可失败的 effect
```

我们把 LLM 失败分成几类：

| 失败层级 | 例子 | 处理方式 |
|---|---|---|
| Transport failure | API timeout、429、5xx | 可机械重试 |
| Protocol failure | JSON parse fail、schema mismatch | repair / constrained decoding / validator retry |
| Semantic failure | 参数合法但含义错 | verifier / simulation / human review |
| Planning failure | 路径选错、目标分解错 | replan / alternative candidate / rollback |
| Epistemic failure | 幻觉、证据不足 | retrieval / citation check / confidence gate |
| Economic failure | token、cost、latency 超预算 | budget-aware stop / degrade |
| Context failure | 上下文污染、旧状态误导 | compaction / pruning / reset / fork |

这也说明：LLM workflow 的容错不应该只是 `try/except + retry`，而应该是显式状态机：

```text
Pending
Running
TimedOut
ProtocolInvalid
Repairing
Verifying
Rejected
Retrying
EscalatedToHuman
Succeeded
FailedTerminal
```

这部分是 Agent / LLM workflow 相比传统开发模式最值得认真建模的差异。

---

## 对现有框架的定位

我们讨论了几个框架在这张坐标里的位置：

- LangGraph：最著名的 stateful graph runtime，但 type / effect / error / resource 语义较弱；
- Pydantic AI：Python 里较认真处理 typed deps、typed output、tool schema；
- ZIO：`ZIO[R, E, A]` 很适合作为 Agent step 的抽象参考；
- Cats Effect：适合理解 `IO`、`Resource`、`Fiber`、`Ref`、`Deferred`；
- Akka / Pekko Typed：适合理解 typed actor、supervision、mailbox、persistence；
- Temporal：适合理解 durable workflow、retry、deterministic replay、activity / workflow 分离；
- Effect / `@effect/ai`：TypeScript 里更接近 typed tools / typed errors / effect system；
- BOC：适合迁移到 resource-aware Agent scheduler。

目前还没有一个统一的“Agent 版 ZIO”或事实标准框架。现有框架各自实现了拼图的一部分。

---

## Agent + PL 研究进展

我们查到近两年的趋势：Agent + PL 在 2024 年还比较散，2025 年明显升温，2026 年开始形成 workshop 和议题集合。PLDI 2026 的 PAgE workshop 是一个明显信号，它关注：

- type-safe tool interfaces；
- agent memory / state management；
- agent plan verification；
- agent runtimes / compilers / VMs；
- cost / latency tradeoff；
- debugging and observability。

值得后续精读的方向包括：

- PAgE 2026：领域问题地图；
- BOC：资源占有与并发调度；
- Turn：Agentic computation language；
- Agint：typed / effect-aware graph compilation；
- TypePilot：用 Scala 类型系统约束 LLM-generated code；
- AgentGit：LangGraph 上的 commit / revert / branching；
- Agentic AI formalization：agent lifecycle、safety、security、functional properties。

---

## 当前形成的核心判断

1. 不是所有“Agent 框架”都真的在处理 Agent 语义，很多只是带 LLM 节点的 workflow runtime。
2. 对你自己的系统，更准确的定位可能是：typed effectful workflow runtime with LLM calls。
3. LLM 应该被视为一种特殊 effect，而不是普通函数或普通 HTTP 调用。
4. Agent runtime 的关键不只是图执行，而是 typed failure semantics、budget-aware scheduling、checkpoint / replay、human escalation、trace and provenance。
5. FP / PL 的价值不是提供术语，而是提供判断结构：状态是否清楚，副作用是否显式，错误是否进入通道，资源是否可治理，执行是否可解释和重放。
6. 你当前已有 typed input / output，下一步最值得补的是 typed error 和 resource / effect declaration。

---

## 后续可做的小实验

### 1. 给个人 Agent step 增加错误类型

先把所有失败分成三类：

```text
可机械重试
可修复
需要重新判断
```

再逐步扩展为更细的 LLM / Tool / Permission / Timeout / Budget / Validation / Semantic error。

### 2. 定义 `StepSpec`

一个 step 可以声明：

```text
name
input_schema
output_schema
possible_errors
required_resources
replayable
timeout
cost_budget
```

这会把 `Step[I, O, E, R]` 从概念变成框架内的元数据。

### 3. 做 LangGraph state/effect analyzer

扫描一个 LangGraph graph，输出：

```text
node 读哪些 state
node 写哪些 state
可能 goto 哪些节点
调哪些 tool
有哪些 replay / resource 风险
```

这可以作为 Agent + PL 方向的一个小 artifact。

### 4. BOC-inspired Agent scheduler

把 repo、browser、terminal、memory、calendar 等资源看成 `Cown` 类对象。每个 step 声明自己需要哪些资源，runtime 根据冲突图调度并发。

### 5. Checkpoint / replay safety 分类

把 effect 分成：

```text
pure step
replay-safe effect
non-replayable effect
compensatable effect
human-approved effect
```

这会直接改善长流程 Agent 的恢复语义。

---

## 开放问题

- `AgentStep[I, O, E, R]` 中的 `R` 应该表示资源、环境、capability，还是 effect requirement？
- LLM semantic failure 如何验证？validator、verifier、retrieval、human review 的边界在哪里？
- 哪些 effect 可以 replay，哪些必须 commit / compensate？
- 对个人 Agent 框架来说，强类型应该加到哪一层最划算：tool schema、state、error、resource，还是 checkpoint？
- LangGraph 现有生态能不能通过外部 analyzer / decorator 补上 typed effect metadata？
- Agent + PL 的研究如果要形成自己的贡献，应该做框架、论文阅读笔记、还是先做一个小工具 artifact？

---

## 引用章节：外部资料阅读顺序

阅读资料分两块：一块是语言、effect system 和 workflow runtime；另一块是 Agent 相关的生产实践与研究论文。优先看更贴近生产的资料，再精读论文。

### A. 语言、Effect 与 Runtime

1. [ZIO core reference](https://zio.dev/reference/core/zio/) (accessed: 2026-05-08)

   先看 `ZIO[R, E, A]` 的核心模型。这里的重点不是写 Scala，而是理解“程序需要什么环境、可能失败成什么、成功产出什么”。这正好对应 `AgentStep[I, O, E, R]` 里的 `R / E / O`。

2. [Cats Effect docs](https://typelevel.org/cats-effect/docs/getting-started) (accessed: 2026-05-08)

   重点看 `IO`、`Resource`、`Fiber`、`Ref`、`Deferred`。它适合建立“副作用是可组合的描述，runtime 负责解释执行”的直觉。

3. [Pekko Typed actors](https://pekko.apache.org/docs/pekko/current/typed/index.html) (accessed: 2026-05-08)

   重点看 typed actor、supervision、mailbox、persistence。它对应长期运行实体、失败隔离和监督树，能连接前面关于 Actor 的讨论。

4. [Temporal durable execution](https://docs.temporal.io/) (accessed: 2026-05-08)

   重点看 workflow / activity 分离、retry、timeout、deterministic replay。Temporal 不是 Agent 框架，但它的长流程恢复语义比大多数 Agent 框架成熟。

5. [BOC: When Concurrency Matters](https://www.microsoft.com/en-us/research/publication/when-concurrency-matters-behaviour-oriented-concurrency/) (accessed: 2026-05-08)

   重点看 `Cown`、behavior、多个资源的 exclusive access 和 deadlock-free scheduling。它对设计 resource-aware Agent scheduler 很有启发。

### B. Agent 生产实践与框架资料

1. [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (accessed: 2026-05-08)

   这是偏生产经验的文章，适合先看。它会帮助区分 workflow 和 agent，并强调不要过早复杂化。和我们“很多 Agent 框架其实是带 LLM 节点的 workflow runtime”的判断一致。

2. [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) (accessed: 2026-05-08)

   看 Agent、tool、handoff、guardrail、tracing、session 这些生产 API 如何组织。它适合作为“主流厂商如何包装 Agent runtime”的参考。

3. [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (accessed: 2026-05-08)

   更偏落地指南，可以看它如何定义 agent、tool、guardrail、human-in-the-loop 和 deployment checklist。

4. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) (accessed: 2026-05-08)

   回看 checkpointer、thread、state snapshot、resume 语义。LangGraph 的价值主要在 stateful graph execution，不在强类型 effect system。

5. [Pydantic AI dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/) (accessed: 2026-05-08)

   重点看 typed deps、`RunContext`、output type / validation。它是 Python 生态里较贴近 typed boundary 的 Agent 框架。

6. [Microsoft Semantic Kernel Process Framework](https://learn.microsoft.com/en-sg/semantic-kernel/frameworks/process/process-framework) (accessed: 2026-05-08)

   关注 step input/output、event-driven workflow、process state 和 audit。它比“纯 agent loop”更接近企业 workflow runtime。

7. [Microsoft Semantic Kernel Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/) (accessed: 2026-05-08)

   关注 sequential、concurrent、group chat、handoff、magentic orchestration。适合观察大厂如何把多 Agent 模式包装成产品 API。

8. [Google Cloud Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) (accessed: 2026-05-08)

   偏部署和生产运维视角，适合看大厂如何处理 agent deployment、managed runtime、observability 和服务化。

### C. Agent + PL / 论文与研究资料

下面按“与我们讨论的相关性”和“影响度 / 成熟度”排序。这里的“影响度”不是引用数，而是对当前问题的参考价值和来源成熟度。

| 资料 | 相关性 | 影响度 / 成熟度 | 建议读法 |
|---|---|---|---|
| [PAgE 2026: Principles of Agentic Engineering](https://pldi26.sigplan.org/home/page-2026) (accessed: 2026-05-08) | 很高 | 早期方向标；workshop 尚未举办 | 先读 CFP 主题，把它当 Agent + PL 问题地图，不当成熟论文集 |
| [BOC: When Concurrency Matters](https://www.microsoft.com/en-us/research/publication/when-concurrency-matters-behaviour-oriented-concurrency/) (accessed: 2026-05-08) | 高 | OOPSLA / Microsoft Research 线，PL 可信度高 | 精读并发语义，重点迁移到 Agent resource scheduling |
| [Turn: A Language for Agentic Computation](https://arxiv.org/abs/2603.08755) (accessed: 2026-05-08) | 很高 | 预印本，概念新，尚未形成共识 | 看它如何把 LLM inference、actor、capability、typed output 做成语言 primitive |
| [Agint: Agentic Graph Compilation for Software Engineering Agents](https://arxiv.org/abs/2511.19635) (accessed: 2026-05-08) | 很高 | 预印本，和 typed/effect-aware graph 极贴近 | 重点看 typed graph、effect-aware code DAG、compiler/interpreter/runtime |
| [Quasar: Safer Code Actions for LLM Agents](https://arxiv.org/abs/2506.12202) (accessed: 2026-05-08) | 高 | 研究原型，贴近 tool/code action 安全 | 看它为什么不让 LLM 直接写普通 Python，而是设计受控 action language |
| [TypePilot: Leveraging the Scala Type System for Secure LLM-generated Code](https://arxiv.org/abs/2510.11151) (accessed: 2026-05-08) | 中高 | 预印本；Scala/type system 相关性强 | 看强类型如何约束 LLM 生成代码，连接你自己的 typed input/output |
| [AgentGit](https://arxiv.org/abs/2511.00628) (accessed: 2026-05-08) | 中高 | 预印本；工程启发强 | 看 commit / revert / branch 如何补 LangGraph 的 recovery / exploration 语义 |
| [Formalizing the Safety, Security, and Functional Properties of Agentic AI Systems](https://arxiv.org/abs/2510.14133) (accessed: 2026-05-08) | 中 | 预印本；偏 formal methods | 看 agent lifecycle、safety、security、liveness 如何形式化 |

### D. 推荐阅读顺序

更贴近当前目标的顺序：

1. 先读 Anthropic 的生产文章，校准 workflow / agent 的工程边界；
2. 读 ZIO core reference，把 `R / E / A` 作为 `AgentStep[I, O, E, R]` 的理论支架；
3. 读 Temporal durable execution，补长流程恢复、retry、replay 语义；
4. 回看 LangGraph persistence，理解当前主流框架处理 checkpoint 的方式；
5. 读 Pydantic AI dependencies / output validation，比较 Python typed boundary 能做到哪一步；
6. 读 Semantic Kernel Process Framework / Agent Orchestration，看企业产品如何包装 workflow 和多 Agent；
7. 读 PAgE 2026 CFP，建立 Agent + PL 的研究问题地图；
8. 精读 BOC，迁移到 resource-aware Agent scheduler；
9. 精读 Agint 或 Turn，选择一个最贴近“typed/effect-aware Agent runtime”的方向；
10. 最后读 Quasar / TypePilot / AgentGit，分别补 tool action 安全、强类型约束、状态分支回滚。
