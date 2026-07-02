---
name: multi-service-discovery
description: 在 monorepo 或虚拟 monorepo 中识别跨 Spring 微服务 user story 的影响面、服务边界、契约和验证入口。
---

# 多微服务发现 Guide

## 触发

- 一个需求、缺陷或重构可能涉及两个或更多 Spring 服务。
- 用户提到 monorepo、workspace、多个仓库、多个 Deployment、跨服务调用或服务协作。
- 需要判断某个 API、事件、数据库表或业务概念归属哪个服务。

## 目标

先建立可验证的服务影响面，再进入设计或编码。输出必须回答：

1. 哪些服务直接受影响，哪些服务只是间接受影响。
2. 每个服务的职责边界、数据所有权和 Deployment。
3. 涉及哪些 OpenAPI、Pact、事件 schema、数据库 migration 和测试命令。
4. 是否违反“一个业务聚合一个服务一个 Deployment”的默认规则。
5. 下一步应调用哪些 Guide，例如 `api-contract-builder`、`contract-test-builder`、`spring-architecture` 或 `spring-builder`。

## 验收标准

- 已读取根索引：`AGENTS.md`、`workspace-map.md`、`.github/copilot-instructions.md` 或等价文件。
- 已读取所有直接受影响服务的 `SERVICE.md` 或等价上下文文档。
- 已列出服务间调用、事件、共享 schema 和禁止共享项。
- 已区分“需要修改的服务”和“只需要验证兼容性的服务”。
- 已给出最小验证闭环：单服务测试、契约测试、mock server 或 provider verification。
- 不确定边界时，输出缺口和需要人工确认的问题，不直接扩大修改范围。

## 边界

- 不负责直接写业务代码；发现完成后交给 `spring-builder` 或 `bug-fixer`。
- 不负责设计新 API；需要新契约时交给 `api-contract-builder`。
- 不批准服务拆分、数据所有权迁移或同步调用链扩展；这些必须走 ADR。
- 不把全仓搜索结果当作服务边界事实；服务边界以 `workspace-map.md`、`SERVICE.md`、契约、代码和部署事实交叉验证。

## 输出格式

```md
## 多服务影响面

| 服务 | 角色 | 修改类型 | 契约影响 | 数据影响 | 必读文件 |
|---|---|---|---|---|---|

## 协作链路

1. A 服务调用 B 服务：
   - 协议：
   - 契约文件：
   - 失败处理：

## 风险判断

- 服务边界：
- 兼容性：
- 数据所有权：
- 部署/SLO：

## 下一步

- 使用 Guide：
- 必跑验证：
- 需要人工确认：
```

## 按需加载

复杂跨服务任务必须读取 `references/workspace-discovery-playbook.md`。
