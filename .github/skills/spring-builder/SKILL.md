---
name: spring-builder
description: 在保留当前验证证据的前提下实现已批准的 Java/Spring 开发阶段。
---
# Spring 开发

## 目标

交付已接受的变更，同时保持仓库约定、兼容性与可测试性。

## 验收标准

所有已接受行为均已实现，相关测试、配置和文档同步更新。代码遵守模块边界、DTO/API、校验、授权、事务、结构化日志和错误处理规则。对于同一聚合，命令、查询、修改和删除必须保持在其所有者服务内；跨服务只能走公开 API 或事件。涉及 API、数据、异步、外部调用、文件/URL、缓存、批处理、依赖或配置时，完成说明必须附 `templates/security-performance-assessment.md` 的相关证据，以及本次风险扫描结果。

## 边界

删除或重命名共享代码前先评估影响；新增依赖或抽象前优先复用现有组件。不得无说明扩大范围，也不得自我审批；代码变更后必须独立审查。

涉及分层、JPA、事务、日志、异常或测试分层时按需读取 [Java/Spring 实现手册](references/implementation-playbook.md)。

所有 Java 实现的命名、控制流、DTO/Entity、Optional、Stream、Lombok 与注释规则以仓库根目录的 [Java/Spring 可读性与实战编码规范](../../../standards/java-readability-and-conventions.md) 为准。

安全和性能验收以仓库根目录的 [安全与性能完成门禁](../../../standards/security-and-performance-gates.md) 为准。
