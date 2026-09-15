# dou-tone V2.1

`dou-tone` 是基于 `oil-tone` 重构的个人写作、改写与润色 Skill。V2.1 重点优化 Agent 自动匹配：让 Skill 在真正需要“润色、改写、重写、整理成稿”时更容易被正确调用，同时避免因为主题涉及科研、项目、教学或文档就误触发。

仓库同时保留 `skills/oil-tone/` 作为 V1 兼容层；新的写作转换任务建议优先使用 `dou-tone`。

## 定位

`dou-tone` 只负责文字层的写作与表达规范：

- 校对、润色、深度润色、重写与基于材料成稿；
- 根据真实用途适配正式报告、学术科研、项目技术、教学、PPT 和个人内容；
- 保留事实、数字、引用、术语、责任主体和完成状态；
- 删除空泛 AI 套话、宣传黑话、模糊归因和无信息量升华；
- 与更具体的专业 Skill、DOCX/PDF/PPTX 等 Artifact 能力组合使用，而不是替代它们。

它不应该仅因为主题属于科研、项目或教学而自动介入。纯事实问答、概念解释、资料检索、代码修改、忠实翻译、仅摘要/抽取信息、以及只生成文件格式而未要求文字改写时，不应使用 `dou-tone`。

## Agent 匹配设计

Agent Skills 在 discovery 阶段主要依赖 `SKILL.md` frontmatter 中的 `name` 和 `description` 判断是否相关。因此 V2.1 把正向触发词和负向边界都写进 description：

- 正向：润色、改写、重写、整理成稿、优化表达、用我的语气；
- 负向：纯问答、解释、代码修改、忠实翻译、仅摘要或信息提取、纯文件格式生成。

Skill 被激活后仍会执行一次边界判断，防止宿主过度匹配。

## 改写级别

1. **L1 校对**：错别字、标点、明显语病和格式错误。
2. **L2 润色**：优化句子和衔接，不改观点、结构和详略比例；用户只说“润色”时默认使用这一档。
3. **L3 深度润色**：允许调整句序、段落和局部结构，不增加新事实。
4. **L4 重写**：保留核心事实和意思，重新组织表达与结构。
5. **L5 成稿**：根据已有材料整理成可直接提交、汇报或发布的完整文本。

任何级别都不能通过润色制造新的事实、引用、经历、实验结果、产品能力或完成状态。

## 渐进加载

`SKILL.md` 只保留所有场景都需要的核心规则。具体文体规范放在 `references/`，Agent 默认只读取一个主场景文件；只有真正的混合任务才再读取一个辅助场景文件。

例如：

- 科研汇报 PPT：`academic-writing.md` + `ppt-writing.md`
- 项目建设方案：`report-writing.md` + `project-writing.md`

不要一次性加载全部 references。

## 目录

```text
.
├── .github/
│   └── workflows/
│       └── validate-skills.yml
├── evals/
│   └── dou-tone-matching.md
└── skills/
    ├── oil-tone/                 # V1 兼容层
    └── dou-tone/                 # V2.1 主 Skill
        ├── SKILL.md
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

## 官方 Agent Skills 规范

`dou-tone` 遵循 Agent Skills 开放格式：每个 Skill 目录至少包含一个带 YAML frontmatter 的 `SKILL.md`；`name` 与目录名一致，`description` 同时说明能力和调用时机；详细规则放入 `references/`，脚本放入 `scripts/`。

V2.1 的 `SKILL.md` frontmatter 使用：

```yaml
name: dou-tone
description: "...做什么 + 什么时候用 + 什么时候不用..."
license: MIT
metadata:
  author: techdou
  version: "2.1.0"
  category: writing-conventions
```

不使用非标准顶层字段，以保持跨 Agent Skills 客户端的可移植性。

## 验证

仓库 CI 会在 PR 和 `main` push 时执行三类检查：

1. 使用 Agent Skills reference validator 校验每个 Skill 的 frontmatter、命名与目录规范；
2. 编译所有 Python 脚本；
3. 运行 V1 与 V2 lint self-test。

本地可运行：

```bash
python -m pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
skills-ref validate skills/oil-tone
skills-ref validate skills/dou-tone
python skills/oil-tone/scripts/tone_lint.py --self-test
python skills/dou-tone/scripts/dou_lint.py --self-test
```

Agent 自动匹配的人工回归样例位于：

```text
evals/dou-tone-matching.md
```

其中包含“应触发 / 不应触发 / 组合触发”三组测试，后续修改 description 时应同步回归。

## lint

V1 原有 `tone_lint.py` 继续保留。V2 的 `dou_lint.py` 采用 FAIL / WARN 两级：FAIL 表示比较确定的语言问题，WARN 表示必须结合文体和上下文判断。

```bash
python skills/dou-tone/scripts/dou_lint.py draft.md
```

lint 只能检查已知文本模式，不能验证事实、引用、科学结论和业务状态，也不能替代完整通读。

## V1 与 V2.1

V1 `oil-tone` 保持兼容，不删除、不破坏已有工作流。V2.1 `dou-tone` 将其成熟的事实边界、自然表达和去 AI 味思路扩展为更适合个人长期使用的写作规范，并加入更严格的 Agent 匹配边界、渐进加载和自动验证。

后续新增规则时，优先放入对应 `references/`，只有所有写作场景都必须遵循的内容才进入主 `SKILL.md`。

## License

MIT
