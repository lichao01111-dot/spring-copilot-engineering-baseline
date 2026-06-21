# Java/Spring 可读性与实战编码规范

## 目标

代码的首要读者是未来维护它的人，其次才是编译器。规范的目标是让一个熟悉业务但不熟悉当前实现的工程师，能在短时间内回答：这个类负责什么、数据从哪里来、业务规则在哪里、失败会怎样、如何验证。

本标准不追求“最少行数”或“所有地方都抽象”。判断依据是：职责是否单一、名字是否表达意图、控制流是否容易追踪、异常与副作用是否显式、同类代码是否一致。

## 1. 包、模块与类

优先按业务能力/聚合组织，再在能力内部按接口、应用、领域、基础设施分层；避免全项目堆积为 `controller`、`service`、`repository` 三个超大包。

```text
com.company.order
├── api/                 # HTTP DTO、Controller、错误映射
├── application/         # 用例、事务、命令/查询
├── domain/              # 聚合、值对象、业务规则
├── infrastructure/      # JPA、消息、外部客户端
└── support/             # 仅该能力内部共享的技术辅助
```

类名描述角色和业务含义：`OrderConfirmationService`、`CancelOrderCommand`、`OrderSummaryResponse`、`JpaOrderRepository`。避免 `OrderServiceImpl`、`CommonUtils`、`BaseManager`、`Helper`、`Processor` 这类无法表明职责的名称。

一个类可以有多个紧密相关方法；当它同时承担 HTTP、事务编排、SQL、远程调用和领域规则，或方法之间只共享字段而没有共同业务职责时，才需要拆分。不要为每个十行方法都创建接口、Factory、Builder 或 `XxxImpl`。

## 2. 方法与控制流

方法名称使用业务动词，返回值体现结果：`confirmOrder`、`findActiveSubscription`、`calculatePayableAmount`。布尔方法以 `is/has/can/should` 开头。参数超过 3 个且不是自然组合时，使用命令对象或值对象。

优先使用早返回降低嵌套，但不要把核心流程切碎为大量只能读懂名字的私有方法。一个方法出现以下信号时需要重构：同时有多个业务阶段、嵌套超过两层且无法用 guard clause 表达、重复的错误处理、难以命名的布尔参数、无法用一句话说明副作用。

```java
// 不推荐：条件与副作用混在一起，失败语义不清
public void confirm(Long orderId, Long userId) {
    Order order = repository.findById(orderId).orElse(null);
    if (order != null) {
        if (order.getBuyerId().equals(userId)) {
            if (order.getStatus() == DRAFT) {
                order.setStatus(CONFIRMED);
                repository.save(order);
            }
        }
    }
}

// 推荐：读取、授权、不变量、状态变化和副作用顺序可见
@Transactional
public OrderConfirmationResult confirmOrder(ConfirmOrderCommand command, Actor actor) {
    Order order = orderRepository.getRequired(command.orderId());
    orderAccess.assertCanConfirm(actor, order);
    order.confirm(clock.instant());
    auditPublisher.publishOrderConfirmed(order);
    return OrderConfirmationResult.from(order);
}
```

## 3. DTO、Entity 与领域对象

- API 请求/响应使用不可变 DTO（优先 `record`，除非框架/兼容性要求可变对象）。字段名贴近 API 契约，不直接复用 Entity。
- Entity 只承载持久化映射和聚合内部状态；状态改变通过有业务含义的方法完成，例如 `order.cancel(reason)`，而不是散落的 `setStatus`。
- 值对象表达金额、邮箱、订单号、日期区间、枚举组合等概念；只在它真正封装校验或语义时创建，不能把每个 `String` 都包装成类。
- Mapper 只做数据转换，不做权限、数据库查询、远程调用或隐藏业务决策。
- 删除默认优先明确业务语义：取消、归档、失效、软删或硬删。`DELETE` 不是自动等价于物理删库。

