---
name: spring-discovery
description: 在复杂任务、陌生模块、依赖变更或架构决策前发现 Java/Spring 仓库的真实情况。
---
# Spring 项目发现

## 目标

建立基于事实的项目画像，使后续工作遵循仓库真实约定。

## 验收标准

生成或更新 `.baseline/project-profile.yaml`，覆盖构建工具、JDK/Spring 版本、模块、测试命令、迁移工具、持久化/消息组件、API 约定、CI 门禁与风险；非明显事实必须标注证据路径。未知值明确保留为 `unknown`，不得猜测。

## 边界

默认只读。不修改依赖、配置、代码或构建工具。

复杂项目发现时按需读取 [项目画像采集手册](references/project-profile-guide.md)。
