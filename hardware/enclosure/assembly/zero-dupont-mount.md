# Four-Post Dupont Mount

底板为 Zero 预留四个固定孔及禁铜区，用户可自行安装管理板并通过杜邦线连接。Zero 安装范围为 X = 103–133、Y = 0–65 mm，前后边和接口侧边与底板对齐。板框与槽位布局见 [Cluster Backplane](../../README.md#board-outline-and-mounting)。

## Mounting Holes

| Hole | X (mm) | Y (mm) | Function |
| --- | ---: | ---: | --- |
| MH1 | −3.5 | 3.5 | Chassis |
| MH2 | −3.5 | 61.4501 | Chassis |
| MH3 | 129.4001 | 3.6001 | Zero outer lower |
| MH4 | 129.4001 | 61.4501 | Zero outer upper |
| MH5 | 106.5001 | 3.6001 | Zero inner lower |
| MH6 | 106.5501 | 61.4001 | Zero inner upper |

MH2 与 MH1 共用 X 坐标，与 MH4 共用 Y 坐标。MH2 孔心距左板边 3.50 mm，距上板边 3.55 mm。以 PCB 顶面为起点，用直径 6 mm、高 75 mm 的圆柱包络铜柱最大外廓，对六块完全插合的 845 核心板 STEP 实体测距。MH1、MH2、MH5、MH6 分别距 Slot 2、0、5、3 最近，净空依次为 2.453、2.476、2.370、2.475 mm。右列核心板最外缘与 Zero 板框在 X 方向相距 0.835 mm。六角铜柱按对角尺寸选取，实装余量还需扣除孔位和装配偏差。[STEP 净空数据](checks/slot-standoff-fit.json)

六个底板孔均为 Ø2.9 mm 非金属化孔，周围禁铜直径 Ø6 mm。安装孔按 M2.5 紧固件预留。新增内侧两孔的禁铜区避开当前铜线和过孔。

## Hole Copper

当前六孔采用非金属化机械孔（`plated=false`），无网络连接。孔径和焊盘外径均为 Ø2.9 mm，没有环形铜焊盘；孔外另设 Ø6 mm 禁铜区。金属铜柱安装时，当前设计保持孔周与电路铜箔隔离。

露铜安装焊盘可用于定义螺钉、铜柱和机壳之间的接地连接。是否连接电路 GND 或独立机壳地，应在接地方案确定后设置。当前孔属性保持不变。

## Assembly Height and Wiring

铜柱高度按散热片、RJ45、杜邦插头外壳和出线弯曲空间确定。托盘支撑高度同时满足底面器件净空和风道要求。

管理线束接法见 [Management Header](../../design/management-header.md)，串口接法见 [UART Console](../../README.md#uart-console)。

## Native EDA Preview

[Main EDA Project](../../mci-845-cluster.eprj3) · [3D Assembly](preview/mci-845-eda-assembly-140x65-7020.glb) · [Interface View](preview/eda-zero3w-interface-closeup.png)
