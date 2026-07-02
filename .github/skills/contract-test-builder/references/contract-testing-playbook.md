# Spring 微服务契约测试手册

## 契约类型选择

| 协议 | 推荐契约 | 适用场景 | 常见验证 |
|---|---|---|---|
| HTTP/REST | OpenAPI + Web 测试，必要时 Pact | 对外 API、服务间同步调用 | OpenAPI diff、mock server、provider Web 测试 |
| Consumer-driven HTTP | Pact | 调用方形态比提供方文档更关键 | consumer pact、provider verification |
| 事件/消息 | AsyncAPI / JSON Schema / Avro / Protobuf | Kafka、RabbitMQ、领域事件 | schema 兼容检查、producer/consumer 测试 |
| gRPC | Protobuf | 强类型 RPC | proto breaking change 检查、stub 测试 |

不要同时引入过多工具。团队已经有 OpenAPI 时，先把 OpenAPI 变成 mock 和测试来源；只有调用方差异明显或多消费者复杂时，再引入 Pact。

## OpenAPI 验证闭环

推荐最小闭环：

1. Provider 维护 `openapi.yaml`。
2. Provider 的 Controller/Web 测试验证响应符合 OpenAPI 的字段、状态码和错误结构。
3. Consumer 使用 OpenAPI 生成 stub/mock server 或 client，并用 client 测试验证调用参数。
4. CI 运行 OpenAPI breaking-change 检查。

PR 中必须说明：

- 新增字段是否可选。
- 删除、改名、类型变化是否破坏兼容。
- 错误码是否稳定。
- 分页、排序、幂等 key、trace id 是否保持语义。

## Pact 验证闭环

适用条件：

- 多个 consumer 对同一 provider 有不同调用形态。
- provider 文档经常滞后于实际使用。
- 需要由 consumer 定义“我真正依赖的协议”。

最小流程：

1. Consumer 测试生成 pact 文件。
2. Pact 文件进入仓库或内部 broker。
3. Provider 在 CI 中执行 provider verification。
4. Verification 失败时，provider 不能合并破坏兼容的变更。

注意：

- Pact 不是端到端测试，不验证完整业务流程。
- Provider state 必须可重复准备，不依赖生产数据。
- Consumer 不应把无关字段写进契约，避免过度耦合。

## Mock server 规则

mock 必须从契约生成或受契约约束，不能手写随意响应。

可接受：

- OpenAPI mock server。
- WireMock stub 从契约/测试生成。
- Pact mock server。
- Testcontainers 启动依赖服务的轻量版本。

不可接受：

- 在测试中硬编码一个永远 200 的假 client。
- mock 返回结构和 OpenAPI 不一致。
- 只 mock 成功路径。

## 兼容性判断

通常兼容：

- 新增可选响应字段。
- 新增可选请求字段且有默认值。
- 新增错误码但旧错误码仍保留。
- 新增事件字段且 consumer 忽略未知字段。

通常破坏：

- 删除或重命名字段。
- 改变字段类型、枚举含义或单位。
- 必填字段新增。
- 状态码语义变化。
- 事件 topic、key、幂等语义变化。

破坏性变更必须有版本策略，例如 `/v2`、新 topic、双写双读窗口、灰度开关或 consumer 迁移清单。

## PR 证据清单

- 契约文件 diff。
- 调用方测试输出。
- 提供方验证输出。
- mock server/stub 来源。
- 兼容性判断。
- 如果无法运行某类验证，说明阻塞原因和替代证据。
