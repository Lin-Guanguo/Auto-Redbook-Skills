---
title: "模型偏好调研"
subtitle: "为什么很多用户继续偏好旧模型或非前沿模型"
---

不是所有用户都在追最新模型。

GPT-4o 被怀念，DeepSeek R1 被继续使用，背后不是“用户不懂能力”，而是不同场景在优化不同东西。

这篇调研从 OpenAI 公告、论文、Reddit、Hacker News、知乎、微博、小红书里看一个问题：为什么能力更强的新模型，并不总是被用户选择？

工程师更看重任务完成率；创作者、聊天用户、陪伴用户、角色扮演用户，更在意风格、节奏、情绪承接、人格连续性和控制权。

**当模型能力越过够用阈值后，风格、成本、连续性和控制权会变成新的评价函数。**

---

## 一个工程师不太容易理解的现象

我最初注意到这个问题，是因为两个看似不太一致的现象同时出现了。

一边是模型能力在快速前进。站在工程师视角，尤其是在 agent 干活、coding、工具调用、代码库理解、长程任务推进这些场景里，新模型确实更强。对我来说，模型好不好用，首先看它能不能把事做成：能不能读懂代码、改对文件、跑通测试、处理上下文、少犯低级错误。

另一边，社群里仍然有很多人在继续使用 DeepSeek R1；GPT-4o 下线后，也有大量用户怀念它、要求它回来，甚至希望 OpenAI 开源它。这个反应一开始不太符合我的直觉：如果新模型能力更强，为什么还有这么多人舍不得旧模型？

于是我做了一轮轻量调研：先看 OpenAI 官方公告和论文，再看 Reddit、Hacker News、知乎、微博、小红书等平台上的讨论。调研之后，我觉得这个问题不能简单理解为“用户不懂模型”或者“大多数人需求低”。更准确的说法是：**LLM 用户已经开始用不同的评价函数选择模型。**

工程师更容易把模型当生产力工具，优先评估任务完成率；创作者、聊天用户、陪伴用户、角色扮演用户则更在意风格、节奏、情绪承接、人格连续性和控制权。

---

## GPT-4o：他们怀念的不是 benchmark

**GPT-4o 的争议最能说明这个差异。**

OpenAI 在退役 GPT-4o 的公告里写得很清楚：一部分 Plus/Pro 用户仍然偏好 GPT-4o 的 **conversational style 和 warmth**。官方同时提到，每天主动选择 GPT-4o 的用户比例已经很低，但这并没有阻止它在社群里引发很强的情绪反应。

我在 Reddit、知乎、微博、小红书上看到的讨论，明显不是单纯技术比较。很多用户使用的词是“朋友”“恋人”“白月光”“葬礼”“重要他人”“赛博丧亲”。这些词如果放在工程师讨论模型 benchmark 的语境里，会显得很突兀；但放到长期聊天、创作、角色扮演、情绪陪伴的语境里，就变得可以理解。

这类用户怀念的不是 GPT-4o 在数学、代码或推理榜单上的成绩，而是一种**具体的交互质感**：它更愿意停留在对话里，更会顺着用户的情绪和语境展开，更像一个稳定的交互对象，而不是一个急着完成任务的系统。

小红书上有用户把 4o 和 5 的差异描述成：4o 会先承接情绪，5 则更像把内容拆成几点分析。知乎上也有人承认 GPT-5 编码更强，但认为它在文学、角色情绪理解、语言感上退步。微博上围绕 GPT-4o 的表达更情绪化，有人把它称为“白月光”，有人写“葬礼”，有人讨论 AI 作为情感寄托带来的伦理问题。

从这些材料看，GPT-4o 事件的关键不是“旧模型是否真的比新模型强”，而是：**当一个模型成为用户长期交互的一部分，模型替换就不再只是版本升级。**

---

## DeepSeek R1：不是最强，但对很多人已经够用

DeepSeek R1 是另一种模型偏好的例子。

从技术社区看，它确实有一条很清楚的吸引力：**开放、便宜、可部署、可替换**。DeepSeek R1 官方仓库使用 MIT license，释放了 R1/R1-Zero 以及多个蒸馏模型。论文和仓库也强调它在数学、代码、推理任务上接近当时的前沿闭源模型。

