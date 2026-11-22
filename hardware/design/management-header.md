# Reset and Power Header

J11 是 2×5、2.54 mm 双排直插公针，提供六槽复位、交换机复位、5 V、3.3 V 和公共地。使用杜邦线按信号名连接 Zero。方形焊盘为 1 脚。

| Odd pin | Signal | Even pin | Signal |
| --- | --- | --- | --- |
| 1 | SLOT0_RESET | 2 | SLOT1_RESET |
| 3 | SLOT2_RESET | 4 | SLOT3_RESET |
| 5 | SLOT4_RESET | 6 | SLOT5_RESET |
| 7 | SW_RESET_N | 8 | GND |
| 9 | SYS_5V | 10 | SW_3V3 |

J11 的 1–6 脚分别直连 SLOT 0–5 的 R05（母座焊盘 3），由外部 GPIO 独立驱动。背板上这六路没有分压、上拉或下拉。GPIO 输出电压直接到达 R05，GPIO 高阻时由核心板和外部连接决定电平。首件在确认 R05 的允许输入电压后再主动驱动，并验证有效脉宽和复位释放。3.3 V 耐受性尚未确认。[核心板针脚与实测电平](../845-coreboard/README.md#short-group)

7 脚与 U9 的开漏复位输出共线。外部控制器通过开漏输出拉低复位，释放时保持高阻。9 脚和 8 脚分别作为 Zero 的 5 V 电源和回流；10 脚为背板交换电源提供的 3.3 V 辅助输出。U2 的额定输出为 3 A。若给 Zero 预留 2 A，交换芯片的两路降压及其他 5 V 负载合计可用 1 A 输入预算。选用可持续通过 2 A 的针座、触点和线束，满载时在 Zero 电源针处测电压，并记录 U2 温升。[TPS54302 数据手册](https://www.ti.com/lit/ds/symlink/tps54302.pdf)

十针已在原理图和 PCB 网表中分配网络，PCB 布线待完成。风扇使用独立两针 J8。[DC Power](../README.md#dc-power)

J11 暂摆在顶面，中心为 (102.00, 45.50) mm，长边沿 Y 方向，1 脚在左下。右列针脚中心进入 Zero 投影 0.27 mm，位置待确认，插头与 Zero 的高度净空待核对。
