# MCI 845 Core Board

核心板装配模型用于底板布置、装配净空检查和 3D 展示。模型保留弹簧扣、散热片鳍片、22 触点连接器和 USB-C 接口，背面的元件和丝印按照片简化。

## Core Board Connector

MCI 845 核心板使用 **SATA 外形的 22 触点连接器**，通过配套转接板引出电源和千兆以太网。它采用核心板自定义针脚分配，**不能按标准 SATA 接线**。

### Contact Numbering

正对核心板金手指，让 MCI 标识正立、连接器朝上。从最左端开始数，长段依次为 **L01–L15**。越过缺口，短段从 **R01** 重新起算，最右端是 **R07**。

### Pin Mapping

两张表都从左向右读。Pin# 是核心板金手指编号，Pad 是背板母座的焊盘号，Function 是当前背板设计分配的信号。[TE 1735284-5 母座](https://www.te.com/en/product/1735284-5.html)

#### Long Group

| Pin# | L01 | L02 | L03 | L04 | L05 | L06 | L07 | L08 | L09 | L10 | L11 | L12 | L13 | L14 | L15 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Pad | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 |
| Function | GND | MDI0+ | MDI0− | GND | MDI1+ | MDI1− | GND | MDI2+ | MDI2− | GND | MDI3+ | MDI3− | GND | GND | GND |

#### Short Group

| Pin# | R01 | R02 | R03 | R04 | R05 | R06 | R07 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Pad | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
| Function | 12V | 12V | 12V | 12V | RESET | UART TX | UART RX |