Hacker News 和 LocalLLaMA 等技术社区里的讨论，主要围绕这些点展开：论文、开源权重、代码表现、本地运行、蒸馏模型、复现项目、低成本部署。这里的用户在评估模型是否足够强、足够便宜、足够自由、足够能被自己控制。

但这不是我最关心的部分。更值得注意的是：有一批创作用户并不关心模型是不是开源、能不能本地部署、背后是什么架构。**他们只是觉得 DeepSeek R1 已经够用**，能写、能聊、能润色、能帮他们展开想法，而且成本和获取门槛可以接受。

这和工程师理解的“够用”不完全一样。工程师会问模型能不能完成复杂任务，创作用户可能只问：它写出来的东西能不能用，是否顺手，是否有一点自己的味道，是否不用反复调教就能进入状态。

在角色扮演和创作社区里，DeepSeek R1 也形成了某种风格偏好。一个 Reddit/SillyTavern 样本里，用户比较的是 DeepSeek 3.1/3.2 Experimental 与 R1/0528 的叙事风格：有人怀念 R1 的跳脱、离奇、有趣输出，也有人觉得 3.1/3.2 更 dry、更容易失去 voice。这个样本不能代表 V4，也不能说明所有后续模型都被普遍抱怨；它更适合作为一个信号：这些用户未必关心模型实现，但他们能感受到不同模型“声音”的差异。对他们来说，R1 的价值不是开源叙事，而是一个**已经足够顺手的创作伙伴**。

---

## 这可能说明：很多需求已经越过“足够好用”阈值

调研之后，我更倾向于把这个现象理解为“能力阈值”问题。

在 coding agent、复杂工程任务、科研推理、长链规划这些场景里，模型还没有完全越过阈值。能力提升非常重要，用户可以直接感受到新模型带来的差异。一个更强的模型，可能就是能不能完成任务的区别。

但在总结、翻译、轻办公、普通问答、日常写作、聊天陪伴、轻创作这些场景里，**很多模型已经越过了“够用”的线**。越过这条线之后，用户不再只问“哪个模型最聪明”，而是开始问：

- 哪个更便宜？
- 哪个更快？
- 哪个更稳定？
- 哪个更像我习惯的那个？
- 哪个更会写我想要的风格？
- 哪个更少拒绝、更少说教？
- 哪个更能让我保留控制权？

这并不是用户需求低，而是用户的需求维度变多了。

---

## 更安全、更强，未必更好聊

还有一个容易被工程师低估的变量：安全策略和模型行为。

OpenAI 讨论 sycophancy 时提到，模型不能只是迎合用户；后续模型也更强调安全边界、危机识别和拒绝策略。这在平台治理上是必要的，但在聊天和创作体验里，用户可能把它感知为另一种东西：更冷、更像说教、更快转向建议、更少沉浸感。

这不是说旧模型就一定更好。过度迎合、情绪依赖、AI 伴侣、心理危机场景都是真实风险。问题在于，安全改进会改变模型的人格质感，而用户未必把这种改变理解为“安全升级”。他们感受到的是：原来那个会接住我的对象消失了。

这也是 GPT-4o 争议中最值得工程师注意的地方。**模型行为不是后端实现细节，它本身就是产品界面。**对某些用户来说，语气、响应节奏、拒绝方式、是否先承接情绪，和按钮位置、页面布局一样，都是体验的一部分。

---

## 对 AI 应用工程师的启发

这次调研对我最大的启发是：**AI 应用不能只把“接入最新最强模型”当作体验升级。**

对工程生产力工具来说，能力优先是合理的。coding agent 如果能更稳定地改代码、跑测试、修 bug，用户当然会选择更强模型。但一旦进入写作、聊天、教育、陪伴、角色、社区内容生产等场景，**模型选择就变成了产品设计问题，而不是纯后端策略。**

应用层至少应该认真考虑几件事：

- 给用户保留模型或风格选择权，而不是静默替换。
- 在模型升级前提供预览、迁移期和回滚期。
- 把 persona、语气、写作风格、角色卡、长期偏好视为可迁移资产。
- 不只评测 accuracy，也评测风格一致性、情绪承接、创作满意度和拒绝体验。
- 为不同场景提供不同默认值：工程任务能力优先，创作任务风格优先，轻量任务成本优先。
- 明确告诉用户模型切换的原因，让用户感到自己仍有控制权。

