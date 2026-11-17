# MCI 845 Cluster

用六块 MCI 骁龙 845 核心板组成一个桌面集群。Slot 0 担任管理节点，Slot 1–5 担任工作节点。项目目前处于设计阶段，底板使用嘉立创 EDA 专业版 v4。

## Repository Layout

| Directory | Contents |
| --- | --- |
| [hardware/backplane](hardware/backplane/) | 集群底板的原理图、PCB 布局和嘉立创 EDA 工程 |
| [hardware/enclosure](hardware/enclosure/) | 外壳、支架和风扇座的机械设计 |
| [software/controller](software/controller/) | Slot 0 上运行的集群管理软件和部署配置 |
| [docs](docs/) | [系统架构](docs/architecture.md)、[组装](docs/assembly.md)和[上电调试](docs/bringup.md) |

## Local References

原始照片、图纸、测量记录和数据手册放在仓库根目录的 `references/`。该目录由 Git 忽略，克隆后可按需创建。新收到的材料可先放到 `references/inbox/`，再按来源归档：

| Directory | Contents |
| --- | --- |
| `references/mci-845/` | MCI 845 核心板照片、尺寸测量、引脚资料和原理图 |
| `references/nanocluster/` | Sipeed NanoCluster 的整机照片、拆解资料和结构图 |
| `references/datasheets/` | 风扇、连接器和其他器件的数据手册及尺寸图 |

确认后的尺寸、引脚定义和来源写入对应的设计文档，随设计一起维护。

## Fabrication and Reproduction

每次送厂打样用 Git 标签记录对应的设计版本，并在 GitHub Releases 附上 Gerber、贴片 BOM、贴片坐标和打印文件。发布说明记录 PCB 修订号、外壳版本和验证过的核心板固件版本。

核心板固件和刷机工具见 [mci-845-firmware](https://github.com/saurlax/mci-845-firmware)。核心板背景和集群形态分别参考[骁龙 845 核心板折腾记](https://saurlax.com/blog/mciserver-845)和 [Sipeed NanoCluster](https://wiki.sipeed.com/hardware/zh/cluster/NanoCluster/index.html)。
