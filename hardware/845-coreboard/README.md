# MCI 845 Core Board

核心板装配模型用于外壳布置、接口开窗和 3D 展示。模型保留弹簧扣、散热片鳍片、22 触点连接器和 USB-C 接口，背面的元件和丝印按照片简化。

## JLCEDA Pro Library

[MCI 845 Mechanical](MCI%20845%20Mechanical.elib) 是嘉立创 EDA 专业版的本地器件库。三个器件各有独立符号、外形封装和 STEP 绑定，可放置到 PCB 上用于装配预览。封装无铜焊盘，器件不计入 BOM。

| Device | Placement Origin |
| --- | --- |
| MCI 845 Core Board | 竖插，原点在 SATA 插合端面的中心。背板母座的实际插合高度通过 3D 偏移校准 |
| MCI 845 Heatsink | 鳍片区中心，Z=0 为散热片底面 |
| MCI 845 Spring Push Pin | 扣脚轴线，Z=0 为扣脚尖端 |

本机客户端的库和 STEP 已安装到 `Documents/LCEDA-Pro/libraries`。迁移时，把 `.elib` 和 [`eda-models`](eda-models/) 内的三个 STEP 放进目标客户端配置的库目录，刷新器件库，再在封装的 3D 模型管理器中选中对应 STEP，核对放置原点。 [嘉立创 EDA 封装属性](https://prodocs.lceda.cn/cn/footprint/side-panel-left-property/)

## CAD Files

- [STEP assembly](mci-845-coreboard.step) 用于 CAD 导入和测量。
- [GLB assembly](mci-845-coreboard.glb) 用于彩色 3D 预览，文件单位为米。
- [CadQuery source](model.py) 可修改尺寸。用 CadQuery 2.8.0 执行 `python model.py`，重新生成整板模型和 `eda-models` 内各器件的 STEP。丝印使用 Arial 字体。

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
