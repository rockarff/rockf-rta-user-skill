# 输出结构规则

RTA-CONTENT 默认同时输出：

1. Markdown
2. JSON

## JSON 顶层结构

```json
{
  "meta": {},
  "input_snapshot": {},
  "content_judgment": {},
  "content_map": {},
  "generation_record": {},
  "topic_pool": [],
  "selection_gate": {},
  "production_mode": {},
  "deliverables": {},
  "follow_up_questions": [],
  "confidence_notes": []
}
```

## `content_judgment`

至少要有：

- 当前优先用户类型
- 当前优先生命周期阶段
- 当前优先内容类型
- 默认公域内容配比
- 公域重点
- 私域重点
- 判断理由

如果信息足够，建议额外记录：

- `closed_portraits_used`
- `near_close_portraits_used`
- `excluded_portraits_used`
- `portrait_confidence`
- `mother_topic_pool`

## `topic_pool`

每个选题至少要有：

- `topic_title`（短视频选题）
- `interview_question`（访谈提问）
- `user_type`
- `lifecycle_stage`
- `content_type`
- `scene`
- `goal_action`

默认 `content_type` 应使用：

- `broad_traffic`
- `semi_vertical_traffic`
- `trust`
- `conversion`

如果当前轮明确需要私域内容，才额外使用：

- `private_domain`

如果本轮广流量 / 半垂直流量依赖了特定画像，建议每条题额外保留：

- `portrait_basis`
- `mother_topic`
- `topic_source_type`
- `topic_structure`
- `speakability_score`
- `public_content_fit`

可选值例如：

- `closed`
- `near_close`
- `excluded`
- `mixed`
- `inference_only`

`topic_source_type` 建议使用：

- `native_mother_topic`
- `assisted_mother_topic`
- `business_inferred_topic`

## `selection_gate`

必须支持记录：

- 是否已经完成选题确认
- 是否需要辅助框架
- 已选中的题目编号或标题

## `generation_record`

必须支持记录：

- 客户名
- 生成次数
- 本次总题数
- 本次内容比例（默认优先记录：广流量 50 / 半垂直流量 20 / 信任 10 / 转化 10）
- 历史是否已读取
- 本次文档路径

## `production_mode`

必须明确：

- `input_method`
- 为什么这样判断

## `deliverables`

根据输入方式分流。

如果用户要求为已选题生成辅助框架，`deliverables` 里应包含表格化结构。
