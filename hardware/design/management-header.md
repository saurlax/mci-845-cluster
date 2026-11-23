# Management Header

J11 是 2×12、2.54 mm 双排直插公针，型号为 Samtec TSW-112-07-G-D，提供六槽 UART、六槽复位、交换机复位、5 V、3.3 V 和公共地。使用杜邦线按信号名连接 Zero。方形焊盘为 1 脚。

| Odd pin | Signal | Even pin | Signal |
| --- | --- | --- | --- |
| 1 | S0_RESET | 2 | S1_RESET |
| 3 | S2_RESET | 4 | S3_RESET |
| 5 | S4_RESET | 6 | S5_RESET |
| 7 | SW_RESET_N | 8 | GND |
| 9 | SYS_5V | 10 | SW_3V3 |
| 11 | S0_UART_TX | 12 | S0_UART_RX |
| 13 | S1_UART_TX | 14 | S1_UART_RX |
| 15 | S2_UART_TX | 16 | S2_UART_RX |
| 17 | S3_UART_TX | 18 | S3_UART_RX |
| 19 | S4_UART_TX | 20 | S4_UART_RX |
| 21 | S5_UART_TX | 22 | S5_UART_RX |
| 23 | GND | 24 | GND |

J11 的 1–6 脚分别直连 SLOT 0–5 的 R05（母座焊盘 3），每路可单独短接到 8 脚 GND 触发复位。使用 Zero 控制时，将 GPIO 配为开漏，拉低触发、切回高阻释放，关闭 GPIO 内部上拉。[核心板针脚与实测电平](../845-coreboard/README.md#short-group)

7 脚与 U9 的开漏复位输出共线。外部控制器通过开漏输出拉低复位，释放时保持高阻。9 脚和 8 脚分别作为 Zero 的 5 V 电源和回流；10 脚为背板交换电源提供的 3.3 V 辅助输出。U2 的额定输出为 3 A。若给 Zero 预留 2 A，交换芯片的两路降压及其他 5 V 负载合计可用 1 A 输入预算。选用可持续通过 2 A 的针座、触点和线束，满载时在 Zero 电源针处测电压，并记录 U2 温升。[TPS54302 数据手册](https://www.ti.com/lit/ds/symlink/tps54302.pdf)

11–22 脚按核心板方向标注。外接八路 TTL UART 模块使用其中六路，各槽 TX 接模块 RX，各槽 RX 接模块 TX，模块地接 23 或 24 脚。模块逻辑电平按核心板金手指实测值选择。风扇使用独立两针 J8。

24 针封装已绑定到原理图。现有 PCB 为上一版 10 针布局，更新 PCB 时重新核对 Zero 下方的线束空间和插拔净空。
