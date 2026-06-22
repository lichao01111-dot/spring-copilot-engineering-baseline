# 使用度量改进工程基线

## 启用本地采集

`.baseline/metrics/config.json` 已提供完整可运行示例：

```json
{
  "schema_version": 1,
  "enabled": true,
  "project_key": "example-order-api",
  "retention_days": 90,
  "allow_upload": false,
  "endpoint": "https://metrics.example.internal/engineering-baseline/v1/reports"
}
```

引入真实服务时，必须将 `project_key` 与 `.baseline/project-profile.yaml` 中的 `metrics.project_key` 同步改为不含客户、仓库 URL 或人员信息的稳定内部别名，例如 `order-core-a`。`retention_days` 需符合公司数据保留政策。默认采集已启用，但只保存在本地 Git 忽略文件中；`allow_upload` 默认关闭，即使存在示例 endpoint 也不会访问网络。

`scripts/verify.sh` 与 `scripts/test.sh` 会自动记录成功/失败和粗粒度耗时。其余工作由 Agent 在完成时显式记录：

```bash
printf '%s' '{
  "event_type":"guide_run",
  "name":"spring-builder",
  "outcome":"passed",
  "duration_ms":120000
}' | python3 scripts/record_metric.py --stdin
```

出现失败或阻塞时才附加枚举型 `reason_code`：

```bash
printf '%s' '{"event_type":"agent_review","name":"code-reviewer","outcome":"blocked","reason_code":"MISSING_AUTHORIZATION_TEST","severity":"P1"}' | python3 scripts/record_metric.py --stdin
```

## 查看本地报告

```bash
python3 scripts/metrics_report.py --format markdown
python3 scripts/metrics_report.py --format json --output .baseline/metrics/reports/week-2026-06.json
```

重点观察：Guide/审查使用量、PASS/FAIL/BLOCKED 比例、高频原因码、风险扫描命中、检查中位耗时。不要以单一成功率或耗时作为绩效指标。

## 向内部平台导出

默认不上传。仅在公司完成隐私评审并提供内部 HTTPS 聚合端点后，在 `.baseline/metrics/config.json` 中设置：

```json
{
  "allow_upload": true,
  "endpoint": "https://metrics.company.internal/engineering-baseline/v1/reports"
}
```

然后由 CI Secret 或 OIDC 注入 `BASELINE_METRICS_TOKEN`，显式执行：

```bash
python3 scripts/export_metrics.py --upload
```

该命令只上传聚合报告；配置不完整或端点不是 HTTPS 时会拒绝执行。

## 如何形成改进闭环

1. 每周生成各项目聚合报告。
2. `evolution-runner` 同时读取 `signals.jsonl` 和报告，提出候选改进。
3. 优先修复高频阻塞：补测试/ArchUnit/扫描器/模板通常优于增加提示词。
4. 在一到两个项目试点 2～4 周，比较阻塞率、风险命中和误报。
5. 通过 PR 与 Code Owner 审核后推广；无效规则应退休。
