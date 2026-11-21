# Four-Post Dupont Mount

底板仅保留 Zero 四个固定孔及禁铜区，用户可自行安装管理板并通过杜邦线配置连接。Zero、四根铜柱和直插排母的机械组件及封装均已移除，长条直插通道禁铜区已取消。板框继续为 140 × 65 mm，7020 风扇及六块 845 的位置保持当前布局。

## Mounting Holes

| Hole | X (mm) | Y (mm) | Function |
| --- | ---: | ---: | --- |
| MH1 | −3.5 | 3.5 | Chassis |
| MH2 | 5.5 | 47 | Chassis |
| MH3 | 129.4001 | 3.6001 | Zero outer lower |
| MH4 | 129.4001 | 61.4501 | Zero outer upper |
| MH5 | 106.5001 | 3.6001 | Zero inner lower |
| MH6 | 106.5501 | 61.4001 | Zero inner upper |

六个底板孔均为 Ø2.9 mm 非金属化孔，周围禁铜直径 Ø6 mm。安装孔按 M2.5 紧固件预留。新增内侧两孔的禁铜区避开当前铜线和过孔。

## Hole Copper

当前六孔采用非金属化机械孔（`plated=false`），无网络连接。孔径和焊盘外径均为 Ø2.9 mm，没有环形铜焊盘；孔外另设 Ø6 mm 禁铜区。金属铜柱安装时，当前设计保持孔周与电路铜箔隔离。

露铜安装焊盘可用于定义螺钉、铜柱和机壳之间的接地连接。是否连接电路 GND 或独立机壳地，应在接地方案确定后设置。当前孔属性保持不变。

## Assembly Height and Wiring

当前预览仅显示底板、六块 845 和 7020 风扇。铜柱高度可按散热片和线束选择；四个固定点用于用户安装管理板。最终高度同时计入散热片、RJ45、杜邦插头外壳和出线弯曲空间。

现有 847 条焊盘网络映射保持原样。Zero 与底板的 UART、RESET、电源针位和电平在电气设计中定义，当前保留四孔固定与用户自行接线的方案。

## Native EDA Preview

[Main EDA Project](../../backplane/mci-845-backplane/mci-845-backplane.eprj3) · [3D Assembly](preview/mci-845-eda-assembly-140x65-7020.glb) · [Interface View](preview/eda-zero3w-interface-closeup.png)

当前主工程包含 206 个组件：199 个电气组件、六块 845 和一个 7020 风扇。
