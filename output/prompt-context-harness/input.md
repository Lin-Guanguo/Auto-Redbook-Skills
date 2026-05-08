---
title: "Prompt Engineering<br>现在还重要吗"
subtitle: '<span style="display:inline-block;background:#ffe066;padding:4px 14px;">从提示词模板</span><br><span style="display:inline-block;background:#ffe066;padding:4px 14px;">到模型可见接口设计</span><br><span style="display:inline-block;background:#ffe066;padding:3px 12px;font-size:38px;line-height:1.2;">Prompt / Context / Harness / Agent</span>'
---

真正过时的是**提示词模板**，不是 Prompt Engineering 本身。

本文讨论的是：当 AI 应用从一次调用走向 **Context / Harness / Agent**，Prompt Engineering 如何从一句话技巧，变成组织输入、schema、示例、工具描述和验证逻辑的**产品稳定性工程**。

我会把**文献、官方文档和一线实践**放在一起看：哪些技巧仍然有效，哪些问题必须下沉到 schema、validator 和 harness，以及为什么它会影响 AI 产品能不能**第一次就做对**。

---

## 先说结论

这篇文章想回答一个问题：

**Prompt Engineering 现在还重要吗？**

我的答案是：**重要，但重要的方式变了。**

它不再是写一段漂亮咒语，而是在设计模型能看见、能理解、能稳定执行的信息接口。

这个接口不只包括自然语言 prompt，也包括：

- schema description
- few-shot examples
- 字段名和字段顺序
- 工具描述
- 上下文格式
- 输出合同
- validator 和后续消费方式

换句话说，今天的 PE 更像一套**小型协议**。

## 为什么大家觉得 PE 降温了？

狭义 Prompt Engineering 的热度确实下降了。

2023 年到 2024 年那种“提示词秘籍”“万能咒语”“Act as an expert”“超级 CoT 模板”的时代过去了。模型基础能力变强以后，普通用户直接说需求，也能得到不错结果。

所以“提示词技巧”的稀缺性自然下降。

岗位层面也能看到类似趋势：Prompt Engineer 作为独立岗位并不多。这个现象不能证明 PE 没价值，但说明市场不太把“写 prompt”当成一个大规模独立工种。

它更像被吸收到产品、工程、数据、评测和 agent 架构工作里。

## 真正上升的是控制层

早期很多 LLM 应用本质上是一次调用：

用户输入 + 系统 prompt + 少量上下文，送进模型，拿回结果。

那时候 prompt 几乎就是应用能力的主要控制面。

但现在越来越多应用不是一次调用了。一个 Agent 系统可能要检索 memory、读取文件、调用工具、维护状态、处理失败、多轮执行，再把中间结果压回上下文。

问题自然从“这句话怎么写”扩大成：

- 模型这一轮应该看到什么？
- 运行环境如何组织？
- 工具结果怎么压缩？
- 失败后如何修复？
- 哪些约束写进 prompt，哪些下沉到 schema、validator 或测试？

所以 Context Engineering 和 Harness 的讨论上升，不是概念炒作，而是应用形态变化后的自然结果。

## Prompt / Context / Harness 是一条控制链

这几个词边界还没有完全统一。为了讨论方便，我用一个工程定义：

| 层 | 主要问题 | 典型内容 |
|---|---|---|
| **Prompt** | 信息如何表达给模型 | 指令、示例、字段名、schema 描述、输出格式 |
| **Context** | 模型这一轮看到什么 | 检索、压缩、排序、过滤、memory 注入 |
| **Harness** | 运行环境如何组织 | 工具、状态、失败恢复、eval、trace、fallback |

它们不是替代关系，而是**控制层上移**。

```text
Harness：整个运行环境如何组织
  Context：这一轮模型应该看到什么
    Prompt：这些东西如何被表达给模型
```

对开放式 agent 来说，Context 往往先决定上限。如果相关文件没进上下文，再好的 prompt 也救不了。

但在高稳定性 C 端流程里，另一件事同样关键：当正确材料已经给了模型，它能不能第一次就按正确方式理解和输出？

这就是 PE 仍然存在的位置。

---

## 仍然站得住的 PE 技巧：文献 × 一线经验

