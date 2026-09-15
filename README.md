# dou-tone V2

`dou-tone` 是基于 `oil-tone` 重构的个人写作、改写与润色 Skill。V2 保留了 oil-tone 已经成熟的事实边界、自然表达、去 AI 味规则和确定性 lint 思路，同时把能力扩展到正式报告、科研学术、项目技术、教学材料、PPT 和个人内容。

仓库同时保留原来的 `skills/oil-tone/`，因此旧的 `$oil-tone` 工作流不会失效；新的任务建议优先使用 `$dou-tone`。

## 为什么做 V2

`oil-tone` 的优势是让个人成稿保持真实、平实、完整和易读，但它原本主要面向博客、演讲、PPT、产品介绍和社交内容。正式报告、开题论文、项目方案、教学设计等文本不仅需要“自然”，还需要文体规范、结构边界、术语一致性和更严格的事实控制。

V2 将“个人文风”升级为“个人写作系统”：先判断任务和文体，再决定允许修改到什么程度，最后执行语言优化和质量检查。

## V2 能处理什么

- 日常表达与草稿整理
- 工作总结、汇报、建设方案、申请和调研材料
- 论文、开题报告、研究现状、实验分析和科研汇报
- AI / Agent / Web / 3D / 软件项目的需求与技术方案
- 教案、说课稿、教学设计和课堂材料
- PPT 标题、页面文字和讲稿配套文案
- 博客、公众号、个人简介、GitHub 项目介绍和社交内容

## 改写级别

`dou-tone` 把修改幅度分成五级：

1. **L1 校对**：错别字、标点、明显语病。
2. **L2 润色**：优化句子和衔接，不改结构和观点。用户只说“润色”时默认使用这一档。
3. **L3 深度润色**：允许调整句序、段落和局部结构，不增加新事实。
4. **L4 重写**：保留核心事实和意思，重新组织表达。
5. **L5 成稿**：根据现有材料整理成可直接提交、汇报或发布的完整文本。

任何级别都不允许通过润色编造事实、引用、经历、实验结果或项目能力。

## 核心规则

优先级依次是：用户本轮明确指令 → 事实准确与来源边界 → 原文观点、数字、术语和引用 → 文体规范 → 可读性与去 AI 味 → 排版细节。

V2 不再把“去 AI 味”理解成机械禁词。例如“综上”“已有研究表明”“因此”在学术写作中只要承担真实结构或引用功能，就可以正常使用；需要删除的是没有来源、没有信息量或纯粹为了制造语气的套话。

## 目录

```text
skills/
├── oil-tone/                 # V1 兼容层，保留原有 Skill 与 tone_lint.py
└── dou-tone/                 # V2 主 Skill
    ├── SKILL.md              # 路由、优先级、改写级别、核心规则
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── academic-writing.md
    │   ├── daily-writing.md
    │   ├── personal-writing.md
    │   ├── ppt-writing.md
    │   ├── project-writing.md
    │   ├── report-writing.md
    │   └── teaching-writing.md
    └── scripts/
        └── dou_lint.py
```

## 使用示例

```text
使用 $dou-tone 润色这份工作总结，保持原结构和数字不变。
```

```text
使用 $dou-tone 按硕士论文语言深度润色这一节，不修改学术观点，不补造引用。
```

```text
使用 $dou-tone 把这些口述需求整理成给甲方看的项目需求说明，不展开实现细节。
```

```text
使用 $dou-tone 把这份教学设计改得适合七年级课堂，保留教学目标和知识点。
```

```text
使用 $dou-tone 用我的语气把这些材料整理成公众号文章，不虚构个人经历。
```

## lint

V1 原有检查器继续保留：

```bash
python3 skills/oil-tone/scripts/tone_lint.py --self-test
```

V2 新增 `dou_lint.py`，继续采用 FAIL / WARN 两级：FAIL 表示已确认的语言问题，WARN 表示需要结合文体和上下文判断。

```bash
python3 skills/dou-tone/scripts/dou_lint.py --self-test
python3 skills/dou-tone/scripts/dou_lint.py draft.md
```

lint 只检查已知文本模式，不能验证事实、引用、科学结论和业务状态，不能替代完整审阅。

## 安装

如果宿主支持从 GitHub 安装 Skill，可安装本仓库中的 `skills/dou-tone/`。旧版用户可以继续安装 `skills/oil-tone/`。

仓库：`https://github.com/techdou/oil-tone`

## V1 与 V2 的关系

V2 不是删除 oil-tone，也不是把所有文体强制改成同一种“豆哥语气”。`oil-tone` 继续承担成熟的个人成稿风格规范；`dou-tone` 在此基础上增加文体路由、改写强度、科研与正式文书边界以及更广的场景规则。

后续新增规则时，优先判断它属于核心规则还是某个文体规则，避免不断把所有内容堆进 `SKILL.md`。

## License

MIT
