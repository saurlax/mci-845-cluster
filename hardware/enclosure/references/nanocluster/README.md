# NanoCluster Enclosure Reference

## Source

本地原件为 Sinky 的 [Sipeed nanoCluster 外壳](https://makerworld.com.cn/zh/models/1311487-sipeed-nanocluster-wai-ke)，由 [Sipeed 安装文档](https://wiki.sipeed.com/hardware/en/cluster/NanoCluster/use.html#Hardware-Installation)链接。作者说明可使用原机配件安装。

| Item | Value |
| --- | --- |
| Author | Sinky |
| Original file | `sinky-nanocluster-case.3mf` |
| Original size | 622435 bytes |
| License recorded in 3MF | Standard Digital File License |
| Local inspection date | 2026-11-20 |
| Mesh parts | 2；均为封闭网格、各一个连通实体 |

3MF 包含两件壳体网格、缩略图、切片配置及组件变换。原文件完整保存。两个 STL 是直接提取的局部坐标网格；GLB 使用 3MF 组件摆放变换生成，以便查看内侧结构，未把展开姿态解释为合拢后的外形。原始两件网格的 X 向宽度均为 69 mm。衍生检查数据见 [Model checks](model-check.json)。第三方原件及预览仅保存在本地参考目录，由本目录的 `.gitignore` 排除；设计归属保留给原作者。

[Original 3MF](sinky-nanocluster-case.3mf) · [Interactive parts](sinky-nanocluster-parts.glb) · [Inner view](reference-inner.png) · [Source thumbnail](sinky-model-preview.png)

## Observations

模型采用两件包覆式结构。上壳有连续顶面、侧壁、内侧横向加强筋和端部通风格栅；下壳可见承托结构、圆形固定柱、三角加强筋、侧边成排矩形开口及底部操作开孔。原件缩略图显示两半壳合拢后形成完整小机箱，风扇位于端部开口。

另一个 [Noctua Edition](https://www.printables.com/model/1376174-sipeed-nanocluster-case-noctua-edition/files) 由 meteyou 发布。已读取发布页和文件列表：三件 STL（Bottom、Top、Grill）、Fusion F3Z 和 STEP。作者说明使用 60 × 60 × 25 mm Noctua NF-A6x25 5V PWM 风扇、改进铰链／卡扣、底部 Slot 1 BOOT 和 RESET 开孔，设计打印材料为 ABS。该版本的文件尚未保存到本目录。

## Recommendations for MCI 845 Cluster

保留当前托盘和六孔 PCB 固定方式，在上方增加可拆 U 形罩，把顶部和两侧形成连续风道。靠网口一端增加大面积出风口，接口保留独立开口。风扇与端框仍由底座承受载荷，四颗短款风扇自攻螺丝从外侧拧入，内侧不加会碰到 845 的螺母。

上盖先采用定位舌加两颗外露螺丝，便于频繁拆装及调整公差。外壳跨距按 140 mm 底板重新设计，长侧壁增加筋位；罩内筋位放在 845 和散热片包络以外。NanoCluster 的 69 mm 宽壳体与六块 845、7020 风扇的孔位和布局不同，参考其分件和连接方式，按本项目模型重建尺寸。

核心板顶部可另做可拆限位横梁，轻限制卡片摆动，避开散热片并留取卡空间。Zero 的上方安装区域采用独立可拆扩展盖，按最终铜柱及散热片高度确定内部净空。底部保留操作孔和风扇线缆卡位，并为上盖、PCB 和风扇保留各自的独立拆装路径。