如果把 PE 理解成“写一句神奇提示词”，它确实越来越弱。

但如果把它理解成**模型可见接口设计**，很多技巧仍然站得住：一部分来自文献和官方文档，一部分来自我在真实产品里的反复调试。

下面不再把“研究”和“经验”分开，而是按实际工作里的动作来列。

这里的来源标记很简单：**文献**指 ICL、CoT、ReAct、instruction hierarchy 等研究；**官方文档**指 OpenAI、Anthropic、Google 等 provider guidance；**一线实践**指我在结构化输出、C 端流程、模型迁移里的经验。

### **1. 用 few-shot 定义行为范式**

这一条主要来自文献和一线实践。

Few-shot 不只是“给模型看几个例子”。文献里，in-context learning 的例子会传递输出格式、标签空间、输入分布和任务边界；实践里，它还会传递产品语气、推荐路径和边界判断。

很多时候，模型不是因为看懂了一句抽象规则而稳定输出，而是因为它看到了“这种情况应该长这样”。

这在结构化输出、路由、字段选择、工具调用里尤其明显。

但 few-shot 也会锁住旧行为。如果 schema 改了，example 还保留旧字段，模型可能继续沿用旧字段。所以 few-shot 需要和 schema、prompt 一起维护。

### **2. 把 schema description 当成局部 prompt**

这一条主要来自官方文档、文献和一线实践。

Structured Outputs 和 constrained decoding 让“稳定输出 JSON”更可靠。它们能限制模型只能生成符合 schema 的 token。

但这只解决**结构合法性**。

只要有多个合法输出，模型仍然要在合法空间里做语义选择。这个语义偏向来自字段名、字段描述、枚举值、字段顺序，以及 provider 对 structured output 的训练方式。

所以 schema description 不是给工程师看的注释。它也是**模型可见信息**。Schema 有两层作用：保证形状合法，也影响语义选择。

这和我的实践观察一致：同一个要求，写在全局 prompt 里不稳定，写进字段描述里反而更稳定。因为字段描述贴近模型即将生成的字段，离决策点更近。

### **3. 把推理写成可检查字段**

这一条主要来自文献、官方文档和一线实践。

CoT、Least-to-Most、ReAct 说明，中间步骤、任务分解、推理和行动交替，确实能改善一些复杂任务。

但直接写一句 “think step by step” 已经不是万能办法。尤其 reasoning models 出现后，一些厂商也开始强调：reasoning model 往往更适合简单直接的 prompt，显式 CoT 未必总是有益。

更稳的做法不是泛泛要求“认真思考”，而是把产品关心的中间判断写进输出结构：

- 输入是否满足条件？
- 哪些约束必须保留？
- 哪个对象是核心对象？
- 为什么选择这个分支？
- 后续生成要避免什么？

这样做不是为了暴露“真实思考”，而是把某个中间判断变成输出合同的一部分。

最终结果错了，也更容易定位：是输入理解错、条件判断错，还是最后生成偏了。

### **4. 让控制信息远离生成通道**

这一条主要来自一线实践，也和 instruction hierarchy / 安全相关研究有关。

我踩过一个典型坑：一些内部 marker、标签、路由信息，如果放进自然语言生成通道，模型可能会原样输出，甚至出现在用户可见内容里。

这本质上不是“模型不听话”，而是接口设计不干净。

如果某个信息只给系统控制流程用，不应该被用户看到，就不要混进会被生成的文本里。更好的方式是放进结构化 metadata、代码侧字段或下游不可见的控制层，而不是只靠 prompt 提醒“不要输出这个 marker”。

### **5. 给模型语义 handle，不要让它做脆弱索引**

这一条主要来自一线实践。

LLM 不擅长维护脆弱的 index 算术，尤其在长上下文、多对象、多轮编辑里。

让模型输出“第 0 页”“第 1 页”“before_index = 3”，很容易遇到 0/1-based 混乱、越界、引用错对象。

更稳的方式是给对象一个可复制的语义标签，让模型直接匹配文本 handle。

比如在多页编辑里，不让模型说“把第 0 页移到第 3 页前”，而是先把页面命名为 `alpha`、`beta`、`gamma`。后续只让模型输出“把 `alpha` 放到 `beta` 前面”。这样模型做的是文本匹配，而不是脆弱的索引计算。

