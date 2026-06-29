# RTA-USER Skill

RTA-USER 用于两种场景：

1. AI Agent 实时访谈客户，一问一答收集信息
2. 直接分析一份访谈逐字稿，输出用户画像和用户生命旅程

它聚焦两个核心交付：

- 用户画像
- 用户生命旅程

当前版本默认输出：

- Markdown 报告
- JSON 结构化数据
- Mermaid 图表草稿

## 适用场景

- 个人 IP 陪跑
- 咨询服务
- 专业服务行业
- 线下成交型业务
- 需要先做用户理解、再做内容选题的客户

## 目录结构

```text
.
├── SKILL.md
├── examples/
├── outputs/
├── references/
└── templates/
```

## 主要输入

- 实时问答内容
- 访谈逐字稿
- Discovery 阶段确认后的分类结论

## 主要输出

- `outputs/user-profiles.md`
- `outputs/user-lifecycle.md`
- `outputs/user-insights.json`
- `outputs/user-profiles-chart.mmd`
- `outputs/user-lifecycle-chart.mmd`
- `outputs/report.md`

仓库内附带一个示例输出：

- `outputs/test-generic-user-insights.json`

## 使用顺序

推荐先跑：

1. `RTA-DISCOVERY`
2. 人工确认
3. `RTA-USER`

如果已经有高质量逐字稿，也可以直接进入 `RTA-USER`。

## 本地自检

运行：

```bash
python3 scripts/smoke_test.py
```

它会检查：

- 核心文件是否齐全
- 示例 JSON 是否结构正确
- 生命周期是否为固定十阶段
- 每个阶段是否至少有 3 条核心痛点

## 最小安装说明

给你的客户时，只需要告诉他：

1. 下载这个仓库
2. 把整个文件夹放进自己的 Agent / Skill 目录
3. 保持目录结构不要改
4. 使用时先说明自己要走哪种模式：
   - 实时访谈
   - 逐字稿分析
5. 如果前面还没做客户分类，先使用 `RTA-DISCOVERY`

建议客户第一次使用时这样说：

```text
请使用 RTA-USER skill，基于我的业务信息，先帮我完成用户画像和用户生命旅程分析。
如果信息不够，请先补问关键问题，不要直接下结论。
```

## 匿名案例

仓库内附带一份匿名示例成品：

- `outputs/test-anonymized-report.md`
