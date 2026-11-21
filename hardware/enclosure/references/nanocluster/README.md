# NanoCluster Enclosure Reference

## Sources

- Sinky 发布的 [Sipeed NanoCluster 外壳](https://makerworld.com.cn/zh/models/1311487-sipeed-nanocluster-wai-ke)，见 [Sipeed 安装文档](https://wiki.sipeed.com/hardware/en/cluster/NanoCluster/use.html#Hardware-Installation)。作者说明可使用原机配件安装。
- meteyou 发布的 [Noctua Edition](https://www.printables.com/model/1376174-sipeed-nanocluster-case-noctua-edition/files)，适配 60 × 60 × 25 mm Noctua NF-A6x25 5V PWM 风扇，带改进的铰链、卡扣和底部 BOOT、RESET 开孔。

## Observations

NanoCluster 外壳分成两件。上壳有连续顶面、侧壁、加强筋和端部通风格栅；下壳提供承托、固定柱、侧边开口和底部操作孔。

## Recommendations for MCI 845 Cluster

保留当前托盘和六孔 PCB 固定方式，在上方增加可拆 U 形罩，把顶部和两侧形成连续风道。靠网口一端增加大面积出风口，接口保留独立开口。风扇与端框仍由底座承受载荷，四颗短款风扇自攻螺丝从外侧拧入，内侧不加会碰到 845 的螺母。

上盖先采用定位舌加两颗外露螺丝，便于频繁拆装及调整公差。外壳跨距按 140 mm 底板重新设计，长侧壁增加筋位；罩内筋位放在 845 和散热片包络以外。NanoCluster 的壳体与六块 845、7020 风扇的孔位和布局不同，参考其分件和连接方式，按本项目模型重建尺寸。

核心板顶部可另做可拆限位横梁，轻限制卡片摆动，避开散热片并留取卡空间。Zero 的上方安装区域采用独立可拆扩展盖，按最终铜柱及散热片高度确定内部净空。底部保留操作孔和风扇线缆卡位，并为上盖、PCB 和风扇保留各自的独立拆装路径。
