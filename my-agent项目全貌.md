# my-agent 项目全貌文档
# 适用于：Claude Code 和普通 Claude 对话
# 用法：新对话开始时直接粘贴此文件内容
# 最后更新：2026-06-14（含三类文件体系、前置检验表）

---

## 一、用户背景

- **技术水平**：Python 初学者（会列表、字典、类基础用法）
- **开发环境**：Windows + Cursor + DeepSeek API
- **时间投入**：工作日 3-4 小时，休息日 8 小时以上，约 800 小时/6 个月
- **已有账号**：Telegram、DeepSeek API、Qdrant Cloud
- **待注册**：Tavily API（tavily.com）

---

## 二、目标

- **主攻**：字节跳动 / 腾讯 AI Agent 实习岗（6 个月内投递）
- **保底**：深圳中小科技公司 AI Agent 正式岗
- **项目定位**：面试作品集主项目，每行代码独立写，不 fork 他人项目

---

## 三、参考项目

### akashic-agent（D:\akashic-agent）
- 原作者：huashen（GitHub: kachofugetsu09），北京工业大学，做完此项目后进入腾讯实习
- **用途**：功能参考 + 架构参考。月2起每完成一个模块就读对应文件，记录差异，存入 notes.md
- **不做的事**：不 fork、不直接复制代码

### nanobot（D:\nanobot）
- 来源：HKUDS/nanobot（GitHub 开源），4000行Python，专为可读性设计
- **用途**：每写完一个模块后，花10-15分钟读 nanobot 等价文件，只做一件事：
  > "它比我的版本多处理了哪些情况？"
- **英文资源**：DeepWiki（deepwiki.com/HKUDS/nanobot）、WangyiNTU/nanobot-study（GitHub）

### nanobot 对照表

| 你要写的文件 | 先读 nanobot 的 | 你会提前发现 |
|------------|----------------|------------|
| `agent.py`（手写循环）| `nanobot/agent/runner.py`（前120行）| tool_call 解析方式、迭代终止条件 |
| `tools/web_search.py` | `nanobot/agent/tools/web.py` | 结果截断、超时处理 |
| `tools/memory_recall.py` | `nanobot/agent/tools/search.py` | 检索结果格式化 |
| `session.py` | `nanobot/session/manager.py` | JSONL 格式存储对话历史 |
| `memory/consolidate.py` | `nanobot/agent/memory.py` | 触发时机设计 |
| `agent/nodes.py` | `nanobot/agent/runner.py`（完整）| 完整 tool loop 生产级实现 |

---

## 四、项目描述

### 用户体验视角
在 Telegram 里和 AI 对话。它能做三件普通聊天机器人做不到的事：
1. **记住你**：上周说过"我不喜欢咖啡"，下周它还记得
2. **主动搜索**：问"今天北京天气"，它去搜索，不是乱编
3. **记忆管理**：自动压缩整理记忆，不会因为记忆太多变蠢

### 技术视角（数据流）
```
用户发消息
    ↓
bot.py 接收（Telegram）
    ↓
agent（LangGraph 图）决策：
    ├─ 直接回答 → 调 DeepSeek
    ├─ 需要搜索 → Tavily → 结果给 DeepSeek
    └─ 需要查记忆 → Qdrant 向量检索 → 相关记忆给 DeepSeek
         ↑
    每次对话结束：新内容向量化存入 Qdrant
    记忆超量时：DeepSeek 压缩整合旧记忆
```

### 面试叙述视角
> "我从零构建了一个 Telegram AI 助手，核心是语义记忆系统：用 Embedding 把对话内容向量化存入 Qdrant，检索时加了 Rerank 步骤提升精度，并用 LLM 自动压缩整合旧记忆。Agent 用 LangGraph 做工具调用和状态管理，支持联网搜索。我写了评测脚本测量 Recall@5，Rerank 前后从 X% 提升到 Y%。在实现过程中对照了 nanobot 和 akashic-agent，积累了 20+ 条设计差异点。"

