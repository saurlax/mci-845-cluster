# 7020 Fan Fit

台达 AFC0712DD-TP10 风扇安装在 140 × 65 mm 底板的核心板一侧。[装配预览](README.md) · [测量数据](checks/fan7020-fit.json)

## Placement

单位为 mm，沿用背板 EDA 原点，背板顶面为 Z = 0。风扇厚度沿 X，机内侧端面保持 X = −7，名义气流方向为 +X，从左向右经过核心板。安装时按实物风向箭头确定进出风面。

| Feature | Placement |
| --- | --- |
| Fan frame envelope | X = −27–−7；Y = −2.5–67.5；Z = 0–70 |
| Frame center, Y / Z | 32.5 / 35 |
| Minimum distance to Slot 0 / 1 / 2 | 均为 2.115 mm，STEP 实体表面测距 |
| Frame overhang beyond 65 mm PCB width | 两侧各 2.5 mm |
| Frame top above 845 top | 约 5.15 mm |
| Mounting-hole pitch | 61.5 × 61.5 mm |
| Mounting-hole diameter | Ø4.3 mm |
| Hole axes, Y / Z | (1.75, 4.25)、(63.25, 4.25)、(1.75, 65.75)、(63.25, 65.75) |

当前实体模型显示风扇与核心板之间有净空。底座风扇面板需容纳 70 mm 风框，并为减振垫、线缆和紧固件留空间。厂商 STEP 为外形包络模型，预览沿用其简化几何。

## Source

净空依据风框和左列三块核心板的 STEP 实体测量。官方模型与下载信息见 [Delta Mechanical Reference](../../reference-models/delta-7020/README.md)；安装零件见 [Printed Base](../printed-base/README.md)。
