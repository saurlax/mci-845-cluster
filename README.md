# MCI 845 Cluster

用六块 MCI 骁龙 845 核心板组成一个桌面集群。Slot 0 担任管理节点，Slot 1–5 担任工作节点。项目目前处于设计阶段，底板使用嘉立创 EDA 专业版 v4。

## Repository Layout

| Directory | Contents |
| --- | --- |
| [hardware/backplane](hardware/backplane/) | 集群底板的原理图、PCB 布局和嘉立创 EDA 工程 |
| [hardware/845-coreboard](hardware/845-coreboard/) | 核心板机械模型和 EDA 库 |
| [hardware/enclosure](hardware/enclosure/) | 打印底座、集装箱外壳概念和装配 |
| [hardware/reference-models](hardware/reference-models/) | 供应商 STEP 下载说明和校验值 |
| [software/controller](software/controller/) | Slot 0 上运行的集群管理软件和部署配置 |
| [docs](docs/) | [系统架构](docs/architecture.md)、[组装](docs/assembly.md)和[上电调试](docs/bringup.md) |

## Fabrication and Reproduction

每次送厂打样用 Git 标签记录对应的设计版本，并在 GitHub Releases 附上 Gerber、贴片 BOM、贴片坐标和打印文件。发布说明记录 PCB 修订号、外壳版本和验证过的核心板固件版本。

核心板固件和刷机工具见 [mci-845-firmware](https://github.com/saurlax/mci-845-firmware)。核心板背景和集群形态分别参考[骁龙 845 核心板折腾记](https://saurlax.com/blog/mciserver-845)和 [Sipeed NanoCluster](https://wiki.sipeed.com/hardware/zh/cluster/NanoCluster/index.html)。