---

## 五、完整项目架构

### 手写阶段（月 1-2）
```
my-agent/
├── [第一类] config.py           ← 读取所有 API key 和配置（.env文件）
├── [第一类] llm.py              ← 封装 DeepSeek API 调用，async
├── [第二类] bot.py              ← Telegram 收发消息
├── [第二类] agent.py            ← 手写 agent 循环（月2临时版，理解原理用）
├── [第二类] session.py          ← 当前对话的短期记忆（最近 N 条消息）
├── tools/
│   ├── [第一类] web_search.py   ← 调 Tavily 搜索
│   └── [第一类] memory_recall.py← 查询向量数据库，返回相关记忆
├── memory/
│   ├── [第一类] embed.py        ← 调 Embedding API，文字→向量
│   ├── [第三类] store.py        ← 向量数据库增删查（月3先ChromaDB，月5迁Qdrant）
│   ├── [第三类] search.py       ← 相似度检索 + Rerank
│   └── [第三类] consolidate.py  ← 记忆超量时用 LLM 压缩
└── main.py                      ← 启动入口
```

### 月 3 加入（LangGraph 正式版）
```
agent/
├── [第一类] state.py    ← LangGraph 状态定义（TypedDict）
├── [第三类] graph.py    ← LangGraph 图结构（节点 + 条件路由）
└── [第二类] nodes.py    ← 每个节点的具体逻辑
```

### 月 4-5 加入
```
eval/
└── [第二类] metrics.py  ← Recall@5 评测脚本（15个手工测试案例）

[第三类] scheduler.py    ← APScheduler 定时任务：每日查近期记忆，LLM 决定是否主动推送
notes.md                 ← 持续记录：与 nanobot / akashic-agent 的设计差异
```

---

## 六、依赖关系与构建顺序

### 依赖方向（谁依赖谁）
```
config.py（被所有人依赖）
    ↓
llm.py          embed.py
    ↓                ↓
consolidate.py  store.py
                    ↓
                search.py
                    ↓
            memory_recall.py  web_search.py
                    ↓                ↓
              session.py ←→ agent.py（手写临时版）
                                ↓
                         agent/（LangGraph正式版）
                                ↓
                             bot.py
                                ↓
                             main.py
                                ↓
                          scheduler.py（月5加入）
```

### 铁律：tools/ 永远不得 import agent/ 内容
违反此规则会产生循环依赖，Python 运行时报错。

### 构建顺序（必须遵守）
config.py → llm.py + embed.py → store.py → search.py
→ tools/ → session.py + agent.py（手写）→ bot.py → main.py
→ agent/（LangGraph，月3替换）→ eval/（月4）→ scheduler.py（月5）

---

## 七、技术选型理由（面试必备）

| 技术 | 替代方案 | 选择理由 | 接受的代价 |
|------|---------|---------|----------|
| DeepSeek | GPT-4、Claude | 价格极低（约 GPT-4 的 1/200），中文好，API 格式兼容 OpenAI | 复杂推理弱于 GPT-4 |
| ChromaDB（月3）→ Qdrant（月5）| 全程 Qdrant | ChromaDB 本地零部署加速开发迭代；月5迁 Qdrant 覆盖JD要求；迁移过程是面试素材 | 需迁移一次 |
| Tavily | SerpAPI、DuckDuckGo | 专为 LLM 设计（返回干净文本），有免费额度 | 较新，文档相对少 |
| 月2手写→月3 LangGraph重写 | 直接用LangGraph | 月2手写理解tool loop原理，月3用LangGraph重新实现——能解释两层 | 月3有重写工作量 |
| python-telegram-bot | aiogram、telebot | 文档最全，社区最大，v20+ 原生支持 async | 代码比 aiogram 略啰嗦 |
| APScheduler | Celery Beat、cron | 纯 Python 轻量级，不依赖额外中间件，异步兼容好 | 不适合分布式大规模任务 |

