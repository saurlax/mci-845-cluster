# Cluster Backplane

在此目录存放完整的嘉立创 EDA 专业版 v4 文件夹工程。提交时保留工程索引（`.eprj3`）、原理图（`.esch2`）、PCB 布局（`.epcb2`）和工程引用的本地库文件。

## Electrical Design

在桌面客户端打开 [MCI 845 Backplane](mci-845-backplane/mci-845-backplane.eprj3)。`J1` 至 `J6` 分别对应 Slot 0 至 Slot 5，`J1` 为管理节点。每槽按[照片对应表](../../docs/coreboard-connector.md#preview-mapping)接入接地、四对以太网、12 V 和两根 UART 信号。复位触点 R05 通过默认不装的 0 Ω 电阻接到管理排针。母座焊盘映射、12 V 输入范围、串口电平及差分耦合方式按实物核对。

六块核心板按两列三行排列，从背板上方垂直插入。核心板侧是 22 触点公头，背板侧是顶插母座。左列从上到下为 Slot 0、1、2，右列为 Slot 3、4、5。7020 风扇在左侧，外部接口集中在右侧。

## Slot Placement

六个 TE 1735284-5 母座从 PCB 顶面看均旋转 180°，7 触点段在右，15 触点段在左，散热片朝 −Y。母座与无焊盘、不计入 BOM 的 MECH1–MECH6 分开放置。机械模型取自 [845 核心板库](../845-coreboard/README.md)。[母座资料](https://www.te.com/en/product-1735284-5.html)

坐标沿用 EDA 工程原点，单位为 mm。左板边 X = −7，下板边 Y = 0。表中为母座封装原点；核心板 STEP 插合端面中心相对各母座原点偏移 (−0.235, +2.300)，按模型的两组触点中心线对齐。插合端面暂放在背板顶面上方 6.20 mm，距母座外壳顶部约 3.64 mm。最终插合深度、键位、触点编号与电源极性需用实板配对核实。

| Row | Left slot | X | Y | Right slot | X | Y |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Upper | Slot 0 / J1 | 20 | 57 | Slot 3 / J4 | 72 | 57 |
| Middle | Slot 1 / J2 | 20 | 37 | Slot 4 / J5 | 72 | 37 |
| Lower | Slot 2 / J3 | 20 | 17 | Slot 5 / J6 | 72 | 17 |

实物极限叠放间距约 18 mm，试装版将同列母座中心距设为 20 mm。两端母座中心分别距板边 17 mm、8 mm。散热片朝 −Y，按插合端偏移计算，已插卡组的 Y 包络为 2.30 至 62.55 mm；鳍尖距下板边约 2.30 mm，另一侧扣脚距上板边约 2.45 mm。按竖插 STEP 实体测距，四组同列相邻卡在完全插合时的最小净空均为 0.98 mm，位于散热片鳍尖与邻板背面的 IC 封装之间。沿插拔轴投影各实体的三角网格，板面保持平行时，投影轮廓最窄间距也约为 0.98 mm。弹簧扣尖与鳍片在板面上错开。两列中心距为 52 mm，同排相邻卡的最小实体净空为 4.00 mm，发生在 FR4 侧边。首件用两块实板和实际母座复测鳍尖净空，并检查轻微倾斜插拔时的擦碰。

## Board Outline and Mounting

主工程 PCB 外形为 **140 × 65 mm**，R3 圆角。板框 X = −7–133、Y = 0–65 mm。底板共有六个 M2.5 安装孔：两个底壳孔位于 (−3.5, 3.5)、(5.5, 47) mm，另外四孔对应 Zero 安装孔。孔径 Ø2.9 mm，禁铜直径 Ø6 mm。

左侧风扇采用台达 AFC0712DD-TP10 **7020** 官方模型，包络 X = −27–−7、Y = −2.5–67.5、Z = 0–70 mm，与左列核心板最小实体净空为 2.115 mm。风框在 PCB 两侧各伸出 2.5 mm。[Fan Fit](../enclosure/fan7020-fit.md)

## Management Board and Models

Zero 安装孔对应的 PCB 平面范围为 X = 103–133、Y = 0–65 mm，前后边和接口侧边与底板对齐。底板仅预留 Zero 四个 M2.5 固定孔及禁铜区；Zero、铜柱和直插排母的机械模型均已移除。用户可自行安装管理板并用杜邦线连接。

| Mount | X (mm) | Y (mm) |
| --- | ---: | ---: |
| Outer lower / MH3 | 129.4001 | 3.6001 |
| Outer upper / MH4 | 129.4001 | 61.4501 |
| Inner lower / MH5 | 106.5001 | 3.6001 |
| Inner upper / MH6 | 106.5501 | 61.4001 |

安装高度根据用户选用的铜柱、散热片、网口净空与杜邦线插头空间确定。当前三维装配显示底板、六块 845 和 7020 风扇。[Mounting Details](../enclosure/zero-dupont-mount.md)

主工程包含 205 个电气组件和 7 个机械组件。已绑定的 3D 模型见 [Model Assets](mci-845-backplane/models/README.md)。

管理接口 J11 采用 **2×10、2.54 mm 直插排针**，放在网口侧的 PCB 顶面。原理图和 PCB 已分配 GND、MDC、MDIO 和六路复位网络。六路复位各通过一颗默认不装的 0 Ω 电阻接至槽位 R05。针位和装配条件见 [Management Header](management-header.md)。排针待布线。六路 UART 经 CH348L 走 USB-C。

[140 × 65 mm 同步试排工程](variants/140x65/mci-845-backplane-140x65.eprj3) · [Native EDA Assembly](../enclosure/mci-845-eda-assembly-140x65-7020.glb)

## Panel and Ethernet

右侧面板从上到下为千兆 RJ45 上联、USB-C `CONSOLE` 和圆筒式 12 V DC 输入。三者的插口均朝向面板，沿板宽方向的中心距为 18 mm。

首版交换芯片采用 RTL8370N-VB-CG（`C2803243`）。P0–P5 对应六块核心板，P6 对应 HR911130A 上联，P7 预留。交换电路包含 25 MHz 晶振、1.1 V 监控复位、启动配置电阻和独立模拟电源滤波。六槽各预留四对差分线的串联焊盘，按实测极性和核心板 PHY 耦合方式决定装配。上联的 P1 是 PHY 侧公共中心抽头，P10 接屏蔽网络。P1 旁路和屏蔽网络到背板地的连接方式按联调确定。 [瑞昱数据手册](https://atta.szlcsc.com/upload/public/pdf/source/20250217/468C3E67021922D5BAC9984AC959B20B.pdf) · [HanRun HR911130A 接线图](https://hrdzen.oss-cn-beijing.aliyuncs.com/202601/1ba07be89265140.pdf) · [PINE64 Clusterboard 原理图](https://files.pine64.org/doc/clusterboard/PINE64%20CLUSTER%20BOARD_2_2_Schematic.pdf)

## USB Console

[USB Console](mci-845-backplane/sch/Backplane/USB%20Console.esch2) 使用 USB-C 设备端接法和 USB 数据线 ESD 保护。CH348L（`C2979160`）由 USB VBUS 经独立 LDO 供电，I/O 电源可选 1.8 V 或 3.3 V，原理图默认 1.8 V。六路 TX/RX 已按候选针位经过一组默认不装的 0 Ω 电阻接到母座，根据实测方向和电平决定装配。 [沁恒 CH348 数据手册](https://atta.szlcsc.com/upload/public/pdf/source/20240313/A2EF5AA685A1AE72CD026213AA917E03.pdf)

## DC Power

采用外置稳压 12 V DC 电源，首版以额定 10 A（120 W）作为预算。满载预算暂取 8 A，其中六块板合计 7.2 A，风扇、交换芯片及其他背板电路合计 0.8 A。这是供电预算，定型前用原配转接板测单板启动峰值和持续满载电流，再复测六槽同时开机。

[Power Distribution](mci-845-backplane/sch/Backplane/Power%20Distribution.esch2) 使用主保险、TVS 和并联 P 沟道 MOSFET 处理输入保护，由 TPS259824O 控制上电斜率和过电流关断。六个槽位各有独立保险，12 V 风扇单独供电。三级 TPS54302 分别生成 5 V、3.3 V 和 1.1 V。元件初值按 10 A 输入设计目标选取，主保险、各支路保险、输入斜率、稳压环路和温升按实测定型。 [TPS25982 数据手册](https://www.ti.com/lit/ds/symlink/tps25982.pdf) · [TPS54302 数据手册](https://www.ti.com/lit/ds/symlink/tps54302.pdf)

首版采用圆筒式 12 V DC 电源入口（J7）。按 10 A 设计目标校核插座、配套插头和线束在机内温度下的载流能力。圆筒方案以额定 11 A 的 Switchcraft RAPC10 插座及 S10K 插头为参考。实际封装和面板开孔按所选电源插头及其配套插座确定。 [插座规格](https://www.switchcraft.com/high-amperage-power-jack-silver-terminal-plating-through-hole-termination/rapc10/) · [配套图纸](https://www.switchcraft.com/assets/1/24/S10_SERIES_CD.PDF?6397=)

铺铜规划：内层 1 为 GND，内层 2 为 BUS_12V。底面为 DC 入口、主保险后、反接保护后和电子保险输出分别铺铜，六槽支路覆盖保险输出及母座 12 V 触点。叠层初选外层 2 oz、独立连续的地参考层。铜宽、端子焊盘颈部、保险焊盘和换层过孔按最大持续电流、允许压降和温升定尺寸。千兆差分线按选定叠层做 100 Ω 阻抗匹配，确定线宽前核对 2 oz 工艺的最小线宽线距。 [嘉立创制造能力](https://www.jlc.com/portal/vtechnology.html) · [IPC-2152](https://www.ipc.org/TOC/IPC-2152.pdf)

三路降压 U2–U4、L1–L3 及其配套阻容已移至顶面前沿；C1、C23、C24 三颗大电容、主保险 F1 和调试排针 J11 同步换到顶面。C1 是 12 V 母线储能电容，C23/C24 为交换芯片 1.1 V 输出滤波电容。输入保护集中在 DC 口旁。[Top-Side Power Placement](top-power-placement.md) 记录各器件位置与电容用途。按持续 8 A 估算，主供电路径每增加 10 mΩ 串联电阻就会产生 0.64 W 损耗和 80 mV 压降。样机装入外壳后，在六槽同时满载时测量插头触点、F1、Q1/Q2 和 U1 的压降与温升，同时记录顶面降压区、底面交换芯片及靠出风端核心板的温度。铜柱高度应同时满足底面最高器件净空和风道要求。

## Fabrication

PCB 的四层预览包含器件摆放、临时封装和试布线。按实际型号确认封装和器件净空，调整 12 V 汇流及地回流，按选定叠层重布 USB 与千兆差分线。通过设计规则检查后，从对应修订导出 Gerber、贴片 BOM 和贴片坐标，并一起上传到对应的 GitHub Release。下单选择绿色阻焊。
