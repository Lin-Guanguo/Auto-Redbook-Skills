# 发布文案

## 笔记标题

从工程实践看 Agent，核心很简单

## 正文

最近读了 Anthropic / OpenAI 的 Agent 工程文章，又研究了 Claude Code、Codex、OpenClaw 这些系统，把我的判断整理成了这篇长文 ⚙️

Agent 的核心循环其实很简单：model → tool call → observation。真正复杂的是外层 harness。

我的判断是：通用 Agent 的形状已经基本收敛——保持最小循环，把复杂度放进 tool surface 和 harness；专用 Agent 则进入组装和评估阶段——积木已经齐全，比拼的是业务组合能力和效果评估。

第 6 张图是控制原语清单表，做 Agent 的朋友可以存一下 📌

#Agent #AIAgent #LLM #大模型 #ClaudeCode #AI工程 #Workflow #程序员