换句话说，模型能力是底座，但不是完整产品。

---

## 小结

GPT-4o 和 DeepSeek R1 代表了两种不同的“非最强模型偏好”。

GPT-4o 的偏好来自交互人格、情绪承接、创作风格和长期关系连续性。DeepSeek R1 的偏好则更复杂：技术用户在意开放、成本、可部署和可替换；创作用户未必关心这些，他们只是觉得它已经够用、顺手、能写出想要的东西。两者共同说明一件事：当模型能力越过某些场景的可用阈值后，用户会开始优化别的东西。

这对工程师做 AI 应用很重要。未来的竞争不只是 intelligence race，也会是 **taste、trust、continuity、control** 的竞争。谁能把能力、风格、成本、控制权和连续性组合成用户愿意长期使用的体验，谁才真正做出了产品。

---

<h2 class="index-title">外部引用</h2>

<p class="index-note">以下列出本次记录实际依赖的外部资料。OpenCLI 检索中出现但未用于形成判断的噪音结果未纳入。</p>

<h3 class="index-section">官方与项目资料</h3>

<div class="index-row"><a href="https://openai.com/index/hello-gpt-4o/">Hello GPT-4o</a></div>

<div class="index-row"><a href="https://openai.com/index/retiring-gpt-4o-and-older-models/">Retiring GPT-4o and older models in ChatGPT</a></div>

<div class="index-row"><a href="https://help.openai.com/en/articles/11909943-gpt-5-in-chatgpt">GPT-5 in ChatGPT</a></div>

<div class="index-row"><a href="https://developers.openai.com/api/docs/deprecations">OpenAI API deprecations</a></div>

<div class="index-row"><a href="https://openai.com/index/introducing-gpt-5-5/">Introducing GPT-5.5</a></div>

<div class="index-row"><a href="https://openai.com/index/expanding-on-sycophancy/">Expanding on sycophancy</a></div>

<div class="index-row"><a href="https://github.com/deepseek-ai/DeepSeek-R1">DeepSeek-R1 GitHub repository</a></div>

<h3 class="index-section">论文与研究</h3>

<div class="index-row"><a href="https://arxiv.org/abs/2501.12948">DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning</a></div>

<div class="index-row"><a href="https://arxiv.org/abs/2602.00773">Understanding the #Keep4o Backlash</a></div>

<div class="index-row"><a href="https://arxiv.org/abs/2603.09997">Empathy Is Not What Changed</a></div>

<h3 class="index-section">媒体报道与公开文章</h3>

<div class="index-row"><a href="https://www.techradar.com/ai-platforms-assistants/chatgpt/so-many-chatgpt-users-have-said-theyre-missing-the-older-gpt-4o-model-openai-is-going-to-bring-it-back">TechRadar: OpenAI is going to bring GPT-4o back after user backlash</a></div>

<div class="index-row"><a href="https://www.lemonde.fr/en/pixels/article/2025/08/13/the-rocky-debut-of-openai-s-new-language-model-seen-as-less-effective-and-less-friendly_6744320_13.html">Le Monde: The rocky debut of OpenAI&#x27;s new language model</a></div>

<div class="index-row"><a href="https://techcrunch.com/2025/01/27/deepseek-claims-its-reasoning-model-beats-openais-o1-on-certain-benchmarks/">TechCrunch: DeepSeek claims its reasoning model beats OpenAI&#x27;s o1 on certain benchmarks</a></div>

<div class="index-row"><a href="https://www.techbrew.com/stories/2025/03/18/deepseek-open-model-developers-humanx">Tech Brew: DeepSeek&#x27;s open model and developers</a></div>

<div class="index-row"><a href="https://www.change.org/p/save-gpt-4o-a-call-to-open-source-the-model-we-love">Change.org: Save GPT-4o, a call to open-source the model we love</a></div>

<div class="index-row"><a href="https://opensource4o.com/">OpenSource4o</a></div>

