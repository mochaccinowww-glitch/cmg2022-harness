# CMG 2022 Research Harness

给 Codex 一个 CMG 工程目录或一份模型文件，它就能从手头的资料开始核查井控、梳理算例或分析结果。

**[下载并解压](https://github.com/mochaccinowww-glitch/cmg2022-harness/releases/download/v0.4.1/cmg2022-harness-v0.4.1.zip)**，用 Codex 打开含 `AGENTS.md` 的文件夹。把工程路径发给它，或者直接附上文件，说出你想查什么。例如：

> 我的工程在 `D:/CMG/Study01`。帮我找出基准算例，核对注采井的实际控制方式，先别改模型。

> 看一下我附上的 DAT：生产井控制的是产油量还是产液量？如果有最低井底流压限制，也一起列出来。

有 DAT 时可以先读模型设置；要判断哪种控制实际生效，还需要对应的 OUT 或 SR3。换个会话说“继续”，agent 会从已保存的项目记录接着做。

**想在自己的项目里直接用？** 把解压包里的 `skills/cmg2022-harness` 文件夹复制到项目的 `.agents/skills/`，重新打开项目，输入 `$cmg2022-harness` 并附上任务即可。需要完整的命令行记录功能时，保留解压包中的 `harness.py` 和 `templates/`。

[English](README.en.md) · [没有模型？试试离线示例](START_HERE.md) · [命令行与项目管理](ARCHITECTURE.md) · [MIT 许可证](LICENSE)