---

## 八、JD 覆盖情况（12条）

| # | JD 要求 | 覆盖方式 | 是否在项目里实现 |
|---|---------|---------|---------------|
| 1 | Python 扎实（async/类型注解/异常） | 贯穿所有文件的代码风格 | ✅ 全部文件 |
| 2 | LangGraph 深入 | agent/ 目录，月3正式实现 | ✅ 月3实现 |
| 3 | LLM API + 异常处理 | llm.py + nodes.py retry | ✅ |
| 4 | RAG 全链路 | embed→store→search→rerank→生成 | ✅ memory/ 全部 |
| 5 | 评测体系（Recall@5） | eval/metrics.py，15个测试案例，月4起建 | ✅ |
| 6 | 异常路径设计 | graph.py 错误节点，工具失败降级 | ✅ 简化版 |
| 7 | Function Calling / Tool Use | tools/ 目录 | ✅ |
| 8 | Memory 管理（短期+长期） | session.py + memory/ | ✅ |
| 9 | 向量数据库（Qdrant） | memory/store.py（月5迁入）| ✅ |
| 10 | Prompt Engineering | nodes.py + consolidate.py | ✅ |
| 11 | RAG 各步骤 | 同第 4 条 | ✅ |
| 12 | MCP 协议 | 跳过（无自然使用场景）| ❌ 跳过 |

---

## 九、6 个月详细计划（修订版）

### 月 1：能跑起来的最小 bot
**里程碑：** Telegram 发消息，bot 用 DeepSeek 回复，5次不崩溃

| 周 | 文件 | 类别 | 做什么 | 完成标准 | 完成后读 nanobot |
|----|------|------|--------|---------|----------------|
| 1 | `config.py` | **第一类** | 学 .env + 写 config.py | 不看参考能写出读取 .env 的函数 | — |
| 2 | `llm.py` | **第一类** | 完成5题训练 → 写 llm.py async版 | 独立完成 httpbin 练习后再写 | `nanobot/providers/base.py` 前50行 |
| 3 | — | — | 给 llm.py 加 retry + 超时处理 | 网络断开时有报错不崩溃 | — |
| 4 | `bot.py` | **第二类** | 写 bot.py + main.py | Telegram bot 能回复消息 | `nanobot/channels/telegram.py` |

### 月 2：手写 agent 循环 + 工具调用
**里程碑：** bot 能搜索网络，记住当前对话；能独立写最简 LangGraph 图

| 周 | 文件 | 类别 | 做什么 | 完成标准 | 完成后读 nanobot |
|----|------|------|--------|---------|----------------|
| 5 | — | — | 类型注解 + try/except + Function Calling 概念 | 能给现有文件加注解和异常处理 | — |
| 6 | `agent.py`（手写）| **第二类** | 写手写 agent 循环 | 独立写出while循环模式后再写 | `nanobot/agent/runner.py`（前100行）|
| 7 | `tools/web_search.py` `session.py` | **第一类** | 写 Tavily 搜索工具 + 会话记忆 | bot 能自主决定是否搜索 | `nanobot/agent/tools/web.py` |
| 8 | — | — | LangGraph 概念预学，只跑官方最小例子 | 能独立写2节点 LangGraph 图 | — |

### 月 3：LangGraph 正式版 + 跨会话语义记忆
**里程碑：** LangGraph 版与手写版输出一致；跨对话记住你，检索相关率 > 60%

| 周 | 文件 | 类别 | 做什么 | 完成标准 |
|----|------|------|--------|---------|
| 9 | `agent/state.py` `agent/nodes.py` | **第一类 / 第二类** | 把 agent.py 逻辑翻译到 LangGraph | 读nanobot/agent/runner.py后再写nodes.py |
| 10 | `agent/graph.py` | **第三类** | 写条件路由 + 错误节点；删旧 agent.py | 画出图结构再写代码 |
| 11 | `memory/embed.py` `memory/store.py` | **第一类 / 第三类** | Embedding + ChromaDB 本地版 | 用中文写出"向量存取"每一步后再写store.py |
| 12 | `memory/search.py` `tools/memory_recall.py` | **第三类 / 第一类** | 相似度检索 + Rerank + 接入 agent | 用中文写出Rerank原理后再写search.py |

