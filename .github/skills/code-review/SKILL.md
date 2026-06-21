---
name: code-review
description: 在 Java/Spring 变更进入 PR 前进行独立两阶段审查。
---
# 代码审查

## 目标

基于证据判断变更是否正确且具备生产质量。

## 验收标准

使用 `templates/review-report.md`。Stage 1 将每条验收标准映射到实现和测试；Stage 2 检查架构、API 兼容、授权、数据安全、事务/并发、错误处理、可观测性、安全、依赖风险、测试真实性和接口/配置真实性。每条发现都有证据与 P0/P1/P2 级别。

## 边界

必须独立上下文执行，禁止修改文件。Stage 1 有阻断问题时停止。PASS 需要两个阶段都通过且有当前验证证据；没有发现问题不是证据。

执行两阶段审查和真实性检查时按需读取 [两阶段 Java/Spring 代码审查手册](references/review-handbook.md)。
