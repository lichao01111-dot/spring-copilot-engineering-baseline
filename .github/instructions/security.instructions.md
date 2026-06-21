---
applyTo: "**/*.java,**/*.yml,**/*.yaml,**/*.properties,**/pom.xml,**/build.gradle,**/build.gradle.kts"
---
# 安全与隐私规则

- 在服务边界落实认证与授权，不能只依赖 UI 或 Controller 可见性。
- 使用标识符前必须校验、规范化和授权；SQL 必须参数化。
- 禁止记录密钥、Token、凭据、访问头、原始个人数据或完整支付/身份信息。
- URL 获取、文件访问、反序列化、模板、重定向和命令执行都是高风险入口，必须限制与校验输入。
- 新依赖必须说明必要性，通过批准的依赖管理路径固定版本，并通过依赖扫描。

新增入口、外部调用或敏感资产处理时按需读取仓库根目录的 [Spring 服务安全建模与控制标准](../../standards/security-threat-model.md)。
