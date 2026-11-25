# CMG 2022 Research Harness

**v0.3.0 · [English quick start](README.en.md) · [零基础入门](START_HERE.md) · [工程架构](ARCHITECTURE.md)**

用于 WinProp、GEM、Results 和 CMOST 数值模拟研究的轻量工程模板。它解决一个常见的交接问题：拿到一张图之后，怎样找到当时的输入、实际运行结果、对照母体和验收记录。包含一个可独立安装的 agent skill，以及只依赖 Python 标准库的本地文件登记工具。两者可以单独使用。

## 第一次使用

完整解压，用 Codex 打开含 AGENTS.md 的目录，发送 **开始**。工程内置 skill、已登记的教学算例、选择理由和研究记录。第一次无需复制技能或编写配置。在终端也可运行 `python start.py`，预期为 daily-r1、校验 1 个文件、三天累计地面油量 12.6 m³。详见[新手指南](START_HERE.md)。

## 命令行试用（Windows PowerShell）

在本仓库根目录执行，使用 Python 3.10 或以上版本。推荐本地工作盘。Linux 和 macOS 的登记目录需支持硬链接。仓库和工作路径建议使用 ASCII 字符，便于跨版本复用。

```powershell
python harness.py --project demo init
New-Item -ItemType Directory demo/cases/baseline
Copy-Item examples/offline/daily.csv demo/cases/baseline/
python harness.py --project demo register baseline --entry daily.csv --note "Offline synthetic fixture"
python harness.py --project demo resolve baseline
python harness.py --project demo verify baseline
python harness.py --project demo select baseline baseline --reason "Offline walkthrough only"
python harness.py --project demo current baseline
python -m unittest discover -s tests -v
```

verify 应返回 verified=baseline 和 files=1。示例中的三行数据为手工构造，只演示交接接口。登记需要一个新 ID，重复登记会报错。resolve 返回本机的绝对入口路径，verify 会检查整个算例目录有无增删和内容变更。

## 接入一个真实研究

从空目录开始用 `python harness.py --project study init`。初始化会生成设计页、交接页和目录。已有项目可以继续按原布局工作，登记接口沿用 v0.1 的格式。

**日常查询。** `resolve ID` 读某个固定版本的位置；`current ROLE` 读研究者选定的当前版本、选择日期和理由，同时重新校验其内容。比如先登记报告，再用 `select report brief-r1 --reason "Reviewed against native well totals"` 把它设为当前报告。选择历史位于 decisions/report。默认返回 JSON，可由 CI、笔记本或其他 agent 读取；文件有漂移时 current 返回非零。初始示例中的 baseline 既是角色名也是首个算例 ID，实际项目可以使用不同名称。

1. 在独立工作目录中建立 cases/<id>/。将该版本应一起交付的文件放在此处，包括外部 INCLUDE、流体、日程和结果；按输入的相对引用保留子目录结构。外部绝对引用需在副本上改为可迁移路径，并用软件重新打开核查。工具对目录文件做哈希，不自动解析 CMG 依赖语法。
2. 先用正在研究的正版安装确认小算例可以运行。记录完整版本、模拟单位、初态、启动参数和预期末日。在新目录中使用 Launcher 提交，或在已验证 CLI 的 GEM 2022.10 工作站使用以下等价形式（在算例目录执行，环境变量 CMG_GEM_EXE 指向本地可执行文件）。进程结束后核查 OUT、SR3 和实际井控。

```powershell
& $env:CMG_GEM_EXE -f case.dat -parasol 4 -doms *> console.log
$LASTEXITCODE
```

3. 复制 templates/REVIEW.md 到算例目录，填入工程验收和物理验收，再登记，例如 `python harness.py --project study register matrix-injection --entry case.dat --note "Matrix injection case; review in REVIEW.md"`。如输入和结果需分别冻结，可按两个 ID 登记并用 --parent 关联。登记可用于准备好但尚未运行的输入，具体状态填在 REVIEW.md。
4. 对照算例使用新目录，复用经过 verify 的母体输入，清除复制来的历史结果，运行之前确保目标目录里没有旧 OUT/SR3。写明输入差异，在登记命令末尾增加 `--parent matrix-injection`。父 ID 只表达谱系，父子是否只差一个因素仍需核对。算例登记完成后，后续报告或新图存入独立批次目录。
5. 将 templates/HANDOFF.md 放在研究根目录作为当前入口。每次更换基准时登记旧 ID、新 ID、选择理由和证据。下一位协作者从该入口 resolve、verify，优先复用已有合格结果。登记文件保存在 registry/<id>.json；清单及哈希支持复核，清单本身应纳入项目版本管理。JSON 输出成功退出码为 0，错误返回非零。

## 安装 skill

将 skills/cmg2022-harness 整个目录复制到个人 Codex skills 路径，或项目的 .agents/skills/ 下。下次会话可用 `$cmg2022-harness` 指定它。例如：

> 读取交接记录，核验当前母体。设计一组相同初态、相同注气政策的成对数值试验，明确实际剂量、压力约束和井组增油的评价方式。先交方案给我审阅。

> 按已批准的方案运行短试。验证井控和终止日后跑全期，已有结果通过校验的直接复用。原生图和计算所得的差值图分别标注。暂停时把最后完成的案例和恢复命令写回交接记录。

## 仓库内容与发布范围

- harness.py、tests/ 为注册、定位、校验接口和回归测试。
- templates/ 提供研究交接和单案验收记录。
- skills/cmg2022-harness/references/ 提供四种软件的验收要点和科学证据口径。
- examples/offline/ 可离线试用。真实模拟另需自行安装和授权的 CMG。工具不包含求解器、商业示例、现场模型、原论文图表或历史结果，不承诺跨版本二进制兼容。

本仓库采用 MIT 许可证，许可范围为本项目原创代码和文档。CMG 产品名称用于说明兼容目标，本项目为独立社区模板。向公开仓库提交时以本发行包为起点；真实工程的运行目录和许可证留在私有项目中。

## 维护与 GitHub 发布

把发行 ZIP 解压到独立目录，在含本 README、LICENSE 和 .github 的目录初始化 Git 仓库。首次提交前查看 `git status --short` 和暂存文件清单。公开目录只维护框架源码、skill、模板、演示和测试。把个人研究、外部软件或未授权资料保存在独立工程根目录；仅凭扩展名过滤无法判定 CSV、图片或文本是否可以公开。仓库中的工作流在 GitHub 的 Windows、Linux、macOS runner 上执行离线测试，实际执行结果由 Actions 给出。发布者可把 v0.3.0 源包附在同名 Release。