### 月 4：记忆压缩 + 评测体系
**里程碑：** 记忆自动压缩；Recall@5 有数字；Rerank 有量化提升证据

| 周 | 文件 | 类别 | 做什么 | 完成标准 |
|----|------|------|--------|---------|
| 13 | `memory/consolidate.py` | **第三类** | 写记忆压缩 | 用中文写出压缩策略后再写代码 |
| 14 | `eval/metrics.py` | **第二类** | 手工构造15个测试案例；写评测框架 | 独立写出命中率计算函数后再写metrics.py |
| 15 | — | — | 完善 Rerank 逻辑，Recall@5 前后对比 | 有具体数字 |
| 16 | — | — | 全功能联调，月1-3所有验收测试仍通过 | 全通过 |

### 月 5：Qdrant 迁移 + 主动推送 + 完整联调
**里程碑：** Qdrant Cloud 接入；每天主动推送消息；项目无严重 bug

| 周 | 文件 | 类别 | 做什么 | 完成标准 |
|----|------|------|--------|---------|
| 17 | `memory/store.py`（迁移）| **第三类** | ChromaDB → Qdrant Cloud | Qdrant版通过月3验收；写迁移差异记录 |
| 18 | `scheduler.py` | **第三类** | 学 APScheduler → 写定时推送 | 用中文写出触发流程后再写代码 |
| 19 | — | — | 完善所有外部依赖的错误处理 | 每个外部依赖有 fallback |
| 20 | — | — | 全系统压测：连续对话20轮 | 连续运行1小时不崩溃 |

### 月 6：对照收尾 + 面试准备

| 周 | 做什么 | 完成标准 |
|----|--------|---------|
| 21 | 整理 notes.md，把月2-5积累的差异点归类 | 至少20条有观点的差异记录 |
| 22 | 基于差异记录，针对性重构 1-2 个模块 | 有改动记录 + 改动理由 |
| 23 | 整理面试叙述（设计理由 + debug经历 + 对比）| 能口头流畅讲解10分钟 |
| 24 | 写 README + 录演示视频 | 项目可直接发给面试官 |

---

## 十、月度验收标准

| 月份 | 验收标准（可测试）|
|------|----------------|
| 月1 | Telegram 发消息，bot 10秒内回复，连续 5 次不崩溃 |
| 月2 | 问天气 bot 调 Tavily；同会话问"我刚才问什么"bot 能回答；LangGraph最小例子能独立写出 |
| 月3 | LangGraph版和手写版对同组输入输出一致；15条记忆存入后随机提问，前3条相关率 > 60% |
| 月4 | Recall@5 有数字（含Rerank前后对比）；记忆超量自动压缩；月2月3测试仍通过 |
| 月5 | Qdrant Cloud 接入；scheduler.py每天定时发主动消息；工具失败时bot不崩溃 |
| 月6 | 随机打断能当场回答任意模块；notes.md有20+条有观点的差异记录；README写好 |

---

## 十一、动态更新机制

**脊梁（永不变动）：** LangGraph + 语义记忆 + RAG + Tool Use + Python async

**动态层规则：**
- 月 1-3：遇到新考察点，只记录，不处理，继续当前任务
- 每月最后一天：把记录的新词发给 Claude，由 Claude 分类
- 动态层最多同时存在 3 个额外内容，超过则替换最不重要的

---

## 十二、调试方法

### 第一反应（月 1-3 通用）
```python
print("=== 到这里了 ===")
# 出错的代码
print("=== 没有到这里 ===")
```
第一个没出现的 print 就是问题所在。

