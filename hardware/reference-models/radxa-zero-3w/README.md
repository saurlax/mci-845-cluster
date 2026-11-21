# Radxa ZERO 3W Mechanical Reference

`radxa-zero-3w-v1.11.step` 是 Radxa 官方 ZERO 3W V1.11 STEP 模型，包含 PCB、接口、元件和朝元件面伸出的 40 pin 排针。模型原始坐标和几何保持原样。

## Source

下载并解压官方压缩包，将 STEP 保存为本目录的 `radxa-zero-3w-v1.11.step`。

- [Official hardware downloads](https://docs.radxa.com/en/zero/zero3/download)
- [Original STEP archive](https://dl.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_3d_stp.zip)
- 获取日期：2026-11-19。
- STEP SHA-256：`1eac96aa8804f7270e08610ebd99bf0eccfd26d39d859fae76d119406694ded3`。

## Coordinates

单位为 mm。PCB 名义范围为 X = 0–65、Y = 0–30；元件面 Z = 0，板底约 Z = −1.6。排针两行中心 Y = 25.405 和 27.945，各行 X = 8.32–56.58，间距 2.54。排针塑胶体范围 X = 7.05–57.85、Y = 24.135–29.215，针尖最高 Z = 8.5。

模型中的四个安装孔为 Ø2.8 mm，中心约为 `(3.55, 3.60)`、`(3.60, 26.45)`、`(61.40, 3.60)`、`(61.40, 26.50)`。机械布局采用这些模型坐标；采购后的实板版本和连接器尺寸按实物复核。

## Assembly Study

底板固定孔和接线方式见 [Zero Mount](../../enclosure/assembly/zero-dupont-mount.md)。
