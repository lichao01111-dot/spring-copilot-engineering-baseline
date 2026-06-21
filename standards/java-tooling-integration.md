# Java 规范的构建工具接入策略

可读性标准必须同时具备“自动格式化”和“人工语义审查”。不要把缩进、换行、import 顺序交给人审；也不要让 Checkstyle 替代业务、事务和安全审查。

## 推荐分工

| 工具类别 | 解决的问题 | CI 策略 |
|---|---|---|
| Formatter（Spotless + 团队 formatter） | 缩进、空格、换行、import、文件结尾 | 必须阻断，可自动修复 |
| 编译器/Enforcer | JDK、依赖版本、重复类、编译警告 | 必须阻断 |
| Error Prone / SpotBugs | 空值、资源泄露、错误 equals、并发和危险 API | 先警告试点，再选择性阻断 |
| ArchUnit | 分层与模块依赖、Controller/Repository 越界 | 对新变更阻断 |
| 测试与覆盖率 | 行为回归、关键路径趋势 | 测试阻断，覆盖率按关键模块 |
| 依赖扫描 | CVE、许可证、过期依赖 | 高危/严重阻断 |

所有插件版本由公司的父 POM、Version Catalog 或内部构建平台统一管理。业务项目不能各自随意升级 formatter 或静态分析规则，避免同一仓库在不同开发机上产生不同 diff。

## Maven 示例

以下片段用于说明职责；版本、仓库、许可证和规则路径由团队统一父 POM 提供。

```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <configuration>
    <java>
      <googleJavaFormat />
      <removeUnusedImports />
      <importOrder />
    </java>
  </configuration>
  <executions>
    <execution>
      <goals><goal>check</goal></goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>
```

开发者本地可运行 `mvn spotless:apply` 修复格式；CI 只运行 `spotless:check`，不能在 CI 自动改写提交。父 POM 还应统一 JDK Enforcer、Surefire/Failsafe、JaCoCo、依赖扫描及必要的静态分析插件。

## Gradle 示例

```kotlin
plugins {
    id("com.diffplug.spotless")
}

spotless {
    java {
        googleJavaFormat()
        removeUnusedImports()
        importOrder()
    }
}

tasks.check {
    dependsOn(tasks.spotlessCheck)
}
```

开发者本地运行 `./gradlew spotlessApply`；PR 运行 `./gradlew check test`。将静态分析、ArchUnit、Testcontainers 和依赖扫描纳入 `check` 或明确 CI job，不能只在某个人本地执行。

## ArchUnit 最小规则示例

```java
@AnalyzeClasses(packages = "com.company")
class ArchitectureTest {
    @ArchTest
    static final ArchRule controllersDoNotAccessRepositories =
            noClasses().that().resideInAPackage("..api..")
                    .should().dependOnClassesThat().resideInAPackage("..infrastructure.persistence..");
}
```

规则应从最关键、争议最少的边界开始：Controller 不直连 Repository、领域层不依赖 Spring/JPA/HTTP、跨服务不能共享 Entity。不要一开始用数十条复杂命名正则让团队疲于修规则。

## 推广顺序

1. 先启用 `.editorconfig` 和 Formatter，统一无争议的格式。
2. 把已有编译、测试和基础依赖扫描稳定放入 CI。
3. 用 ArchUnit 固化两到三条关键架构边界。
4. 以告警模式试点 Error Prone/SpotBugs，记录误报后再阻断。
5. 每季度清理失效规则，不把历史风格偏好永久固化为工程成本。