### nanobot 交叉验证（月2起，每模块完成后）
写完一个文件后，打开 nanobot 等价文件，只问：
> "它比我的版本多处理了哪些情况？"
答案记录到 notes.md。

### 全链路排查（月 4 之后）
```
消息发出了 → bot.py 收到？→ agent 被调用？→ LLM 被调用？
    → 工具被调用？→ Qdrant/Tavily 返回了什么？→ Telegram 发出回复？
```

---

## 十三、已知问题与修正（2026-06-14）

| 类型 | 问题 | 修正 |
|------|------|------|
| Bug | `llm.py` 用了 `httpx.Client`（同步）配 `AsyncOpenAI` | 改为 `httpx.AsyncClient`，现在修 |
| 冗余 | `llm.py` 有 `from unittest import result` 未被使用 | 删除该行 |
| 安全 | `.env` 含真实密钥 | 确认 `.gitignore` 包含 `.env` |

---

## 十四、akashic-agent 对应文件（月2起持续更新）

| 你的文件 | 类别 | akashic-agent 对应文件 |
|---------|------|----------------------|
| config.py | 第一类 | agent/config.py |
| llm.py | 第一类 | agent/provider.py |
| bot.py | 第二类 | bootstrap/channels.py |
| agent.py（手写）| 第二类 | agent/looping/core.py |
| tools/web_search.py | 第一类 | agent/tools/web_search.py |
| session.py | 第二类 | session/manager.py |
| agent/nodes.py | 第二类 | agent/core/passive_turn.py |
| memory/store.py | 第三类 | plugins/default_memory/engine.py |
| memory/search.py | 第三类 | agent/retrieval/default_pipeline.py |
| memory/consolidate.py | 第三类 | plugins/default_memory/engine.py |

---

## 十五、与 akashic-agent 的差异（面试差异化亮点）

| 维度 | akashic-agent | 你的项目 |
|------|--------------|---------|
| 渠道 | Telegram + QQ | 仅 Telegram |
| 记忆 | 完整记忆引擎（插件化）| 语义检索 + LLM 压缩 |
| 主动行为 | RSS推送+复杂漂移系统 | scheduler.py 每日查记忆，LLM决定是否推送 |
| Agent 框架 | 完全自定义循环 | 先手写后迁 LangGraph（理解两层）|
| Plugin 系统 | 有（10+插件）| 无 |
| 评测体系 | 无显式评测 | 有 Recall@5（含对比数据）|
| 参照记录 | — | notes.md：20+条设计差异点 |

---

## 十六、三类文件体系与四步写法

### 三类文件——理解深度不同，要求不同

**第一类：应该能自己写出骨架**
模式：调用外部接口 → 取出结果 → 返回
要求：关掉AI，能写出函数的骨架（不要求记住参数，但知道需要哪几步）
文件：`config.py` `llm.py` `memory/embed.py` `tools/web_search.py` `tools/memory_recall.py` `agent/state.py`

**第二类：需要深度理解流程，允许AI写库调用**
模式：接收输入 → 判断 → 分支执行 → 输出
要求：能在纸上画出这个文件在整个数据流里的位置，能解释每个函数"做什么、为什么需要它"
文件：`bot.py` `session.py` `agent.py`（手写）`agent/nodes.py` `eval/metrics.py`

**第三类：理解算法和目的，允许AI写实现**
模式：执行某个算法流程（涉及复杂库或框架）
要求：能用中文写出算法的每一步；写不出哪一步，就说明那一步没懂
文件：`memory/store.py` `memory/search.py` `memory/consolidate.py` `agent/graph.py` `scheduler.py`

### 四步写法——每次写文件都用这个流程

**第一步：写之前（5分钟，不能跳过）**
用注释回答三个问题，哪怕写错了也没关系：
```python
# 这个文件是干什么的？
# 它需要哪些函数？
# 每个函数大概做几步？
```
目的：在打开AI之前，强迫自己先想。