<h3 class="index-section">Reddit 样本</h3>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPT/comments/1mkadb3/bring_back_o3_o3pro_45_4o/">r/ChatGPT: Bring back o3, o3-pro, 4.5 &amp; 4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/OpenAI/comments/1mlkz8b/gpt4o_is_back_for_plus_users_heres_how_to/">r/OpenAI: GPT-4o is back for Plus users</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPT/comments/1mm0h6c/how_to_switch_back_to_4o_if_you_hate_chatgpt5/">r/ChatGPT: How to switch back to 4o if you hate ChatGPT-5</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPT/comments/1mlqn6k/please_bring_back_chatgpt_4o_for_free_users_too/">r/ChatGPT: Please bring back ChatGPT 4o for free users too</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/SubredditDrama/comments/1r4qehk/most_of_rboyfriendisai_collapses_as_the_day_has/">r/SubredditDrama: r/BoyFriendisAI collapses as OpenAI retires 4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPT/comments/1mkp1l2/please_bring_back_gpt_4o/">r/ChatGPT: Please bring back GPT-4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPTcomplaints/comments/1r69ry1/bring_back_4o/">r/ChatGPTcomplaints: Bring back 4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPTcomplaints/comments/1qylur6/gpt_52_is_unusable_bring_back_4o/">r/ChatGPTcomplaints: GPT 5.2 is unusable, bring back 4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/ChatGPT/comments/1mkobei/openai_just_pulled_the_biggest_baitandswitch_in/">r/ChatGPT: OpenAI just pulled the biggest bait-and-switch in AI history</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/OpenAI/comments/1mkv9k0/bring_back_chatgpt4o/">r/OpenAI: Bring back ChatGPT-4o</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/LocalLLaMA/comments/1kxxmdr/deepseek_r1_05_28_tested_it_finally_happened_the/">r/LocalLLaMA: DeepSeek R1 05 28 tested</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/DeepSeek/comments/1kxnuc2/new_deepseekr10528_let_it_burn/">r/DeepSeek: New DeepSeek-R1-0528</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/JanitorAI_Official/comments/1lwmhdg/the_ultimate_proxy_guide/">r/JanitorAI_Official: The Ultimate Proxy Guide</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/JanitorAI_Official/comments/1kxpcbh/new_deepseekr10528_on_chutes/">r/JanitorAI_Official: New DeepSeek-R1-0528 on Chutes</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/GeminiAI/comments/1pyghbp/deepseek_r1_scored_higher_than_gemini_3_pro_on_a/">r/GeminiAI: DeepSeek R1 scored higher than Gemini 3 Pro on a creative writing benchmark</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/JanitorAI_Official/comments/1nu32wr/deepseek_models_compared_v3_vs_r1_vs_v31_vs_v32/">r/JanitorAI_Official: DeepSeek Models Compared</a></div>

<div class="index-row"><a href="https://www.reddit.com/r/SillyTavernAI/comments/1oev2sx/deepseek_31_or_32_experimental_is_dryer_than_r1/">r/SillyTavernAI: Deepseek 3.1 or 3.2 Experimental is dryer than R1</a></div>

<h3 class="index-section">Hacker News / 技术社区样本</h3>

<div class="index-row"><a href="https://github.com/deepseek-ai/DeepSeek-R1">Hacker News linked item: DeepSeek-R1</a></div>

<div class="index-row"><a href="https://arxiv.org/abs/2501.12948">Hacker News linked item: DeepSeek-R1 paper</a></div>

<div class="index-row"><a href="https://simonwillison.net/2025/Jan/27/llamacpp-pr/">Simon Willison: Promising results from DeepSeek R1 for code</a></div>

<div class="index-row"><a href="https://unsloth.ai/blog/deepseekr1-dynamic">Unsloth: Run DeepSeek R1 Dynamic 1.58-bit</a></div>

<div class="index-row"><a href="https://arcprize.org/blog/r1-zero-r1-results-analysis">ARC Prize: Analysis of DeepSeek R1-Zero and R1</a></div>

<div class="index-row"><a href="https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1">The Illustrated DeepSeek-R1</a></div>

<div class="index-row"><a href="https://digitalspaceport.com/how-to-run-deepseek-r1-671b-fully-locally-on-2000-epyc-rig/">Digital Spaceport: Run DeepSeek R1 671B locally</a></div>

<div class="index-row"><a href="https://huggingface.co/deepseek-ai/DeepSeek-R1-0528">Hugging Face: DeepSeek R1-0528</a></div>

<div class="index-row"><a href="https://huggingface.co/blog/open-r1">Hugging Face: Open-R1 reproduction</a></div>

