---
name: contract-test-builder
description: 为 Spring 微服务间 HTTP、事件或消息协作建立 OpenAPI/Pact/mock server/provider verification 验证闭环。
---

# 契约测试 Guide

## 触发

- 修改服务间 HTTP API、事件、消息、错误码、DTO 字段或兼容策略。
- 新增或调整 OpenAPI、Pact、AsyncAPI、Proto、JSON Schema。
- 一个服务依赖另一个服务，但本地无法稳定启动完整集成环境。
- PR 需要证明调用方和提供方没有协议漂移。

## 目标

把服务间协作从“文档约定”变成“可执行验证”。完成后应形成：

1. 机器可读契约：OpenAPI、Pact、AsyncAPI、Proto 或 JSON Schema。
2. 调用方验证：mock server、stub、consumer contract 或 client 测试。
3. 提供方验证：provider verification、Web 测试或 schema 兼容检查。
4. CI/本地命令：能重复运行，失败信息能指向具体字段、状态码或事件。
5. PR 证据：契约变更、实现变更和测试输出在同一个变更单元内可追踪。

## 验收标准

- 已说明契约类型、契约文件路径、调用方、提供方和兼容方向。
- 破坏性变更有版本策略、迁移窗口和 ADR。
- mock server/stub 来源于契约文件，不手写不受控假响应。
- 契约测试覆盖成功、校验失败、权限失败、幂等/重试或超时中的关键路径。
- Provider 验证不依赖线上真实服务。
- 输出真实验证命令；无法运行时说明缺失依赖和替代证据。

## 边界

- 不把契约测试当作完整业务测试；业务不变量仍由单元/集成测试覆盖。
- 不批准破坏兼容性；破坏性变更必须走 ADR、版本化和人工确认。
- 不在契约中暴露密钥、真实用户数据或生产 endpoint。
- 不为了让测试通过而降低协议语义，例如把必填字段改成全可选。

## 推荐流程

1. 读取 `workspace-map.md` 和相关服务 `SERVICE.md`。
2. 确认协议类型：HTTP、事件、队列、gRPC 或文件。
3. 找到当前契约和调用代码，判断是新增、兼容扩展还是破坏变更。
4. 先改契约，再改调用方/提供方实现。
5. 生成或更新 mock server/stub/provider verification。
6. 运行验证命令并记录输出。
7. 若失败，优先修复契约和实现不一致，而不是放宽断言。

## 输出格式

````md
## 契约变更摘要

| 调用方 | 提供方 | 协议 | 契约文件 | 兼容性 |
|---|---|---|---|---|

## 验证闭环

- 调用方验证：
- 提供方验证：
- mock/stub 来源：
- CI 接入建议：

## 风险

- 破坏性变更：
- 数据/隐私：
- 运行时失败模式：

## 实际命令

```sh

```
````

## 按需加载

复杂契约变更必须读取 `references/contract-testing-playbook.md`。
