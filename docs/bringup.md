# Bring-Up

以下是首版底板的调试顺序。输入电压、限流值、测试点和调试接口随底板修订记录。

1. 核对 [5 V 空焊位](../hardware/design/power/top-power-placement.md#unpopulated-5-v-supply)、电容极性及 J8 风扇线序，测量电源轨对地电阻。
2. 先单测空底板的 BUS_12V、3.3 V、1.1 V 及交换芯片复位释放。断电装入 Slot 0 后，验证启动、千兆协商和双向传输。
3. 参照 [mci-845-firmware](https://github.com/saurlax/mci-845-firmware) 的说明准备核心板，并记录实际使用的固件版本。
4. 逐槽加入 Slot 1–5，核对节点上线状态与物理槽位一致。
5. 按 [J11 针位](../hardware/design/management-header.md)逐槽拉低复位，观察对应 UART 启动日志和其他五槽的运行状态。六槽满载时记录输入电流、各槽电压及供电路径温升。
