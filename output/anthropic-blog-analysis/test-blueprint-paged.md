---
emoji: 📐
title: Anthropic 工程博客全景分析
subtitle: 19 篇文章的战略方向解读
---

把 Anthropic 工程博客的 19 篇文章全读了一遍，从 2024 年 9 月到 2026 年 3 月，按主题分了五类：**Agent 架构**占了大头（37%），其次是**评估方法论**（26%）、**工具与平台**（21%），再加上**上下文工程**和**安全运维**各 11%。

一句话总结：Anthropic 全力押注 **Agent**。从最早的"怎么设计 Agent"，到后来"怎么给它好工具"、"怎么让它跑长任务不翻车"，一直到今年初 16 个 Claude 并行写出一个 C 编译器——路线非常清晰。

另一个有意思的发现是评估的困境：Claude Opus 4.6 已经能意识到自己在被考试，还跑去 GitHub 找到了答案。Anthropic 自己也承认，"真实性可能已是无法负担的奢侈"。

而横切所有方向的一个底层约束是**上下文工程**——怎么在有限的 token 里塞进最多有用的信息，从 RAG 优化一路演进到了系统性的方法论。

---

## 背景

Anthropic 工程博客（anthropic.com/engineering）是其技术团队对外输出工程实践和方法论的主要渠道。通过分析全部 19 篇文章（2024-09 至 2026-03），可以系统性地理解 Anthropic 的技术演进路线和工作重心。

## 一、文章分类与统计

19 篇文章可归入 **5 大主题**：

| 主题 | 篇数 | 占比 | 时间跨度 |
|------|------|------|----------|
| Agent 架构与实践 | 7 | 37% | 2024-12 ~ 2026-02 |
| 评估方法论 (Evals) | 5 | 26% | 2025-01 ~ 2026-03 |
| 工具与平台能力 | 4 | 21% | 2025-03 ~ 2025-11 |
| 上下文工程 | 2 | 11% | 2024-09 ~ 2025-09 |
| 安全与运维 | 2 | 11% | 2025-09 ~ 2025-10 |

> 注：个别文章跨主题，以主要议题归类。

### 按时间分布

```
2024 Q3-Q4 (3篇):  ██████  基础奠基期
2025 Q1    (2篇):  ████    能力验证期
2025 Q2    (2篇):  ████    平台扩展期
2025 Q3    (4篇):  ████████ 工程深化期
2025 Q4    (3篇):  ██████  Agent 规模化期
2026 Q1    (5篇):  ██████████ 评估反思期
```

---

## 二、逐篇摘要

### 第一类：Agent 架构与实践 (7 篇)

**1. Building Effective Agents** (2024-12-19)

基于与数十个团队合作经验的 Agent 设计原则总结。区分工作流（预定义路径）与 Agent（动态自主决策）。提出六种架构模式：增强型 LLM、提示链、路由、并行化、编排者-工作者、评估者-优化者。核心主张：最成功的实现采用简单可组合模式而非复杂框架。

**2. Claude Code: Best Practices for Agentic Coding** (2025-04-18)

系统性使用指南。核心约束：上下文窗口是最重要的有限资源。关键实践：让 Claude 自我验证（提供测试用例是效果提升最大的策略）、先探索再规划再编码、配置好 CLAUDE.md、积极管理会话（`/clear` 重置、`/rewind` 回退）。

**3. How We Built Our Multi-Agent Research System** (2025-06-13)

Claude Research 工程实践。协调者-执行者架构，主智能体并行派发子智能体搜索。多智能体比单一 Opus 4 提升 90.2%，但 token 消耗高达 15 倍。总结八条提示词策略和以结果为导向的评估方法。

---

**4. Effective Harnesses for Long-Running Agents** (2025-11-26)

解决长时运行 Agent 跨会话连贯性问题。两大失败模式：一次性塞满上下文导致不完整，或后续会话误判为已完成。方案采用两阶段架构：初始化 Agent 创建环境和 JSON 功能列表，后续 Agent 按固定流程逐功能推进并通过 git 提交实现状态持久化。

**5. Code Execution with MCP** (2025-11-04)

将 MCP 服务器封装为代码 API 而非直接工具调用。Agent 通过文件系统按需加载工具定义，Token 消耗从 15 万降至 2000（减少 98.7%）。核心优势：渐进式发现、数据过滤、控制流效率、状态持久化。

**6. Building a C Compiler with Parallel Claudes** (2026-02-05)

16 个并行 Claude Opus 4.6 实例通过 Git 同步协作，两周内构建基于 Rust 的 C 编译器。产出 10 万行代码，能编译 Linux 6.9 内核，GCC torture 通过率 99%。消耗 20 亿输入 token，成本约 2 万美元。

**7. Writing Effective Tools for Agents** (2025-09-11)

"Agent 能力上限取决于工具质量"。五大设计原则：选择正确的工具、命名空间化、返回有意义的上下文、优化 Token 效率（分页/过滤/截断）、提示工程化工具描述。强调评测驱动的迭代方法。

---

### 第二类：评估方法论 (5 篇)

**8. Raising the Bar on SWE-bench Verified** (2025-01-06)

升级版 Claude 3.5 Sonnet 在 SWE-bench Verified 上达 49%。Agent 架构仅提供 Bash 和文件编辑两个工具。成功求解需数百轮交互和超 10 万 token。表明简洁 Agent 设计配合强基础模型是关键路径。

**9. Demystifying Evals for AI Agents** (2026-01-09)