原则很简单：让模型做它擅长的匹配，不要让它做它不擅长的算术。

### **6. 把工具描述写成调用合同**

这一条主要来自官方文档和一线实践。

工具描述不是 API 注释。对模型来说，它也是可见接口。

好的 tool description 不只写“这个工具做什么”，还应该说明：

- 什么时候该调用
- 什么时候不该调用
- 输入字段分别是什么意思
- 失败或信息不足时怎么处理
- 工具结果会被后续节点如何消费

否则模型可能会把工具当成普通文本能力来猜，也可能在不该调用时调用，在该调用时继续编。

### **7. 换模型，也是在迁移 prompt**

这一条主要来自官方文档和一线实践。

同一个 prompt 换模型后，不一定还能保持同样效果。

不同模型对 verbosity、few-shot、schema、reasoning instruction、工具描述、system/user 位置、temperature 的敏感度都不一样。

所以 prompt 不是完全模型无关的资产。它更像和模型、schema、上下文格式、解码参数绑定在一起的一套产品接口。

模型切换不应该被当成简单替换，而应该被当成一次 prompt migration：保留关键 case，观察行为差异，调整 prompt、schema description、few-shot 和参数，再看首轮成功率、风格一致性和失败边界是否变化。

真正影响产品体验的差异常常很细。如果这些知识只留在调 prompt 的人脑子里，就很难复用，也很难在模型升级时稳定迁移。

### **8. 不要把硬约束留在 prompt 层**

这一条主要来自文献、官方文档和一线实践。

Prompt hierarchy 和自我修正相关研究都提醒我们：prompt 只能提高概率，不能提供硬保证。

模型可能在长上下文里漂移，可能被示例覆盖，也可能在没有外部反馈的情况下越修越偏。

所以成熟的 PE 不应该把所有问题都留在 prompt 层。结构、校验、工具、代码逻辑、测试和评估，都应该参与进来。

## 今天有效的 PE 长什么样？

我现在更愿意把有效 PE 理解成**模型可见接口设计**。

| 接口元素 | 它影响什么 |
|---|---|
| **few-shot examples** | 输出范式、标签空间、产品语气 |
| **schema description** | 字段级语义选择 |
| **field order** | 模型生成顺序和注意力 |
| **reasoning fields** | 中间判断是否可见、可检查 |
| **context formatting** | 模型如何理解材料边界 |
| **tool descriptions** | 工具何时被调用、如何被调用 |
| **validators** | 哪些错误不能只靠 prompt 兜底 |

很多生产 prompt 已经不像“提示词”，而像一个协议：它规定输入怎么组织、字段怎么命名、示例怎么排列、哪些内容不能泄漏、输出必须满足什么结构、后续节点会怎么消费。

## 为什么 C 端高稳定流程更需要 PE

开放式 agent 可以慢慢来：调用工具、观察结果、反思、重试、交给 evaluator 校验，再根据错误修复。

只要最终答案好，过程慢一点、绕一点，有时可以接受。

但 C 端 APP 的很多流程不一样。

用户直接看到结果，对等待时间敏感；多一次模型调用就多一份成本和延迟；失败重试不一定能被隐藏；中间状态不稳定会损害体验。

很多时候，产品真正追求的是：用户点一下，流程顺滑完成，第一次就尽量对。

所以在这类场景里，PE 的价值不是让模型“更聪明”，而是提高**首轮命中率**。

## Demo 跑通，不等于产品稳定

一个功能 demo 能跑通，只说明链路存在。

它能不能在真实用户路径里稳定跑，往往还要继续调：

| 稳定性问题 | PE 关注点 |
|---|---|
| 入口意图是否稳定理解 | prompt 和示例是否覆盖常见路径 |
| 输出结构是否稳定 | schema、字段描述、validator |
| 语气是否符合产品 | few-shot 和风格边界 |
| 字段含义是否一致 | 字段命名和局部说明 |
| 内部信息是否泄漏 | metadata 和生成通道隔离 |
| 边界输入是否打破流程 | 测试、fallback、监控 |

事后 evaluator、validator、重试和修复当然有价值，但它们不能替代首轮稳定性。

