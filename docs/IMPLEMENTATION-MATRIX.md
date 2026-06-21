# 设计实现映射

| 设计项 | 实现工件 | 验证方式 |
|---|---|---|
| 全局指令与安全边界 | `.github/copilot-instructions.md` | 结构校验 |
| 专项规范 | `.github/instructions/` | 结构校验 |
| 11 个 Guide 与深度手册 | `.github/skills/*/SKILL.md`、各 `references/` | 校验数量、front matter、中文目标/验收/边界标题及每个 Guide 的按需参考 |
| 3 个隔离 Agent | `.github/agents/` | 结构校验 |
| 规格、状态、计划、审查、迁移、发布与 Goal | `templates/`、`.baseline/task-state/` | 真实任务创建工件并由审查引用 |
| 两阶段审查 | `code-review`、`code-reviewer`、审查模板 | 每个代码变更生成独立报告 |
| 构建、测试、密钥检查 | `scripts/verify.sh`、`test.sh`、`scan_secrets.py` | 真实项目调用 Maven/Gradle |
| Hook 与 CI | `.baseline/hooks/`、`.github/workflows/` | 不含自动推送/部署副作用 |
| 演进与治理 | `record_signal.py`、`evolution-engine`、`governance.md` | 信号字段受限，规则走 PR/Code Owner |
| 深度工程标准 | `standards/security-threat-model.md`、`testing-strategy.md`、`observability-and-slo.md` | Agent 按路径/任务按需加载，并在审查报告中引用 |
| Java 代码可读性与规范 | `.editorconfig`、`standards/java-readability-and-conventions.md`、Java 路径指令 | 开发和两阶段审查共同执行；格式化/静态分析由项目构建接入 |
| 服务边界与部署模型 | `standards/service-boundary-and-deployment.md`、`templates/service-boundary.md` | 架构/计划/审查 Guide 强制核查聚合、数据所有权与 Deployment 映射 |

## 试点前必须本地化

项目画像中的版本、构建/测试命令、企业扫描器、测试容器、Code Owner、分支保护、发布审批、异常响应、OpenAPI、日志脱敏、追踪和认证规范都必须基于真实仓库填写。模板 CI 不是生产质量证明。