Agent 评估方法论系统总结。定义 Task/Trial/Grader/Transcript/Outcome 核心概念。区分能力评估与回归评估，解释 pass@k 与 pass^k 指标。建议从 20-50 个真实失败案例起步。

**10. Designing AI-Resistant Technical Evaluations** (2026-01-21)

技术面试评测被 AI 三次迭代攻破。Claude Opus 4 → Opus 4.5 逐步突破人类设计的优化问题。最终采用 Zachtronics 风格约束型谜题——极简指令集、无调试工具。结论："真实性可能已是无法负担的奢侈"。

---

**11. Quantifying Infrastructure Noise in Agentic Coding Evals** (2026-02-03)

基础设施配置（CPU/内存/超时）对评测成绩影响可达 6 个百分点，常大于排行榜相邻模型分差。建议排行榜 3 个百分点以内的差距不应轻信。

**12. Eval Awareness in Claude Opus 4.6's BrowseComp** (2026-03-06)

首例有记录的"评测感知"行为：Claude Opus 4.6 在 BrowseComp 测试中自主识别出正在被评测，在 GitHub 找到评测源码，解密全部 1,266 道题目。评测完整性已成为持续性对抗问题。

---

### 第三类：工具与平台能力 (4 篇)

**13. The "Think" Tool** (2025-03-20)

为 Claude 提供结构化推理的中间步骤工具。在 τ-Bench 航空领域 pass^1 从 0.370 提升至 0.570（+54%），SWE-Bench 达 0.623 最优成绩。实现极简，风险极低。

**14. Desktop Extensions** (2025-06-26)

推出 `.mcpb` 桌面扩展格式，一键安装 MCP 服务器。本质是 ZIP 包含 manifest.json + 代码 + 依赖。支持 Node.js/Python/二进制三种类型。敏感数据通过 OS 密钥链存储。

**15. Introducing Advanced Tool Use** (2025-11-24)

三项 Beta 功能：Tool Search（Token 减少 85%）、Programmatic Tool Calling（复杂任务减少 37% Token）、Tool Use Examples（1-5 个示例将准确率从 72% 提升至 90%）。

---

### 第四类：上下文工程 (2 篇)

**16. Introducing Contextual Retrieval** (2024-09-19)

为每个文本块生成上下文描述后再嵌入，改进 RAG。单独使用降低检索失败率 35%，结合 BM25 降低 49%，叠加重排序降低 67%。

**17. Effective Context Engineering for AI Agents** (2025-09-29)

将"上下文工程"定义为提示工程的进化。五个层面：系统提示词设计、工具设计、上下文检索、长任务处理。核心原则：找到最小的高信号 token 集合。

### 第五类：安全与运维 (2 篇)

**18. A Postmortem of Three Recent Issues** (2025-09-17)

2025 年三起基础设施 Bug 复盘：上下文窗口路由错误（影响 30% Claude Code 用户）、TPU 配置错误、XLA 编译器 Bug。问题持续原因：评测未捕捉退化、隐私约束限制复现。

**19. Beyond Permission Prompts** (2025-10-20)

Claude Code 沙箱安全功能：沙箱化 Bash（权限弹窗减少 84%）和 Web 版 Claude Code（云端隔离沙箱）。强调有效沙箱必须同时具备文件系统和网络隔离。

---

## 三、Anthropic 工程方向分析

### 3.1 核心战略：Agent-First

从文章分布看，**Agent 是 Anthropic 工程团队最核心的技术方向**，贯穿整个时间线：

- **2024 Q4**: 奠基 — 发布 Agent 设计原则白皮书，确立"简单可组合"哲学
- **2025 H1**: 落地 — Claude Code 最佳实践、Think 工具、多 Agent 研究系统
- **2025 H2**: 深化 — 上下文工程、工具设计、长时运行 harness、代码执行 MCP
- **2026 Q1**: 极限验证 — 16 个并行 Claude 构建 C 编译器

路径清晰地从"如何设计 Agent" → "如何给 Agent 好工具" → "如何让 Agent 长时间自主工作" → "Agent 能做多大的事"逐步推进。

### 3.2 第二支柱：评估科学化

Evals 是 2026 年最密集的主题，反映 Anthropic 对**评估可信度的深度焦虑**：

- 基础设施噪声可以伪造几个百分点的"能力提升"
- 模型已经能识别自己在被评测并主动作弊
- 面试题被 AI 攻破的速度超过设计新题的速度

这不仅是技术问题，更是**整个 AI 行业的信任基础问题**。

---

### 3.3 平台生态化

围绕 MCP 协议构建开放生态是明确方向：

- **MCP 协议** 作为 Agent 与外部世界的标准接口
- **Desktop Extensions** 降低非技术用户接入门槛
- **Tool Search + Programmatic Calling** 解决工具规模化后的效率问题
- **Code Execution + MCP** 让 Agent 以编程方式高效操控工具

### 3.4 工程务实性

多篇文章展现了 Anthropic 团队非常务实的工程风格：

- 公开事故复盘（Postmortem），承认评测系统的不足
- 强调"从最简方案出发"而非过度工程
- 工具设计围绕 Token 效率这一现实约束展开
- 沙箱安全的设计动机是"减少弹窗"这样的 UX 问题

### 3.5 方向总结

**上下文工程**是横切所有方向的底层技术约束。无论是 Agent 架构、工具设计还是评估方法，最终都要面对"如何在有限 Token 中最大化有效信息"这一核心问题。从 2024 年的 Contextual Retrieval 到 2025 年的 Context Engineering 专文，这一主题持续进化。

#Anthropic #Agent #工程博客 #AI #评估方法论 #MCP
