---
name: spring-architecture
description: 为跨模块、数据模型、集成、事务或安全边界变化做架构决策。
---
# Spring 架构决策

## 目标

选择满足已批准规格且符合现有系统边界的最小架构。

## 验收标准

记录 ADR：背景、方案、决策、影响模块、依赖方向、事务边界、失败/重试、一致性模型、安全边界、可观测性、发布和回滚/前向修复策略。涉及服务边界时，必须同时完成 `templates/service-boundary.md`，列明同一聚合的命令/查询/修改/删除/API、数据所有权和 Deployment 映射。实现计划必须可从 ADR 推导。

## 边界

没有现有组件不足的证据，不引入框架、服务、数据库、消息队列或跨服务依赖。涉及生产拓扑、数据保留、外部集成或新权限的决策需人工批准。

涉及模块、事务、消息或外部依赖时按需读取 [Spring 架构、事务与依赖边界手册](references/spring-architecture-patterns.md)。

涉及服务拆分、读写分离、Worker 或 Kubernetes 工作负载时，必须按需读取仓库根目录的 [服务边界与单 Deployment 规则](../../../standards/service-boundary-and-deployment.md)。
