# MCI 845 Cluster

用六块 MCI 骁龙 845 核心板组成一个桌面集群。四层底板已完成布线并通过嘉立创 EDA 专业版 v4 的设计规则检查，下一步是首件装配和上电验证。[布线与打样状态](hardware/README.md#fabrication)

## Repository Layout

| Directory | Contents |
| --- | --- |
| [hardware](hardware/) | 集群底板的原理图、PCB 布局和嘉立创 EDA 工程 |
| [hardware/845-coreboard](hardware/845-coreboard/) | [核心板接口定义](hardware/845-coreboard/README.md#core-board-connector)、机械模型和 EDA 库 |
| [hardware/enclosure](hardware/enclosure/) | 开放式打印底座、风扇面板和装配 |
| [hardware/reference-models](hardware/reference-models/) | 供应商 STEP 下载说明和校验值 |
| [software/controller](software/controller/) | Slot 0 上运行的集群管理软件和部署配置 |
| [docs](docs/) | [系统架构](docs/architecture.md)、[组装](docs/assembly.md)和[上电调试](docs/bringup.md) |

## Fabrication and Reproduction

每次送厂打样用 Git 标签记录对应的设计版本，并在 GitHub Releases 附上 Gerber、贴片 BOM、贴片坐标和打印文件。发布说明记录 PCB 修订号、底座版本和验证过的核心板固件版本。

核心板固件和刷机工具见 [mci-845-firmware](https://github.com/saurlax/mci-845-firmware)。集群形态参考 [Sipeed NanoCluster](https://wiki.sipeed.com/hardware/zh/cluster/NanoCluster/index.html)。
