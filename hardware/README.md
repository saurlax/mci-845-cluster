# MCI 845 Cluster

在此目录存放完整的嘉立创 EDA 专业版 v4 文件夹工程。提交时保留工程索引（`.eprj3`）、原理图（`.esch2`）、PCB 布局（`.epcb2`）和工程引用的本地库文件。

[主工程](mci-845-cluster.eprj3) · [复位与供电排针](design/management-header.md) · [顶面供电布局](design/power/top-power-placement.md)

## Electrical Design

在桌面客户端打开 [MCI 845 Cluster](mci-845-cluster.eprj3)。槽位编号与角色见 [System Architecture](../docs/architecture.md)，各槽母座的针脚和差分线序见 [Core Board Connector](845-coreboard/README.md#pin-mapping)。

主工程采用以下三张原理图。

| Sheet | Contents |
| --- | --- |
| [Coreboard](sch/Backplane/Coreboard.esch2) | 六个核心板母座及触点定义，J11 双排 24 针管理接口（六路 UART、复位和供电） |
| [Power](sch/Backplane/Power.esch2) | 12 V 输入保护、电子保险、槽位与风扇支路、交换芯片稳压和去耦 |
| [Ethernet](sch/Backplane/Ethernet.esch2) | 交换芯片、时钟、复位、启动配置和 RJ45 上联 |

六块核心板按两列三行排列，从背板上方垂直插入。核心板侧是 22 触点公头，背板侧是顶插母座。左列从上到下为 Slot 0、1、2，右列为 Slot 3、4、5。7020 风扇在左侧，外部接口集中在右侧。

## Slot Placement

六个 TE 1735284-5 母座从 PCB 顶面看均旋转 180°，7 触点段在右，15 触点段在左，散热片朝 −Y。母座与无焊盘、不计入 BOM 的 MECH1–MECH6 分开放置。机械模型取自 [845 核心板库](845-coreboard/README.md)。[母座资料](https://www.te.com/en/product-1735284-5.html)

坐标沿用 EDA 工程原点，单位为 mm。左板边 X = −7，下板边 Y = 0。表中为母座封装原点；核心板 STEP 插合端面中心相对各母座原点偏移 (−0.235, +2.300)，按模型的两组触点中心线对齐。插合端面暂放在背板顶面上方 6.20 mm，距母座外壳顶部约 3.64 mm。最终插合深度用实板和母座配对核实。

| Row | Left slot | X | Y | Right slot | X | Y |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Upper | Slot 0 / J1 | 25.75 | 55.75 | Slot 3 / J4 | 77.75 | 55.75 |
| Middle | Slot 1 / J2 | 25.75 | 35.75 | Slot 4 / J5 | 77.75 | 35.75 |
| Lower | Slot 2 / J3 | 25.75 | 15.75 | Slot 5 / J6 | 77.75 | 15.75 |

实物极限叠放间距约 18 mm，试装版将同列母座中心距设为 20 mm。两端母座中心分别距板边 15.75 mm、9.25 mm。散热片朝 −Y，按插合端偏移计算，已插卡组的 Y 包络为 1.05 至 61.30 mm；鳍尖距下板边约 1.05 mm，另一侧扣脚距上板边约 3.70 mm。按竖插 STEP 实体测距，四组同列相邻卡在完全插合时的最小净空均为 0.98 mm，位于散热片鳍尖与邻板背面的 IC 封装之间。沿插拔轴投影各实体的三角网格，板面保持平行时，投影轮廓最窄间距也约为 0.98 mm。弹簧扣尖与鳍片在板面上错开。六块核心板的整体横向包络为 X = 0.865–102.165 mm，中心 X = 51.515 mm，与 MH1、MH2、MH5、MH6 四个孔心的平均 X 坐标相差 0.003 mm。两列中心距为 52 mm，同排相邻卡的最小实体净空为 4.00 mm，发生在 FR4 侧边。首件用两块实板和实际母座复测鳍尖净空，并检查轻微倾斜插拔时的擦碰。

## Board Outline and Mounting

主工程 PCB 外形为 **140 × 65 mm**，R3 圆角。板框 X = −7–133、Y = 0–65 mm。六个安装孔的坐标、孔径和禁铜区见 [Mounting Holes](enclosure/assembly/zero-dupont-mount.md#mounting-holes)。

左侧风扇的型号、位置和核心板净空见 [7020 Fan Fit](enclosure/assembly/fan7020-fit.md)。

## Management Board and Models

Zero 的安装范围、铜柱高度和线束净空见 [Four-Post Dupont Mount](enclosure/assembly/zero-dupont-mount.md)。

现有 PCB 布局包含 109 个电气元件位号和 8 个机械组件。外壳装配件 MECH9 包含托盘和可拆风扇面板。已绑定的 3D 模型见 [Model Assets](models/README.md)。

J11 的针位、复位接法和装配条件见 [Management Header](design/management-header.md)。

[Native EDA Assembly](enclosure/assembly/preview/mci-845-eda-assembly-140x65-7020.glb)

## Panel and Ethernet

右侧面板提供千兆 RJ45 上联和圆筒式 12 V DC 输入。六槽串口从板内 J11 引出。

RTL8370N-VB-CG 的 P0–P5 分别直连 SLOT 0–5，每槽四对 MDI 差分线。P6 接内置网络变压器的 HR911130A 上联口，P7 预留。首件逐槽验证千兆协商和双向传输。

J9 的绿灯和黄灯分别通过 R43、R44（各 470 Ω）接 3.3 V，由 U5 的 P6LED0、P6LED1 灌电流驱动。PHY 侧公共中心抽头 P1 经 C61（100 nF）接地。P10 和两个金属屏蔽脚直接连接背板 GND。首件记录断链、百兆、千兆和持续传输时两灯的实际表现。[瑞昱数据手册](https://atta.szlcsc.com/upload/public/pdf/source/20250217/468C3E67021922D5BAC9984AC959B20B.pdf) · [HanRun HR911130A 接线图](https://hrdzen.oss-cn-beijing.aliyuncs.com/202601/1ba07be89265140.pdf) · [PINE64 Clusterboard 原理图，第 2 页](https://files.pine64.org/doc/clusterboard/PINE64%20CLUSTER%20BOARD_2_2_Schematic.pdf#page=2)

HR911130A 图纸第 3 页给出 PCB 孔位和面板开孔，未标注板上禁铜多边形。插座集成磁性器件，保持现有 PHY 信号、中心抽头和屏蔽脚的连接定义。Zero 安装高度需要覆盖 RJ45 外壳、排针插头及线缆转弯空间；风扇两针端子需要按配套插壳和线束复核拔插行程。[Zero 安装尺寸](enclosure/assembly/zero-dupont-mount.md) · [风扇实体测距](enclosure/assembly/fan7020-fit.md)

U9（LTC2909ITS8-3.3）监测 L4、L5 后的 3.3 V 和 1.1 V 模拟电源，两路均越过门限后至少再等 150 ms 释放复位。两路标称门限分别为 3.21 V 和 1.065 V。U3、U4 的反馈分压采用 0.1% 电阻，标称输出分别为 3.361 V 和 1.118 V。首件在磁珠后测满载最低电压、纹波和复位释放时刻。L4、L5 采用 BLM21PG121SN1D。Y1 采用 25 MHz、18 pF 负载的 ABM3-25.000MHZ-D2Y-T，C25、C26 各 27 pF，板上寄生电容计入实际负载。[LTC2909 数据手册](https://www.analog.com/media/en/technical-documentation/data-sheets/2909fb.pdf) · [Abracon ABM3 数据手册](https://abracon.com/Resonators/abm3.pdf)

## UART Console

六个槽位的 UART 直接引到 J11，使用外接多路 TTL UART 模块。针位、信号方向和供电接法见 [Management Header](design/management-header.md)。

## DC Power

背板统一焊装 99 个元件。5 V 支路的 U2、L1、R5、R6、C7–C12 固定空焊。J11 第 9 脚留空，Zero 单独供电。六槽、风扇和交换芯片由电子保险后的 BUS_12V 供电，U3、U4 分别生成 3.3 V 和 1.1 V。

使用外置稳压 12 V / 10 A 适配器。按原供电预算，六块核心板合计 7.2 A，背板和风扇暂估 0.8 A。首件需实测六槽冷启动与满载电流。

[Power](sch/Backplane/Power.esch2) 使用 TVS 和并联 P 沟道 MOSFET 处理输入保护，由 TPS259824O 控制上电斜率和过电流关断。U1 输出的 BUS_12V 同时为六个槽位和两针风扇端子 J8 供电。J8 采用 JST B2B-XH-A 白色直插件，位于顶面左板边，针列沿 Y 轴，中心为 (−3.25, 25.25) mm。线端使用 XHP-2 插壳，从上方插入。靠上板边的 1 脚为 BUS_12V，2 脚为 GND。风扇直接插接时全速运行；需要手动调速时，可在 J8 与风扇之间串接适配两线无刷风扇的旋钮调压模块，最低档按所选风扇的冷启动电压设定。三路 TPS54302 的输入并接 BUS_12V，其中 5 V 支路固定空焊。元件初值按 10 A 输入设计目标选取，整板过流门限、输入斜率、稳压环路和温升按实测定型。 [TPS25982 数据手册](https://www.ti.com/lit/ds/symlink/tps25982.pdf) · [TPS54302 数据手册](https://www.ti.com/lit/ds/symlink/tps54302.pdf)

首版采用圆筒式 12 V DC 电源入口（J7）。按 10 A 设计目标校核插座、配套插头和线束在机内温度下的载流能力。圆筒方案以额定 11 A 的 Switchcraft RAPC10 插座及 S10K 插头为参考。实际封装和面板开孔按所选电源插头及其配套插座确定。 [插座规格](https://www.switchcraft.com/high-amperage-power-jack-silver-terminal-plating-through-hole-termination/rapc10/) · [配套图纸](https://www.switchcraft.com/assets/1/24/S10_SERIES_CD.PDF?6397=)

12 V 主干沿用 8.93 A 连续负载作为铜损设计预算，Zero 由独立电源供电，单槽按 1.2 A 核算。以 20 °C 铜电阻率 0.0172 Ω·mm²/m 估算，给供电方向的主干和每槽支路各分配 50 mV 铜损预算，对应电阻上限分别为 5.60 mΩ 和 41.7 mΩ。地回路、端子接触电阻和温升另计。DC 正极接 VIN_12V_RAW。输入 TVS 故障时由外部电源的短路保护切断或限制电流。U1 监测总电流；支路导线和触点的故障承受能力需结合电源关断时间核对。主干首选线宽为 3.2 mm，槽位支路以 0.8 mm 为初始设计目标，载流能力按并联铜面、焊盘入口和实际换层过孔共同核算。[IPC-2152](https://www.ipc.org/TOC/IPC-2152.pdf)

输入保护集中在 DC 口旁。降压器件布局和电容用途见 [Top-Side Power Placement](design/power/top-power-placement.md)。按持续 8 A 估算，主供电路径每增加 10 mΩ 串联电阻就会产生 0.64 W 损耗和 80 mV 压降。样机装到底座后，在六槽同时满载时测量插头触点、Q1/Q2 和 U1 的压降与温升，同时记录顶面降压区、底面交换芯片及靠出风端核心板的温度。

## Fabrication

四层采用嘉立创 **JLC041621-7628**，标称板厚 1.6 mm。外铜 70 µm，两内层各 30 µm，上下 7628 半固化片各 0.203 mm（Dk 4.4），芯板介质 1.03 mm（Dk 4.6）。L2 为地参考，L3 承载 BUS_12V 铺铜和部分信号走线。外层差分以距连续参考面 0.203 mm、线宽 0.22 mm、边到边间距 0.22 mm 为起点。二维准静态奇模估算约 100 Ω，模型包含阻焊和梯形蚀刻，投产线宽以该叠层的板厂阻抗复核为准。内层和参考面有缺口的走线需要单独处理。[嘉立创叠层](https://jlcpcb.com/impedance) · [阻抗计算器](https://jlcpcb.com/pcb-impedance-calculator/)

六槽和 RJ45 上联的 28 对 MDI 已完成布线。2026-11-24 在嘉立创 EDA 专业版重新打开正式工程、重建铺铜后，全板 DRC 通过，违规 0 项、飞线 0 条。28 对 MDI 的最大对内平面走线长度差为 0.0042 mm，项目容差为 0.254 mm。走线分布在顶层、L3 和底层，L2 用作地参考。J11 两列针之间留出走线禁区。

打样前按所选叠层复核差分阻抗、换层回流和 12 V 载流能力。生产文件从同一修订的嘉立创 EDA 工程导出，包括 Gerber、贴片坐标和 BOM。按[供电装配定义](#dc-power)核对固定空焊位后，将生产文件附到对应的 GitHub Release。阻焊选绿色。