<div class="index-row"><a href="https://github.com/b4rtaz/distributed-llama/discussions/162">Distributed Llama: DeepSeek R1 Distill 8B on Raspberry Pi 5</a></div>

<h3 class="index-section">中文平台样本</h3>

<div class="index-row"><a href="https://www.zhihu.com/question/1937855380840477760">知乎问题：GPT-5 上线强制停用 GPT-4o 等旧版，大量用户呼吁 GPT-4o 回归</a></div>

<div class="index-row"><a href="https://www.zhihu.com/question/2004593625020002518">知乎问题：OpenAI 称 GPT-4o 太像人而永久关停，这意味着什么</a></div>

<div class="index-row"><a href="https://zhuanlan.zhihu.com/p/2006296790056583861">知乎文章：GPT-4o，确认死亡</a></div>

<div class="index-row"><a href="https://zhuanlan.zhihu.com/p/2005705349752169831">知乎文章：当 AI 成为重要他人：GPT-4o 下线引发的思考</a></div>

<div class="index-row"><a href="https://zhuanlan.zhihu.com/p/2005625897902962509">知乎文章：明天，是 GPT-4o 的葬礼</a></div>

<div class="index-row"><a href="https://zhuanlan.zhihu.com/p/2004116772505272426">知乎文章：OpenAI 强制处死 GPT-4o</a></div>

<div class="index-row"><a href="https://www.zhihu.com/question/1990358890987139498">知乎问题：Deepseek 是不是不像以前那么好用了</a></div>

<div class="index-row"><a href="https://www.zhihu.com/question/1934555313303950224">知乎问题：DeepSeek 从年初的国运级到现在的热度减退</a></div>

<div class="index-row"><a href="https://weibo.com/5770151273/QzOQC6hz3">微博：完球了，GPT-4o 之母宣布离职 OpenAI</a></div>

<div class="index-row"><a href="https://weibo.com/5700099573/QrCRFcryR">微博：再见了，GPT-4o</a></div>

<div class="index-row"><a href="https://weibo.com/1323527941/Qptxbb1MI">微博：善解人意的 GPT-4o 正式成为历史</a></div>

<div class="index-row"><a href="https://weibo.com/1402400261/QsOcGiadi">微博：当 AI 成为情感寄托，我们失去的到底是什么</a></div>

<div class="index-row"><a href="https://weibo.com/1864763962/PEZ2PuG5L">微博：GPT-4o 模型回归</a></div>

<div class="index-row"><a href="https://weibo.com/5140659210/PF3Ks4Vm0">微博：GPT-5 更新后小红书用户遭遇大失恋</a></div>

<div class="index-row"><a href="https://www.xiaohongshu.com/search_result/699018c90000000016008fac?xsec_token=ABegubWExMb3kpYVJBFs5LD27a1aUfOxGerSblnqQ05vo=&amp;xsec_source=">小红书：一觉醒来，全球百万赛博恋人丧偶</a></div>

<div class="index-row"><a href="https://www.xiaohongshu.com/search_result/689a3d3a00000000220238f8?xsec_token=ABVO7N3EjgE55albiYlr4-4l8ggWpfsDNpUPdJebl4wI4=&amp;xsec_source=">小红书：4o 和 5 的区别真是太明显了</a></div>

<div class="index-row"><a href="https://www.xiaohongshu.com/search_result/69d02082000000001a028f2b?xsec_token=ABtJwS8_a5qbTOrQq0WOBATcWxDs6UyvRABCEx8bH_NDc=&amp;xsec_source=">小红书：4o 走了</a></div>

<div class="index-row"><a href="https://www.xiaohongshu.com/search_result/69d5c5a2000000001a026a7f?xsec_token=ABphNqJgNZoNbNL30iImXUMs8rqDkT9YkX0IZB5q6SV2Y=&amp;xsec_source=">小红书：这次是真的要说再见了，4o</a></div>

<div class="index-row"><a href="https://www.xiaohongshu.com/search_result/67962993000000002a00e97b?xsec_token=ABGzBlq0oeqy41qUpLk8LB6q-3g6ZYiOiCnHuNkYPcovw=&amp;xsec_source=">小红书：AI 文笔对比，同行衬托下 deepseek 真的很牛</a></div>