对用户同步路径来说，后验修复越多，速度、成本和体验风险就越高。

---

## PE 的边界：它提高概率，不提供硬保证

强调 PE 仍然重要，不等于把所有问题都交给 PE。

Prompt 的本质是软控制。它能提高某个行为发生的概率，但不能提供硬保证。

对高风险要求，必须下沉到更确定的层：

| 需求类型 | 更适合放在哪里 |
|---|---|
| 偏好、语气、轻量约束 | prompt |
| 格式、字段、局部语义 | schema + examples |
| 业务红线 | validator |
| 稳定引用 | 结构化 ID 或语义 handle |
| 信息隔离 | 代码侧控制层 |
| 关键流程 | 测试、监控、fallback |
| 复杂 agent 行为 | harness、eval、trace |

更成熟的做法不是找到一段万能提示词，而是判断某个要求应该放在哪个控制层。

## 结论：PE 没死，它被重新归位了

Prompt Engineering 没有死。

死掉的是把 prompt 当咒语的想象。

在真实应用里，它正在变成一种更朴素、更工程化的能力：**设计模型可见信息的表达方式、结构和约束**。

Context Engineering 和 Harness 的上升是必然的。应用越复杂，模型看到什么、工具怎么用、状态怎么维护、失败怎么恢复，就越重要。

但只要模型还需要根据一段可见输入产生行为，Prompt Engineering 就不会消失。

特别是在高稳定性 C 端应用里，prompt 仍然直接影响用户体验。

它不一定是最外显的技术壁垒，也不一定能单独构成护城河。但真正有价值的经验，往往藏在持续调优里：理解用户场景，理解模型脾气，理解输出结构，理解失败边界，知道哪些东西写进 prompt，知道哪些应该放进 schema，知道哪些必须交给代码和 validator。

## 最后一句

它不再是提示词秘籍，而是**模型可见接口设计**。

对高稳定性 C 端 AI 应用来说，它仍然是**产品稳定性工程**的一部分。

---

## 参考资料

<span class="index-section">市场趋势与 Context / Harness</span>
<span class="index-row">Simon Willison: Context engineering (accessed: 2026-04-30)</span>
<span class="index-row">LangChain: The rise of context engineering (accessed: 2026-04-30)</span>
<span class="index-row">Anthropic: Effective context engineering for AI agents (accessed: 2026-04-30)</span>
<span class="index-row">Anthropic: Effective harnesses for long-running agents (accessed: 2026-04-30)</span>
<span class="index-row">Anthropic: Harness design for long-running application development (accessed: 2026-04-30)</span>
<span class="index-row">Prompt Engineer job market analysis (accessed: 2026-04-30)</span>

<span class="index-section">Prompt Engineering 文献</span>
<span class="index-row">The Prompt Report: A Systematic Survey of Prompt Engineering Techniques (accessed: 2026-04-30)</span>
<span class="index-row">Rethinking the Role of Demonstrations: What Makes In-Context Learning Work? (accessed: 2026-04-30)</span>
<span class="index-row">Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (accessed: 2026-04-30)</span>
<span class="index-row">Least-to-Most Prompting Enables Complex Reasoning in Large Language Models (accessed: 2026-04-30)</span>
<span class="index-row">ReAct: Synergizing Reasoning and Acting in Language Models (accessed: 2026-04-30)</span>
<span class="index-row">The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions (accessed: 2026-04-30)</span>

<span class="index-section">Structured output / schema / provider guidance</span>
<span class="index-row">OpenAI: Introducing Structured Outputs in the API (accessed: 2026-04-30)</span>
<span class="index-row">JSONSchemaBench: Evaluating Constrained Decoding for JSON Schema (accessed: 2026-04-30)</span>
<span class="index-row">Schema Key Wording as an Instruction Channel (accessed: 2026-04-30)</span>
<span class="index-row">Google Gemini: Structured output / Prompting strategies (accessed: 2026-04-30)</span>
<span class="index-row">Anthropic: Prompt engineering overview / Prompting best practices (accessed: 2026-04-30)</span>
<span class="index-row">OpenAI: Reasoning best practices / GPT-4.1 Prompting Guide (accessed: 2026-04-30)</span>
