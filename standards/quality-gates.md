# 质量门禁

| 门禁 | 权威来源 | 触发条件 | 失败处理 |
|---|---|---|---|
| 基线结构 | `scripts/validate_baseline.py` | 每个 PR | 阻断 |
| 编译 | Maven/Gradle | 任意 Java 构建变更 | 阻断 |
| 单元测试 | Maven/Gradle | 任意行为变更 | 阻断 |
| 格式化与基础静态检查 | Spotless/团队 formatter、Error Prone/SpotBugs/Checkstyle（按项目选择） | 任意 Java 变更 | 阻断；规则先试点 |
| 集成测试 | Testcontainers 或批准方案 | DB、消息、安全或 Spring 集成变更 | 阻断 |
| 架构测试 | ArchUnit 或批准方案 | 模块/依赖变更 | 阻断 |
| API 兼容性 | 契约检查 | 对外契约变更 | 阻断 |
| 迁移验证 | 迁移工具与集成测试 | Schema/数据变更 | 阻断 |
| 依赖安全 | 批准扫描器 | 依赖变更与发布 | 高危/严重阻断 |
| Java 高风险用法 | `scripts/security_preflight.py` | 任意 Java 变更 | 未批准 `SEC-*` 用法阻断 |
| 性能风险 | `scripts/performance_preflight.py` + 容量评估 | 查询、导出、异步、缓存、外部调用、批处理变更 | CI 严格模式下未批准 `PERF-*` 用法阻断 |
| 独立审查 | `code-review` Guide | 代码变更 | PASS 前阻断 |
| 服务边界审查 | 服务边界模板 + ADR | 新服务、跨服务 CRUD、读写拆分、独立 Worker/Deployment | 未证明例外时阻断 |

覆盖率是趋势与关键模块控制项，不是全仓库的表面 KPI。全绿测试不能弥补缺少验收标准、未审查迁移风险或缺失安全门禁。
