# MCI 845 Cluster

在此目录存放完整的嘉立创 EDA 专业版 v4 文件夹工程。提交时保留工程索引（`.eprj3`）、原理图（`.esch2`）、PCB 布局（`.epcb2`）和工程引用的本地库文件。

[主工程](mci-845-cluster.eprj3) · [复位与供电排针](design/management-header.md) · [顶面供电布局](design/power/top-power-placement.md)

## Electrical Design

在桌面客户端打开 [MCI 845 Cluster](mci-845-cluster.eprj3)。槽位编号与角色见 [System Architecture](../docs/architecture.md)，各槽母座的针脚和差分线序见 [Core Board Connector](845-coreboard/README.md#pin-mapping)。

主工程采用以下四张原理图。

| Sheet | Contents |
| --- | --- |
| [Coreboard](sch/Backplane/Coreboard.esch2) | 六个核心板母座及触点定义 |
| [Power](sch/Backplane/Power.esch2) | 12 V 输入保护、电子保险、槽位与风扇支路、交换芯片稳压和去耦 |
| [Ethernet](sch/Backplane/Ethernet.esch2) | 交换芯片、时钟、复位、启动配置、复位与供电排针和 RJ45 上联 |
| [Console](sch/Backplane/Console.esch2) | USB-C、CH348L、六路 UART |

六块核心板按两列三行排列，从背板上方垂直插入。核心板侧是 22 触点公头，背板侧是顶插母座。左列从上到下为 Slot 0、1、2，右列为 Slot 3、4、5。7020 风扇在左侧，外部接口集中在右侧。

## Slot Placement

六个 TE 1735284-5 母座从 PCB 顶面看均旋转 180°，7 触点段在右，15 触点段在左，散热片朝 −Y。母座与无焊盘、不计入 BOM 的 MECH1–MECH6 分开放置。机械模型取自 [845 核心板库](845-coreboard/README.md)。[母座资料](https://www.te.com/en/product-1735284-5.html)

坐标沿用 EDA 工程原点，单位为 mm。左板边 X = −7，下板边 Y = 0。表中为母座封装原点；核心板 STEP 插合端面中心相对各母座原点偏移 (−0.235, +2.300)，按模型的两组触点中心线对齐。插合端面暂放在背板顶面上方 6.20 mm，距母座外壳顶部约 3.64 mm。最终插合深度用实板和母座配对核实。

| Row | Left slot | X | Y | Right slot | X | Y |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Upper | Slot 0 / J1 | 20 | 57 | Slot 3 / J4 | 72 | 57 |
| Middle | Slot 1 / J2 | 20 | 37 | Slot 4 / J5 | 72 | 37 |
| Lower | Slot 2 / J3 | 20 | 17 | Slot 5 / J6 | 72 | 17 |

实物极限叠放间距约 18 mm，试装版将同列母座中心距设为 20 mm。两端母座中心分别距板边 17 mm、8 mm。散热片朝 −Y，按插合端偏移计算，已插卡组的 Y 包络为 2.30 至 62.55 mm；鳍尖距下板边约 2.30 mm，另一侧扣脚距上板边约 2.45 mm。按竖插 STEP 实体测距，四组同列相邻卡在完全插合时的最小净空均为 0.98 mm，位于散热片鳍尖与邻板背面的 IC 封装之间。沿插拔轴投影各实体的三角网格，板面保持平行时，投影轮廓最窄间距也约为 0.98 mm。弹簧扣尖与鳍片在板面上错开。两列中心距为 52 mm，同排相邻卡的最小实体净空为 4.00 mm，发生在 FR4 侧边。首件用两块实板和实际母座复测鳍尖净空，并检查轻微倾斜插拔时的擦碰。

## Board Outline and Mounting

主工程 PCB 外形为 **140 × 65 mm**，R3 圆角。板框 X = −7–133、Y = 0–65 mm。六个安装孔的坐标、孔径和禁铜区见 [Mounting Holes](enclosure/assembly/zero-dupont-mount.md#mounting-holes)。

左侧风扇的型号、位置和核心板净空见 [7020 Fan Fit](enclosure/assembly/fan7020-fit.md)。

## Management Board and Models

Zero 的安装范围、铜柱高度和线束净空见 [Four-Post Dupont Mount](enclosure/assembly/zero-dupont-mount.md)。

主工程包含 139 个电气组件和 8 个机械组件。外壳装配件 MECH9 包含托盘和可拆风扇面板。已绑定的 3D 模型见 [Model Assets](models/README.md)。

J11 的针位、布线状态和装配条件见 [Reset and Power Header](design/management-header.md)。

[Native EDA Assembly](enclosure/assembly/preview/mci-845-eda-assembly-140x65-7020.glb)

## Panel and Ethernet

右侧面板从上到下为千兆 RJ45 上联、USB-C `CONSOLE` 和圆筒式 12 V DC 输入。三者的插口均朝向面板，沿板宽方向的中心距为 18 mm。

RTL8370N-VB-CG 的 P0–P5 分别直连 SLOT 0–5，每槽四对 MDI 差分线。P6 接内置网络变压器的 HR911130A 上联口，P7 预留。六槽差分对待按叠层重新布线，首件逐槽验证千兆协商和双向传输。

J9 的绿灯和黄灯分别通过 R43、R44（各 470 Ω）接 3.3 V，由 U5 的 P6LED0、P6LED1 灌电流驱动。PHY 侧公共中心抽头 P1 经 C61（100 nF）接地。P10 和两个金属屏蔽脚直接连接背板 GND。首件记录断链、百兆、千兆和持续传输时两灯的实际表现。[瑞昱数据手册](https://atta.szlcsc.com/upload/public/pdf/source/20250217/468C3E67021922D5BAC9984AC959B20B.pdf) · [HanRun HR911130A 接线图](https://hrdzen.oss-cn-beijing.aliyuncs.com/202601/1ba07be89265140.pdf) · [PINE64 Clusterboard 原理图，第 2 页](https://files.pine64.org/doc/clusterboard/PINE64%20CLUSTER%20BOARD_2_2_Schematic.pdf#page=2)

U9（LTC2909ITS8-3.3）监测 L4、L5 后的 3.3 V 和 1.1 V 模拟电源，两路均越过门限后至少再等 150 ms 释放复位。两路标称门限分别为 3.21 V 和 1.065 V。U3、U4 的反馈分压采用 0.1% 电阻，标称输出分别为 3.361 V 和 1.118 V。首件在磁珠后测满载最低电压、纹波和复位释放时刻。L4、L5 采用 BLM21PG121SN1D。Y1 采用 25 MHz、18 pF 负载的 ABM3-25.000MHZ-D2Y-T，C25、C26 各 27 pF，板上寄生电容计入实际负载。[LTC2909 数据手册](https://www.analog.com/media/en/technical-documentation/data-sheets/2909fb.pdf) · [Abracon ABM3 数据手册](https://abracon.com/Resonators/abm3.pdf)

## USB Console

CH348L 的 VCC 取背板 SW_3V3，U8 从同一电源生成 1.8 V，供全部串口 I/O 使用。UART0–5 直接接 SLOT 0–5，每路 TX 接对端 RX。94 脚 TEST 接地，RESET 使用内部上拉。晶振为 8 MHz，七颗 100 nF 电容分别靠近各 VCC、VIO 引脚。V2.1 首件从金手指验证六槽收发，槽位复位连接见 [Reset and Power Header](design/management-header.md)。[沁恒 CH348 数据手册](https://atta.szlcsc.com/upload/public/pdf/source/20240313/A2EF5AA685A1AE72CD026213AA917E03.pdf)

USB-C 的 CC1、CC2 分别通过 5.1 kΩ 接地。U10 保护 D+/D−，U11（TS3USB221ARSER）由背板 3.3 V 供电。R47、R48 各 10 kΩ，将 VBUS 二分之一送到 U11 的 S 输入。主机提供 VBUS 时，U11 选择接到 CH348L 的第二通道；拔线后选择留空的第一通道。仅插 USB 时，背板和串口桥保持断电。首件验证 USB 正反插枚举、带线开关背板电源，以及背板供电时拔线再枚举。[TI TS3USB221A 数据手册](https://www.ti.com/lit/ds/symlink/ts3usb221a.pdf) · [USB-IF 反向供电测试](https://www.usb.org/sites/default/files/USB-IFTestProc1_3.pdf)

## DC Power

采用外置稳压 12 V DC 电源，首版以额定 10 A（120 W）作为预算。满载预算暂取 8 A，其中六块板合计 7.2 A，风扇、交换芯片及其他背板电路合计 0.8 A。这是供电预算，定型前用原配转接板测单板启动峰值和持续满载电流，再复测六槽同时开机。

[Power](sch/Backplane/Power.esch2) 使用主保险、TVS 和并联 P 沟道 MOSFET 处理输入保护，由 TPS259824O 控制上电斜率和过电流关断。六个槽位各有独立保险，F8 经两针 J8 为 12 V 两线风扇供电。风扇直接插接时全速运行；需要手动调速时，可在 J8 与风扇之间串接适配两线无刷风扇的旋钮调压模块，最低档按所选风扇的冷启动电压设定。三级 TPS54302 分别生成 5 V、3.3 V 和 1.1 V。元件初值按 10 A 输入设计目标选取，主保险、各支路保险、输入斜率、稳压环路和温升按实测定型。 [TPS25982 数据手册](https://www.ti.com/lit/ds/symlink/tps25982.pdf) · [TPS54302 数据手册](https://www.ti.com/lit/ds/symlink/tps54302.pdf)

首版采用圆筒式 12 V DC 电源入口（J7）。按 10 A 设计目标校核插座、配套插头和线束在机内温度下的载流能力。圆筒方案以额定 11 A 的 Switchcraft RAPC10 插座及 S10K 插头为参考。实际封装和面板开孔按所选电源插头及其配套插座确定。 [插座规格](https://www.switchcraft.com/high-amperage-power-jack-silver-terminal-plating-through-hole-termination/rapc10/) · [配套图纸](https://www.switchcraft.com/assets/1/24/S10_SERIES_CD.PDF?6397=)

铺铜规划：内层 1 为 GND，内层 2 为 BUS_12V。底面为 DC 入口、主保险后、反接保护后和电子保险输出分别铺铜，六槽支路覆盖保险输出及母座 12 V 触点。叠层初选外层 2 oz、独立连续的地参考层。铜宽、端子焊盘颈部、保险焊盘和换层过孔按最大持续电流、允许压降和温升定尺寸。千兆差分线按选定叠层做 100 Ω 阻抗匹配，确定线宽前核对 2 oz 工艺的最小线宽线距。 [嘉立创制造能力](https://www.jlc.com/portal/vtechnology.html) · [IPC-2152](https://www.ipc.org/TOC/IPC-2152.pdf)

输入保护集中在 DC 口旁。降压器件布局和电容用途见 [Top-Side Power Placement](design/power/top-power-placement.md)。按持续 8 A 估算，主供电路径每增加 10 mΩ 串联电阻就会产生 0.64 W 损耗和 80 mV 压降。样机装到底座后，在六槽同时满载时测量插头触点、F1、Q1/Q2 和 U1 的压降与温升，同时记录顶面降压区、底面交换芯片及靠出风端核心板的温度。

## Fabrication

PCB 的四层预览包含器件摆放、临时封装和试布线。按实际型号确认封装和器件净空，调整 12 V 汇流及地回流，按选定叠层重布 USB 与千兆差分线。通过设计规则检查后，从对应修订导出 Gerber、贴片 BOM 和贴片坐标，并一起上传到对应的 GitHub Release。下单选择绿色阻焊。