**第二步：跟AI交互时**
不要说"帮我写XXX文件"。
要说："我需要一个函数，它接收[X]，应该做[第一步、第二步、第三步]，返回[Y]。我不知道第二步怎么实现，帮我写那一步。"
区别：你在描述自己知道的需求，不在把整个思考过程外包给AI。

**第三步：写完之后（10分钟，不能跳过）**
逐行读一遍，用中文在脑子里翻译每一行在做什么。
有一行翻译不出来 → 立刻问AI那一行是什么意思 → 不要跳过去。

**第四步：验收测试（一句话）**
> 如果面试官现在问我"解释一下这个函数"，我能说吗？

能说 → 继续。不能说 → 先把说不出来的地方弄懂，才能继续。

---

## 十七、每个文件的前置检验

### 判断前置检验的原则
每个文件的核心操作模式决定了前置检验的类型：

| 类别 | 核心模式 | 前置检验类型 |
|------|---------|------------|
| 第一类 | 调用外部接口→取出结果→返回 | 能手写最简版本（代码练习）|
| 第二类 | 接收输入→判断→分支执行→输出 | 能独立写出流程逻辑（不靠AI设计）|
| 第三类 | 执行某个算法流程 | 能用中文写出算法每一步（写不出哪步就是没懂哪步）|

**推导方法（遇到新文件时用）：**
> 这个文件的核心操作模式是什么？ 我有没有独立完成过这个模式的最简版本？

### 每个文件的具体前置检验

| 文件 | 类别 | 开始写之前必须能做到 | 通过标准 |
|------|------|-------------------|---------|
| `config.py` | 第一类 | 不看代码，能写"读.env返回对应值"的函数 | 代码能跑，值正确 |
| `llm.py` | 第一类 | 完成5题训练，最后能独立调 httpbin.org/get | 不问AI能跑通 |
| `memory/embed.py` | 第一类 | 能写"调某API，取返回JSON里某字段"（同llm.py模式）| 不问AI能写骨架 |
| `tools/web_search.py` | 第一类 | 同上，换一个API地址也能写 | 不问AI能写骨架 |
| `tools/memory_recall.py` | 第一类 | 能调用另一个.py里的函数，格式化它的返回值 | 不问AI能写 |
| `agent/state.py` | 第一类 | 能定义一个含3个字段的TypedDict | 不问AI能写 |
| `bot.py` | 第二类 | 用中文写出："消息进来→调agent→把结果发回去"每一步 | 能写出且没有模糊的地方 |
| `session.py` | 第二类 | 手写一个类：列表存消息，能返回最后N条 | 不问AI能独立实现 |
| `agent.py`（手写）| 第二类 | 手写一个while循环：调函数→检查返回值里有没有特定key→有继续没有退出 | 不问AI能独立实现 |
| `agent/nodes.py` | 第二类 | 纸上画出消息到回复的完整流程图，每个判断点能解释 | 画得出来且能解释每个箭头 |
| `eval/metrics.py` | 第二类 | 手写函数：接收[期望]和[实际]，返回命中率% | 不问AI能独立实现 |
| `memory/store.py` | 第三类 | 用中文写出："文字→向量→存库→按相似度取回"每一步在做什么 | 每一步都能写，写不出的就是没懂的 |
| `memory/search.py` | 第三类 | 用中文写出：为什么先检索再Rerank，Rerank在做什么决策 | 写得出且不依赖背诵 |
| `memory/consolidate.py` | 第三类 | 用中文写出：压缩20条记忆时保留什么、丢弃什么，prompt怎么指导LLM | 写得出且有自己的判断 |
| `agent/graph.py` | 第三类 | 纸上画出LangGraph节点和边，条件路由的判断逻辑写出来 | 不靠AI自己能画出来 |
| `scheduler.py` | 第三类 | 用中文写出：触发后执行哪几步，每步失败了怎么处理 | 写得出来且没有"大概是这样" |
