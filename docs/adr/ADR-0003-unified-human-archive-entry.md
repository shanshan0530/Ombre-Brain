# ADR-0003: 统一人类归档入口

## Decision

Dashboard 对普通记忆桶只展示一个「归档」按钮。人类点击后必须填写理由，提交既有
AI 删除审批。审批通过后执行 delete-to-archive：Markdown 文件移入 `archive/`，并写入
`deleted_at`；不会物理抹除文件。

底层两种生命周期操作继续存在且语义不变：`bucket_mgr.delete()` 表示带删除标记的归档，
`bucket_mgr.archive()` 表示不带删除标记的普通归档。AI、自动衰减和其他系统生命周期逻辑
仍可使用后者。兼容的 HTTP DELETE 端点继续保留，但 Dashboard 不再并列展示第二个人类
按钮。

## Rationale

此前 Dashboard 同时展示「归档」和「删除到档案」，两者都要求人类理由、都进入相同 AI
审批，却在批准后产生不同元数据。这让用户难以理解该选哪个，也造成两套近乎重复的交互。
人类表达的是“我希望这条记忆退出活跃记忆”，系统仍应保留决定是否批准的边界；批准后的
删除标记则保留更明确的审计足迹。

## Boundaries

- 不改变 AI 对普通桶的归档能力。
- 不改变自动衰减和底层 `archive()` 的行为。
- 不增加物理删除能力。
- 不改变 Letter、导入审核或可擦除测试桶各自已有的专用边界。
- 不移除兼容 API，只收敛 Dashboard 普通桶的人类入口。

## Tests required

Web 路径测试必须证明单桶与批量人类「归档」都记录为 `action="delete"`，且批准前不移动
文件；可擦除测试桶继续直接执行但也走 delete-to-archive。Dashboard 回归测试必须证明
普通桶详情只保留「归档」按钮，不再调用 `bucketDelete()`。
