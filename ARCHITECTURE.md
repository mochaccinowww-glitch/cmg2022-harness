# 从研究问题到可核查的交付

本框架管理的是算例及证据的生命周期。Launcher 或经本机验证的命令行负责提交，CMG 软件负责数值计算，harness 负责版本登记和查找，研究者决定哪些结论可用于下一阶段。

|环节|输入与产物|下载者可如何检查|
|---|---|---|
|研究设计|研究问题、资料来源、合成假设、评价指标和备择解释写入 STUDY.md|读者能说明什么结果会改变原判断|
|算例准备|cases/ID/ 保存输入、依赖、原生文件及 REVIEW.md；派生案记录母体和改动|检查初态、单位、软件版本与 INCLUDE 可移植性|
|计算与复核|在工作副本启动；登记前完成所需输出及日志整理|比较预期和实际末日、警告、关键物衡、实达井控、时空分辨率|
|研究结论|用独立脚本从原生输出复算图表；记录指标、时间窗、分母、反例和适用范围|原生导出、跨案派生图、操作截屏分别标注；复算时可定位输入和脚本|
|版本发布|registry/ID.json 保存逐文件 SHA-256；decisions/角色/序号.json 保存选择理由与前版；HANDOFF.md 记待办|从 current 找回选定交付，再沿 parent 查来源；编号选择记录应纳入私有项目备份或版本控制|

**目录示例。** 框架源码放在工具目录。真实数据放在独立研究目录，维护两者各自的版本和发布范围。

```text
my-study/
  STUDY.md
  HANDOFF.md
  cases/baseline-r1/      # 完整登记单元
  cases/rate-change-r1/   # 新输入与对应输出
  cases/brief-r1/         # 可独立登记的报告、脚本与数据来源说明
  registry/
  decisions/baseline/
  decisions/report/
```

**复算与回退。** 先用 verify 校验母体，把许可范围内的输入依赖复制到新工作目录，再运行。派生案登记时写入 --parent。一个比较涉及多个算例时，在报告的 REVIEW.md 中列全来源 ID、字段和哈希；parent 表示主要派生关系。接纳新基准或回退到旧基准，都用同一角色追加一次 select，填写理由。不直接编辑已发布的算例。哈希验证的是当前文件相对登记清单的一致性；登记目录自身的可信来源依靠项目的访问控制和版本历史。

**成对试验例。** 对每种储层展布分别计算注气与未注气条件下的同期地面累产油量，先求同一展布的增油量，再比较两种展布的增油差。分别核对实际注气量、分层吸气量与实际生效的井控。储层压力响应、地面气体富集、井底游离气到达和低效循环使用各自的证据。若用户研究水驱、热采或其他过程，改用对应的相态、能量或物质平衡及评价量。

**适用范围。** 离线接口不依赖 CMG；本包中的软件核查卡覆盖 WinProp、GEM、Results 与 CMOST。其他求解器可沿用版本与交接接口，原生关键字、输出字段及验收算例需在目标安装上另行验证。登记前冻结算例，避免后台进程继续写入结果。


## 用在自己的工程里

例如，要比较调整采液量前后的产油响应，先把基准算例的输入、包含文件和结果放在同一个算例目录。将新方案登记为它的派生算例，写清调整了哪口井、哪个时段的采液目标。运行后再核对实际产量和生效的井底流压约束。这样，即使两次计算的入口都叫 `case.dat`，也能找回每条曲线对应的文件。

### 命令行试用（Windows PowerShell）

在仓库根目录创建一项研究：

```powershell
python harness.py --project study init
```

在 `study/cases/base-r1/` 放入自己的算例副本及其依赖。以下以入口文件 `case.dat` 为例：

```powershell
python harness.py --project study register base-r1 --entry case.dat --note "Baseline before the rate change"
python harness.py --project study select baseline base-r1 --reason "Reference for the production-rate comparison"
python harness.py --project study current baseline
```

最后一条命令返回当前基准的编号、入口路径和选择理由，并复核文件清单及 SHA-256。若登记后的文件有改动，校验会报出差异。准备新方案时使用新编号，并在登记时用 `--parent base-r1` 记录来源。运行实际模型需要相应的 CMG 安装和许可；求解是否收敛、物质平衡是否满足要求、井控是否切换，需结合原生输出核查。

## 跨会话继续研究

从本版开始，项目内 agent 默认在交付前保存已核实的进展、影响研究的用户反馈和下一步工作。资料按任务分开，例如流体拟合、井控、论文图表。下次说“继续”时先读总览，再读相关主题。普通查询不会生成新记录。这个约定由读取项目说明的 agent 执行；单独操作 Launcher 或 Results 时，可以从命令行手动保存。工具不在后台监控聊天或软件窗口。

```powershell
python harness.py --project study context
python harness.py --project study checkpoint fluid --base 0 --kind feedback --summary "Use the published fitted value for the viscosity comparison." --next "Recompute the comparison table." --evidence STUDY.md
python harness.py --project study context fluid
python harness.py --project study context fluid --history
```

首次保存后版本为 1，下一次更新用 `--base 1`。将证据路径替换为本轮实际核查的文件。案例、角色与主题可分别创建；已有 v0.3 研究直接使用新工具读取，首次保存时自动建立 context/。更新工具时保留原研究目录及历史记录。项目私有 Git 仓库如需跨工作站交接，应一并管理 context/、registry/、decisions/ 和它们引用的证据。

