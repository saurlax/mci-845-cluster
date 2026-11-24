# Management Header

J11 是 2×12、2.54 mm 双排直插公针，型号为 Samtec TSW-112-07-G-D，提供六槽 UART、六槽复位、交换机复位、3.3 V 和公共地。使用杜邦线按信号名连接 Zero。方形焊盘为 1 脚。

| Odd pin | Signal | Even pin | Signal |
| --- | --- | --- | --- |
| 1 | S0_RESET | 2 | S1_RESET |
| 3 | S2_RESET | 4 | S3_RESET |
| 5 | S4_RESET | 6 | S5_RESET |
| 7 | SW_RESET_N | 8 | GND |
| 9 | SYS_5V（空焊，留空） | 10 | SW_3V3 |
| 11 | S0_UART_TX | 12 | S0_UART_RX |
| 13 | S1_UART_TX | 14 | S1_UART_RX |
| 15 | S2_UART_TX | 16 | S2_UART_RX |
| 17 | S3_UART_TX | 18 | S3_UART_RX |
| 19 | S4_UART_TX | 20 | S4_UART_RX |
| 21 | S5_UART_TX | 22 | S5_UART_RX |
| 23 | GND | 24 | GND |

J11 的 1–6 脚分别直连 SLOT 0–5 的 R05（母座焊盘 3），每路可单独短接到 8 脚 GND 触发复位。使用 Zero 控制时，将 GPIO 配为开漏，拉低触发、切回高阻释放，关闭 GPIO 内部上拉。[核心板针脚与实测电平](../845-coreboard/README.md#short-group)

7 脚与 U9 的开漏复位输出共线。外部控制器通过开漏输出拉低复位，释放时保持高阻。9 脚留空。Zero 使用独立电源，通过杜邦线连接所需信号和公共地。10 脚提供 3.3 V 辅助输出。

11–22 脚按核心板方向标注。外接八路 TTL UART 模块使用其中六路，各槽 TX 接模块 RX，各槽 RX 接模块 TX，模块地接 23 或 24 脚。模块逻辑电平按核心板金手指实测值选择。风扇使用独立两针 J8。

PCB 顶面的 J11 中心为 (106.325, 22.39) mm，长边沿 Y 轴。靠板下边的 1、2 脚中心位于 Y = 8.42 mm，与 Zero 排针下端对齐；1 脚为方形焊盘。24 针均已与原理图网表核对，两列之间留有走线禁区。试装时核对插满核心板后的插头高度、出线方向和插拔净空。
