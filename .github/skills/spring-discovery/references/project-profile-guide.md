# 项目画像采集手册

`project-profile.yaml` 不是简介，而是后续 Agent 选择命令、测试方式、迁移策略和风险门禁的依据。每个字段都应有仓库证据；无法确认时填 `unknown` 并写出待确认路径，不能根据常见 Spring 项目猜测。

## 必查证据

| 领域 | 读取位置 | 必须记录的事实 |
|---|---|---|
| 构建 | `pom.xml`、`build.gradle*`、wrapper、父 POM | JDK、Spring Boot、依赖 BOM、模块、真实构建/测试命令、插件 |
| 源码布局 | `src/main`、多模块目录、package 依赖 | 分层方式、模块边界、DTO/Entity 放置、异常处理入口 |
| 配置 | `application*.yml`、配置类、部署清单 | profile、配置绑定、密钥来源、端口、健康检查、日志脱敏 |
| 数据 | migration 目录、Entity、Repository、连接配置 | 数据库种类、Flyway/Liquibase、命名策略、审计字段、软删/多租户 |
| 异步 | Kafka/RabbitMQ/Scheduler/Outbox 相关代码 | Topic、消费语义、重试/DLQ、幂等键、顺序和重放风险 |
| API | Controller、OpenAPI、网关、客户端 | 版本策略、认证方式、错误响应、分页、幂等和兼容性约束 |
| 质量 | `src/test`、ArchUnit、CI、扫描配置 | 现有测试层级、容器测试、格式化、静态扫描、覆盖率、阻断门禁 |
| 运行 | Dockerfile、Helm/K8s、监控配置 | 制品类型、启动命令、资源限制、探针、指标、追踪、告警 |
| 度量 | `.baseline/metrics/config.json`、CI Secret 配置 | 匿名 `project_key`、本地/CI 采集、保留期、是否允许内部聚合导出 |

## 画像完成标准

1. 所有 `auto` 命令替换为真实可运行命令，或明确说明当前仓库为何没有该能力。
2. 每个模块的职责和依赖方向可用一句话描述；不允许只列目录。
3. 列出会影响变更安全性的已知限制，例如共享数据库、旧消费者、长事务、批量任务、弱测试覆盖、历史包袱。
4. 变更前重新验证会受影响字段：依赖升级、迁移、CI、发布、消息、权限改动都可能使旧画像失效。
5. 对真实服务，`project-profile.yaml` 中的 `metrics.project_key` 必须与 `metrics/config.json` 保持一致；它是匿名内部别名，不能是仓库 URL、客户名或人员标识。

## 禁止误用

- 看到 `spring-boot-starter-web` 不等于 REST API 已经对外公开；以网关、OpenAPI 和部署边界为准。
- 看到 JPA 不等于允许任意 Schema 变更；以迁移工具和生产数据策略为准。
- 测试存在不等于测试可作为门禁；必须确认 CI 实际运行的任务。