## 4. 异常、返回值与 Optional

业务失败应使用稳定业务码和可预期异常/结果；基础设施异常保留根因并在统一边界映射。禁止捕获 `Exception` 后返回 `null`、空集合或 `false` 掩盖错误。

`Optional` 仅用于表达“查询结果可能不存在”的返回值；不要作为字段、方法参数、DTO/JPA Entity 字段，也不要通过 `optional.get()` 把语义重新隐藏。

```java
public Order getRequired(OrderId id) {
    return repository.findById(id)
            .orElseThrow(() -> new BusinessException(OrderError.ORDER_NOT_FOUND, id));
}
```

集合应尽量返回空集合而非 `null`；但“没有结果”和“请求无效/依赖失败”必须用不同的错误语义表达。

## 5. Spring、事务与依赖注入

- 构造器注入是默认方式；依赖字段应是 `final`。禁止 field injection，除非遗留框架限制且有说明。
- `@Transactional` 放应用服务的 public 用例方法。避免自调用事务、长事务中远程 HTTP、在事务中执行大文件/批量循环。
- Controller 只做协议转换；应用服务编排；领域对象维护不变量；Repository 访问数据；Adapter 处理外部系统。
- `@Async`、定时任务和消息监听器必须明确线程池/消费者组、超时、重试、幂等和 trace 传播，不能只是加注解。
- 配置集中在 `@ConfigurationProperties`，具备校验和文档化默认值；业务代码中避免散落 `@Value`。

## 6. 集合、Stream、并发与性能

Stream 适合无副作用的 map/filter/collect。涉及异常处理、早停、复杂分支、外部调用、状态更新或调试困难时，普通 `for` 循环更可读。

```java
// 推荐 Stream：纯转换
return orders.stream().map(OrderSummary::from).toList();

// 推荐 for：控制副作用、失败和顺序
for (Order order : orders) {
    try {
        notificationSender.send(order);
    } catch (RetryableException exception) {
        retryQueue.enqueue(order.id());
    }
}
```

禁止在循环中隐式执行数据库查询或远程调用而不评估数据量。集合处理必须明确最大数量、分页/批次、排序和超时。并发控制优先使用数据库唯一约束、乐观锁、幂等键和明确队列语义，不依赖 JVM 内存锁解决分布式问题。

## 7. 日志、注释与 TODO

日志记录事件和上下文，不重复记录“进入方法”。错误日志包含业务键、操作、结果、关联 ID 和异常；字段必须脱敏。注释解释“为什么”，而不是翻译代码；复杂业务规则、兼容性、反直觉性能取舍和外部约束应写注释或 ADR。

`TODO` 必须包含跟踪编号或移除条件，例如 `TODO(ORDER-421): 在旧客户端停止调用后删除双写逻辑`。禁止没有责任人和清理条件的 TODO/FIXME。

## 8. Lombok 与格式化

- 可以使用 `@RequiredArgsConstructor`、`@Getter`、`@Builder`（用于构造复杂 DTO/测试数据）以减少样板代码。
- Entity 不使用无约束的 `@Data`：它会生成不受控 setter、`equals/hashCode/toString`，容易触发 JPA 代理、循环引用和敏感字段泄露问题。
- 格式化交给 Spotless + Google Java Format 或团队统一 formatter；开发者不应为缩进、换行、import 排序争论。
- 静态分析优先捕获空值、资源泄露、危险 API、依赖漏洞和架构依赖；建议使用 Error Prone/SpotBugs、ArchUnit、依赖扫描。工具规则必须先在试点验证误报。

## 9. 审查触发信号

下列情况不一定是错误，但必须在审查中说明：超过一个聚合的事务；新增通用基类；新增静态可变状态；原生 SQL；反射；`@SuppressWarnings`；`catch (Exception)`；`@Async`；新线程池；缓存；重试；Feature Flag；跨服务调用；删除/迁移；绕过权限检查。
