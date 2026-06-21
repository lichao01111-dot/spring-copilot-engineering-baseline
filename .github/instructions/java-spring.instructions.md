---
applyTo: "**/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts,**/application*.yml,**/application*.yaml,**/application*.properties"
---
# Java 与 Spring 规则

- 先读取项目画像，再确定 JDK、构建工具、Spring Boot、数据库和模块布局。
- Controller 只处理 HTTP；应用服务承载用例和事务边界；领域层承载规则；Repository/Adapter 处理持久化与外部系统。
- Controller 只使用请求/响应 DTO，不暴露 JPA Entity 或持久化异常。
- 所有外部输入必须使用 Bean Validation，并映射为项目标准错误响应，保留关联 ID。
- `@Transactional` 位于服务/用例边界；非默认传播或隔离级别必须说明原因。
- 避免 N+1、无界查询、意外 eager load 和实体图泄漏；可能增长的集合必须分页和稳定排序。
- 新配置必须有文档化默认值，且不得降低生产安全性；绝不提交真实凭据。
- 除非已有批准的破坏性变更，外部 API 必须向后兼容。
- 面向维护者写代码：业务能力优先于技术层大包；避免 `XxxServiceImpl`、`CommonUtils`、field injection、裸 `null`、无约束 `@Data` 和无业务语义的 setter。
- 纯转换可以使用 Stream；有副作用、异常、早停、远程调用或复杂分支时使用普通循环，保持控制流可读。

新增关键用例、异步流程或性能敏感路径时按需读取仓库根目录的 [可观测性、性能与 SLO 标准](../../standards/observability-and-slo.md)。

所有 Java 代码修改都按需读取仓库根目录的 [Java/Spring 可读性与实战编码规范](../../standards/java-readability-and-conventions.md)。
