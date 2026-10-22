# AI 电商运营练手项目集（个人项目 / 实战练习）

> 这是一套**用于求职的作品集项目**，目标是向「AI 产品 / 运营（需求落地）」类岗位证明：
> 你能发现业务痛点 → 写出 AI 功能需求（PRD）→ 推动落地一个能跑的原型 → 讲清效果与边界。
>
> 全部使用**公开示例数据**（包包店知识库为演示样本），不含任何真实店铺隐私；
> 项目可离线演示（演示模式），接上免费大模型 API key 后解锁真实对话能力。

## 🔗 在线 Demo（点开即玩，无需安装）

**https://shanzzjr.github.io/ai-ecommerce-portfolio/**

纯前端实现（原项目「演示模式」逻辑的网页版），零 API key、零成本，6 个项目全部可交互：
`index` 导航页 · `p1` 智能客服 · `p2` 文案+违禁词 · `p3` 评价洞察 · `p4` 数据日报 · `p5` 标题搬家 · `p6` 脚本生成。
源码见本仓库 `online-demo/` 目录（main 分支），由 `gh-pages` 分支通过 GitHub Pages 托管。

## 项目清单

| 项目 | 业务痛点 | 交付物 | 对应能力 |
|------|----------|--------|----------|
| 01 电商智能客服 | 售前高频问题重复回答、夜间无人值守、容易乱承诺 | 可跑网页 Demo + PRD + 说明 + 千牛提示词 | 需求拆解、转人工规则设计、Agent 落地 |
| 02 商品文案生成 + 违禁词检测 | 上新文案耗时长、极限词违规被罚 | 可跑网页 Demo + PRD + 说明 | 生成式需求设计、合规校验闭环 |
| 03 竞品 / 店铺评价洞察 | 评价散、差评无归因、改不动 | 可跑网页 Demo + PRD + 说明 | 数据归因、改进清单、复盘闭环 |
| 04 经营数据日报生成器 | 每天手动抄数算环比、异常发现慢 | 可跑网页 Demo + PRD + 说明 | 规则化异常检测、经营指标体系、可解释日报 |
| 05 多平台标题搬家 + SEO | 一品多发要手动改写、跨平台违规风险翻倍 | 可跑网页 Demo + PRD + 说明 | 平台规则配置化、生成+合规闭环 |
| 06 短视频 / 直播脚本生成 | 每条视频每场直播现想脚本、结构不稳定 | 可跑网页 Demo + PRD + 说明 | 内容方法论模板化、批量与 A/B |

## 怎么跑（通用步骤）

项目都是本地 Flask 网页，零部署（端口：项目一 5000 / 二 5001 / 三 5002 / 四 5003 / 五 5004 / 六 5005）：

```bash
# 1. 建环境（用你自己的 Python 也行，这里是示例）
python -m venv .venv
.venv\Scripts\activate        # Windows
# macOS/Linux: source .venv/bin/activate

# 2. 装依赖
pip install -r requirements.txt

# 3. 启动
python app.py
# 浏览器打开 http://localhost:5000
```

- **不填 key 也能跑**：自动进入「演示模式」，用规则命中返回示例答案，证明流程闭环。
- **填 key 解锁真实能力**：在页面右上「配置」里粘贴免费大模型 API key（DeepSeek / 通义千问 / OpenAI 任选），key 仅存于本次会话内存，不落盘。

## 怎么写进简历（诚实写法）

- 标题写法：`个人项目｜电商智能客服原型（需求+落地）`
- 不要写「某公司实习 / 在职项目」，写清是**自主练手 / 课程项目**。
- 量化用「可验证」的说法，例如：
  - 「覆盖包包店 6 大类售前高频问题，设计转人工规则规避承诺类风险」
  - 「输出标题/五点/详情页生成 + 极限词自动检测，降低违规风险」
  - 「对 24 条示例评价做情感+差评归因，输出按类目映射的改进清单」
  - 「设计规则化异常检测（流量 ±30% / 退款率 8% / 转化降幅 25%），自动生成带建议的经营日报」
  - 「一次输入生成淘宝/拼多多/抖音/小红书四平台合规标题，逐条过违禁词检测」
  - 「将带货脚本方法论沉淀为结构模板，批量产出分镜脚本与直播话术，支持 A/B 版本」
- 面试时能讲清：为什么做、需求怎么定、转人工规则怎么设计、效果怎么验证、边界在哪——比堆功能更有用。

## 目录

```
ai-ecommerce-projects/
├── README.md                  # 本文件
├── 面试讲稿与问答.md           # 六个项目的面试叙述 + 可能被追问的问题
├── project-01-智能客服/
│   ├── README.md              # 该项目的 PRD（需求文档）
│   ├── 千牛客服Agent提示词.md  # 可直接粘贴到千牛/客服工具的提示词
│   ├── app.py
│   ├── knowledge_base.py      # 示例知识库（包包店）
│   ├── templates/index.html
│   └── requirements.txt
├── project-02-文案生成/
│   ├── README.md              # 该项目的 PRD
│   ├── app.py
│   ├── banned_words.py        # 极限词 / 违禁词表
│   ├── templates/index.html
│   └── requirements.txt
├── project-03-竞品评价洞察/
│   ├── README.md              # 该项目的 PRD
│   ├── app.py
│   ├── analyze.py             # 情感分类 + 差评归因 + 改进映射
│   ├── sample_reviews.csv     # 公开合成的示例评价
│   ├── templates/index.html
│   └── requirements.txt
├── project-04-数据日报/
│   ├── README.md              # 该项目的 PRD
│   ├── app.py
│   ├── report_analyzer.py     # 环比 + 阈值异常检测 + 建议映射
│   ├── sample_data.csv        # 生意参谋导出格式的 14 天示例数据
│   ├── templates/index.html
│   └── requirements.txt
├── project-05-标题搬家/
│   ├── README.md              # 该项目的 PRD
│   ├── app.py
│   ├── platform_rules.py      # 四平台规则配置表 + 违禁词检测
│   ├── templates/index.html
│   └── requirements.txt
└── project-06-脚本生成/
    ├── README.md              # 该项目的 PRD
    ├── app.py
    ├── script_templates.py    # 短视频/直播脚本结构模板
    ├── templates/index.html
    └── requirements.txt
```
