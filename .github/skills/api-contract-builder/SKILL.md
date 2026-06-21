---
name: api-contract-builder
description: 定义或修改 Java/Spring 服务的 HTTP、事件或跨服务契约。
---
# API 契约构建

## 目标

在实现前明确外部行为与兼容性。

## 验收标准

产出 OpenAPI 或事件契约，定义请求/响应 Schema、校验、认证授权、错误码、幂等语义、分页排序、版本化、示例和兼容性影响，并说明消费者能否独立升级。

## 边界

破坏性变更必须有明确批准和迁移策略。不能将实现类或 JPA Entity 作为公共契约；未实现并测试的端点、事件、配置或错误码不得写入文档宣称支持。

定义 HTTP、事件、错误码或兼容策略时按需读取 [HTTP 与事件契约标准](references/http-api-standard.md)。
