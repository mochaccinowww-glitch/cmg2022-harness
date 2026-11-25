---
name: cmg2022-harness
description: Organize and audit local CMG 2022 WinProp, GEM, Results and CMOST studies. Use for case lineage, controlled numerical experiments, history matching evidence, native deliverables and restartable research handoffs.
---

先读当前工程的 AGENTS.md 和上下文入口，通过已登记的编号找到母体。已有项目有自己的接口时沿用它。新项目可使用配套仓库中的 harness.py；单独安装本技能时也可使用项目自己的清单。

接手已有研究时，先从研究者要回答的问题定位基准。配套仓库可用 `current <role>` 找到已选版本和选择理由，未建立角色时再读交接页。用能改变研究决策的观测来选对照，例如相同注气政策下先查各层实注量。参数缺失时记录来源和候选假设。软件求解、工程验收、物理解释与预测标签各自产生证据，按实际完成的部分报告。

修正的结论若进入报告或机器读取接口，把同一版本写回生成源、角色和交接页。历史快照保留。角色选择需有研究者决定或已有授权，执行者不因文件更新日期更晚而自动提升版本。

用户要求“先判断、给我审阅”时，交付假设、可比条件和判据。用户明确说“开始运行”后，在派生目录试算、核查、再运行共同研究时段。要求“停”时记下已完成的算例、尚未核实的结果及恢复位置。用户说“打不开”或“结果里看不到”时，在其指出的具体文件和软件入口复现，分别核对求解器和图形界面。

每轮交付注明母体、修改量、实际运行状态、经验证的物理量和下一项待判问题。面向研究者使用油藏工程名称，算例编号放在名称后。对导师的材料保留能解释选择的数据和图，不夹杂代写建议。

- 使用 WinProp、GEM、Results 或 CMOST 时，按需要读 [软件验收](references/native.md)。
- 设计机理对照、判断历史拟合或准备预测标签时，读 [证据与判据](references/evidence.md)。
- 遇到审阅、追问、返工或版本交接时，读 [沟通与复核实例](references/collaboration.md)。
