# 多微服务 Workspace 发现手册

## 发现顺序

1. 从根目录读取 `AGENTS.md`、`workspace-map.md`、README、`.github/copilot-instructions.md`。
2. 查找服务目录，不通过目录名直接推断职责，必须结合服务文档、启动文件、配置和契约。
3. 对每个候选服务读取：
   - `SERVICE.md` 或等价文档。
   - `pom.xml`/`build.gradle`。
   - `src/main/resources/application*.yml`。
   - `openapi.yaml`、`api.yaml`、`pact/`、`asyncapi.yaml`、`proto/`。
   - migration 目录。
4. 画出调用链：入口 API、内部 client、事件生产/消费、数据库写入。
5. 将服务分成三类：
   - 直接修改：本次必须改代码或配置。
   - 契约验证：不改代码，但必须验证兼容。
   - 背景依赖：只用于理解流程，不纳入本次变更。

## 边界判断

优先使用这些证据：

1. 数据库 migration 和表名归属。
2. OpenAPI/Pact/事件 schema。
3. Controller、Client、Listener、Repository。
4. Deployment、Helm、Kustomize 或 CI 发布配置。
5. 团队 Owner 与值班责任。

低可信证据：

- 过期 README。
- 只有 URL 前缀或包名相似。
- 单个调用点。
- 口头需求中临时提到的服务名。

## 常见错误

- 把“需要验证的服务”误判为“需要修改的服务”。
- 修改 provider 字段但漏改 consumer contract。
- 为了方便跨库 join，直接读其他服务表。
- 将 DTO 包升级成共享业务模型。
- 只启动完整 E2E 环境，不提供可重复的本地契约验证。

## 最小验证矩阵

| 变更类型 | 最小验证 |
|---|---|
| 新增可选响应字段 | provider Web 测试、OpenAPI diff、consumer smoke |
| 删除/改名字段 | 兼容性 ADR、版本化契约、consumer contract 全量验证 |
| 新增同步调用 | client 单测、mock server 测试、超时/重试/降级测试 |
| 新增事件字段 | schema 兼容检查、producer 测试、consumer contract |
| 修改数据所有权 | ADR、migration 测试、回退方案、审查通过 |

## 与其他 Guide 的交接

- 需要新 API：交给 `api-contract-builder`，并附上提供方/调用方/兼容要求。
- 需要契约测试：交给 `contract-test-builder`，并附上协议、契约位置和验证命令。
- 需要拆分或合并服务：交给 `spring-architecture`，必须生成 ADR。
- 需要实现代码：交给 `spring-builder`，并限定每个服务的修改范围。