长段的 MDI0 至 MDI3 是四对千兆以太网差分线，+ 和 − 表示各对的正端和负端。GND 为地。V2.1 六槽背板的端口分配和直连接法见 [Panel and Ethernet](../README.md#panel-and-ethernet)。

短段 VIN 按 12 V 输入设计。UART TX、RX 分别指核心板发送和接收。底板的串口和复位接法见 [UART Console](../README.md#uart-console) 和 [Reset and Power Header](../design/management-header.md)。

R05（RESET，母座焊盘 3）接地触发核心板复位。外部控制器用开漏输出拉低，释放时切回高阻。此前在运行中的 V2.1 板上记录过 0 V；首件用示波器复核空闲电平和有效复位脉宽。

### Reference Evidence

本地照片位于 `references/mci-845/sata-interface/`。`05-k001-v2-3-contacts.jpg` 给出触点编号的观察方向，`01-coreboard-and-12v-adapter.jpg` 显示转接板的 `DC12V` 丝印，`02-h845d-adapter-top.jpg` 和 `06-feng-adapter-render-top.jpg` 可见长段到 RJ45 一侧的走线。

长段线序、差分极性和接地触点依据此前记录的 15 针标注特写，特写中的网卡丝印为 RTL8153。照片 03 和 05 分别显示 `MCI_K001_V2_1` 和 `MCI_K001_V2_3`。首件按实际版本核对插合与导通、电源触点和输入电压范围、UART 方向和空闲电平，以及复位脉宽。

器件资料见 [AX88179 数据手册](https://downloads.codico.com/misc/ROHS%202011%2065%20EU%20ab%201.1.2013/Asix/AX88179_Datasheet_v122.pdf) · [Amphenol 22 触点连接器图纸](https://www.amphenol-cs.com/product/sata00102253a.html)。

### Continuity Mapping

1. 拔下电源和网线，核心板与转接板分离。用转接板母座的可接触焊脚测量。先记录 DC 插座正极、负极及输入保护器件两端各连到哪些触点。用电阻值区分直接连接和经过器件的路径。
2. 读出 RJ45 型号，用该型号的图纸确认板侧引脚、变压器中心抽头、LED 和屏蔽脚。逐一追踪板侧焊脚到 22 触点，必要时再从核心板实际搭载的以太网芯片或其邻近器件交叉验证。变压器同一绕组的两端都可能触发蜂鸣，需用走线或直接到器件焊盘的测量分辨极性。
3. 用原配转接板单独供电，在固定测点验证电源触点电压。剩余触点记录测过的端点、电阻和上电状态。仅凭蜂鸣表没有响，无法确定触点空接。确认电源和地之前，禁止从自制背板向核心板上电。

### Measurement Record

每块板填一张。测试记录包含核心板版本、转接板版本和 RJ45 型号。将 `—` 替换为确认到的网络与测点，电源触点同时记录电压。

| Long Contact | Net / Test Point | Short Contact | Net / Test Point |
| --- | --- | --- | --- |
| L01 | — | R01 | — |
| L02 | — | R02 | — |
| L03 | — | R03 | — |
| L04 | — | R04 | — |
| L05 | — | R05 | — |
| L06 | — | R06 | — |
| L07 | — | R07 | — |
| L08 | — | | |
| L09 | — | | |
| L10 | — | | |
| L11 | — | | |
| L12 | — | | |
| L13 | — | | |
| L14 | — | | |
| L15 | — | | |

## Onboard UART Pads

`MCI_K001_V2_1` 的 USB-C 旁有三个串口焊孔，实板丝印为 `TX`、`RX`、`GND`。该版本实测中，TX 和 RX 焊孔与金手指均未测得直通。焊孔的逻辑电压、与金手指串口之间的电路关系及启动时是否输出日志仍待确认。

## JLCEDA Pro Library

[MCI 845 Mechanical](MCI%20845%20Mechanical.elib) 是嘉立创 EDA 专业版的本地器件库。三个器件各有独立符号、外形封装和 STEP 绑定，可放置到 PCB 上用于装配预览。封装无铜焊盘，器件不计入 BOM。

| Device | Placement Origin |
| --- | --- |
| MCI 845 Core Board | 竖插，原点在 SATA 插合端面的中心。背板母座的实际插合高度通过 3D 偏移校准 |
| MCI 845 Heatsink | 鳍片区中心，Z=0 为散热片底面 |
| MCI 845 Spring Push Pin | 扣脚轴线，Z=0 为扣脚尖端 |

安装器件库时，把 `.elib` 和 [`eda-models`](eda-models/) 内的三个 STEP 放进 EDA 配置的库目录，刷新器件库，再在封装的 3D 模型管理器中选中对应 STEP，核对放置原点。 [嘉立创 EDA 封装属性](https://prodocs.lceda.cn/cn/footprint/side-panel-left-property/)

## CAD Files

- [STEP assembly](assembly/mci-845-coreboard.step) 用于 CAD 导入和测量。
- [GLB assembly](assembly/mci-845-coreboard.glb) 用于彩色 3D 预览，文件单位为米。

## Dimensions

单位为 mm。由散热片侧俯视，SATA 在上方，USB-C 在下方。原点位于 PCB 左下角，X 向右，Y 指向 SATA，Z=0 为 PCB 上表面。

| Feature | Nominal | Basis |
| --- | ---: | --- |
| PCB length × width | 54 × 48 | 手测 |
| SATA overhang | 4 | 从 PCB 的 SATA 边量至外壳端面 |
| USB-C shell edge to PCB edge | 13 | 正对 USB-C 口、PCB 位于口上方时，量外壳右缘至板右缘。对应模型 X=13 至 X=0 |
| Heatsink body | 37 × 37 | 手测，安装耳伸出本体 |
| PCB top to heatsink base | 4.5 | 手测，量至底座下表面 |
| PCB top to fin tips | 17 | 手测 |
| Diagonal push-pin pitch | 59 | 参考 Radian 37.5004 系列图纸 |
| PCB thickness | 1.2 | 按侧面照片估计 |

散热片沿用实测外形，安装孔中心采用 `(2.50, 3.40)` 和 `(45.50, 43.80)`，单孔位置及孔径按照片和参考件估算。加工前以实物复核孔坐标、板厚与接口开窗。 [Radian 37.5004 系列尺寸图](https://radianheatsinks.com/wp-content/uploads/2025/09/Radian-Catalogue-2026-27.pdf)

Same Sky HSB30-373710 的厂商 STEP 中，鳍片区为 37.4 × 37.4 mm，铝件高 10 mm，扣脚在底座下方约 3 mm。实物对应的铝件高度为 12.5 mm，距板面约 4.5 mm。库件按这两个装配尺寸建模，孔距采用 59 mm。 [Same Sky 尺寸图](https://www.sameskydevices.com/product/resource/hsb30-373710.pdf)
