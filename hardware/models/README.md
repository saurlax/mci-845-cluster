# Assembly Models

本目录记录当前底板装配使用的 3D 模型。Zero 的安装与接线见 [Four-Post Dupont Mount](../enclosure/assembly/zero-dupont-mount.md)。

## Local Library

MECH1–MECH6 共用[核心板竖插 STEP](../845-coreboard/eda-models/mci-845-coreboard-vertical.step)。MECH8 加载[台达 7020 风扇 STEP](mci-845-delta-7020.step)。工程保留 STEP 原件，EDA 从已登记的本地模型库加载。换机时将核心板、风扇、J8、J11 及外壳 STEP 放入新机器的模型库，并在 PCB 的 3D 模型管理器中核对库路径。

7020 模型来自台达官方 STEP。J11 的 [2×12 公排针 STEP](samtec-tsw-112-07-g-d.step) 按 [Samtec TSW-112-07-G-D](https://www.samtec.com/products/tsw-112-07-g-d) 的排距、针高和焊尾尺寸建模。J8 的 [JST B2B-XH-A STEP](jst-b2b-xh-a.step) 来自 René Pöschl 绘制的 [KiCad 3D 模型库](https://github.com/KiCad/kicad-packages3D/blob/master/Connector_JST.3dshapes/JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical.step)，授权说明保留在 STEP 文件头。两者均从本地 EDA 模型库加载。Zero 3W 的机械资料见 [Radxa 官方资源](../reference-models/radxa-zero-3w/README.md)。铜柱与加高排母 STEP 是历史试排资源。

MECH9 引用[外壳装配 STEP](../enclosure/printed-base/cad/printed-base-assembly.step)，按 PCB 原点放置托盘和风扇面板。

## Component Packages

[CSV](model-bindings.csv) 和 [JSON](model-bindings.json) 按 PCB 位号列出模型、安装面和装配状态。目录模型使用 EDA 标识，本地 STEP 使用相对于本目录的路径。JSON 另列出本地模型的 SHA-256。5 V 空焊位仍保留封装模型，导出装配清单时按[供电装配定义](../README.md#dc-power)核对。

## Preview

![EDA assembly preview](../enclosure/assembly/preview/eda-cluster-assembly.png)

[Native EDA Assembly](../enclosure/assembly/preview/mci-845-eda-assembly-140x65-7020.glb) 由 EDA 原生三维导出转换，导出时关闭缺失模型自动生成。
