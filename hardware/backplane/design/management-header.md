# Management Header

管理接口采用 **2×10、2.54 mm 双排直插公针**。从元件面看，1、2 为丝印标记端的同一列。使用杜邦线按信号名连接 Zero。六路 UART 经 CH348L 走独立的 USB-C。

| Odd Pin | Signal | Even Pin | Signal |
| ---: | --- | ---: | --- |
| 1 | SLOT0_RESET | 2 | GND |
| 3 | SLOT1_RESET | 4 | GND |
| 5 | SLOT2_RESET | 6 | GND |
| 7 | SLOT3_RESET | 8 | GND |
| 9 | SLOT4_RESET | 10 | GND |
| 11 | SLOT5_RESET | 12 | GND |
| 13 | SW_MDC | 14 | SW_MDIO |
| 15 | SW_RESET_N | 16 | SW_INT |
| 17 | FAN_PWM | 18 | FAN_TACH |
| 19 | AUX_5V | 20 | AUX_3V3 |

20 针分配为 12 根信号、2 根辅助电源和 6 根 GND。接线时，电源回线可接就近的 12 脚 GND。该针位为底板自定义分配。可参考 [Samtec TSW-110-07-G-D](https://www.samtec.com/products/tsw-110-07-g-d) 的机械规格。

## Board Integration

主工程与 140 × 65 mm 试排版均已将 J11 改为 20 孔通孔封装。中心位于 X = 101.50、Y = 51.50 mm，长边沿 Y 轴，1 脚位于靠风扇的一排、Y 较小的一端。1–14 脚已在原理图和 PCB 中分配网络，待布线。15–20 脚预留。

| Slot | Core Connector | Isolation Link | J11 Pin |
| --- | --- | --- | ---: |
| 0 | J1.3 (R05) | R37 | 1 |
| 1 | J2.3 (R05) | R38 | 3 |
| 2 | J3.3 (R05) | R39 | 5 |
| 3 | J4.3 (R05) | R40 | 7 |
| 4 | J5.3 (R05) | R41 | 9 |
| 5 | J6.3 (R05) | R42 | 11 |

R37–R42 为 0603、0 Ω，默认不装。确认核心板复位电平、触发极性和外部驱动方式后，再决定是否安装。

- 交换机复位已由板上的监控复位电路驱动，接入管理排针时需保证两路驱动相容，同时确认 SW_INT 的引脚模式、电平和极性。
- 现有 J8 提供 12 V 和 GND。PWM 和测速需配合四线风扇接口，按风扇规格校核信号电平、驱动与上拉。
- 辅助电源接入前按负载核算余量和限流。Zero 使用独立供电时，通过 GND 建立信号参考。
