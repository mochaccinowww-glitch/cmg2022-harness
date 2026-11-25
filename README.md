# CMG 2022 Research Harness

一个用于 CMG 油藏数值模拟的项目模板。做完一组算例，你可以给基准模型和每个派生算例分配固定编号，记录改过哪些输入，再从报告追溯到对应的 DAT、OUT 和 SR3。交给同事时，对方可以查到当前采用的版本、选择理由，以及还有哪项结论需要验证。

[English](README.en.md) · [下载 v0.3.0](https://github.com/mochaccinowww-glitch/cmg2022-harness/releases/download/v0.3.0/cmg2022-harness-v0.3.0.zip) · [新手指南](START_HERE.md)

## 先跑一个例子

准备 **Python 3.10 或更高版本**，下载 ZIP 并完整解压。打开同时包含 `AGENTS.md` 和 `start.py` 的文件夹。示例只用 Python 标准库，离线即可运行，无需安装 CMG 或第三方 Python 包。

- **使用 Codex**：把这个文件夹作为项目打开，发送 **开始**。根目录的项目说明会引导 Codex 使用随包的 skill 并运行示例。
- **使用终端**：在同一目录执行 `python start.py`。如果系统的 Python 3 命令是 `python3`，请使用 `python3 start.py`。

示例包含三个完整日的地面平均产油量，分别为 4.1、4.3 和 4.2 m³/d。程序先校验已登记的数据文件，再计算累产油量。输出中应看到 `case` 为 `daily-r1`、`days` 为 `3`、`cumulative_surface_oil_m3` 为 **12.6**。这些数值来自随包的教学 CSV。可以打开[原始数据](examples/starter/cases/daily-r1/daily.csv)复算，也可以在[交接记录](examples/starter/HANDOFF.md)中查看解释。

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

## 按需查阅

| 想做什么 | 从哪里开始 |
|---|---|
| 设计一组有明确对照的数值试验 | [研究设计模板](templates/STUDY.md) |
| 记录一个假设如何通过算例检验 | [研究记录](templates/RESEARCH_LOG.md) |
| 核对流体文件、求解日志、Results 图件或 CMOST 结果 | [原生软件核查说明](skills/cmg2022-harness/references/native.md) |
| 暂停项目，留给下次或另一位研究者接手 | [交接模板](templates/HANDOFF.md) |
| 将 skill 用于已有工程，或了解文件如何组织 | [新手指南](START_HERE.md) · [工程架构](ARCHITECTURE.md) |

本项目由社区独立维护，代码与文档采用 [MIT 许可证](LICENSE)。仓库提供研究管理工具和合成教学数据；CMG 软件、商业算例及现场资料由使用者自行准备。
