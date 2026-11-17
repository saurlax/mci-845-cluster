# Assembly

选定打样版本后，从同一个 GitHub Release 获取底板生产包和外壳打印文件，并核对其中记录的 PCB 修订号和外壳版本。

整机物料包括六块 MCI 845 核心板、集群底板、外壳及支架，以及 60 × 60 mm 方框轴流风扇。风扇选型依据见[外壳设计](../hardware/enclosure/README.md)。电源、紧固件规格和打印设置随设计补齐。确定规格后，整机采购清单记录在 `docs/assembly-bom.csv`，PCB 贴片 BOM 由嘉立创 EDA 工程导出。

安装顺序及连接器方向以对应版本的装配图为准。装好后按[上电调试](bringup.md)逐槽检查。
