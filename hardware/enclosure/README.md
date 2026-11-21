# Enclosure and Mounting

在此目录维护外壳、核心板支架和风扇座的可编辑 CAD 源文件。打样时随对应的底板版本发布可切片的 STL 或 3MF。

当前可打印方案为 [Printed Base](printed-base.md)：172 × 77 mm 低边托盘加可拆 7020 风扇面板，PCB 固定在六个支撑柱上，风扇通过四颗短款风扇自攻螺丝固定到面板，面板用两颗 M3 螺丝连接托盘。[装配预览](printed-base-assembly.png) · [三维装配](printed-base-140x65-7020.glb) · [托盘 STL](printed-base-tray.stl) · [面板 STL](printed-base-fan-panel.stl)。

[Container Style Concept](container-style.md) 在当前装配外增加集装箱风格波纹上罩、角框和双门式出风端，提供外观草案及 STEP，供后续外壳结构设计参考。[Concept preview](container-style-concept.png) · [Interactive concept](container-style-concept.glb)。

当前装配采用 **70 × 70 × 20 mm 7020 风扇**，型号为 Delta AFC0712DD-TP10。140 × 65 mm 底板、7020 风扇及板上器件已同步至 EDA 主工程。Zero 和铜柱模型已移除，保留管理板安装孔。[Native EDA Assembly](mci-845-eda-assembly-140x65-7020.glb) · [Preview](eda-backplane-with-zero3w.png)

装配尺寸以底板板框、固定孔位、核心板间距和接口位置为准。打印设置和紧固件规格记录在[组装文档](../../docs/assembly.md)。

## Management Board

当前方案采用 [Four-Post Dupont Mount](zero-dupont-mount.md)：底板保留 Zero 四个安装孔及禁铜区，Zero 和铜柱模型已移除，用户可自行安装并用杜邦线连接。下方直插排母内容保留为历史试排。

[7020 Assembly](fan7020-fit.md) 将台达 AFC0712DD-TP10 官方模型装入 140 × 65 mm 试排版。风框两侧各伸出 PCB 2.5 mm，与左列 845 的最小实体净空为 2.115 mm。[最新三维装配](backplane-140x65-with-zero3w-7020.glb) · [装配预览](aligned65-7020-backplane-with-zero3w.png)。

[Aligned 65 mm Assembly](aligned65-fit.md) 是 140 × 65 mm 试排方案：带原装排针的 Zero 整板倒扣，前后与接口侧板边对齐，内侧由排母承托，外侧两个孔接铜柱；845 完整包络收进板框。[三维试排](backplane-140x65-with-zero3w.glb) · [俯视对齐图](aligned65-zero3w-top.png)。

[ZERO 3W Fit Study](zero3w-fit.md) 将 Radxa ZERO 3W 官方模型放在右侧接口区上方，记录板卡净空、20 mm 铜柱与支架方案，以及 40 pin 直插通道与 RJ45 的干涉。可打开[三维装配](backplane-with-zero3w.glb)或查看[装配预览](backplane-with-zero3w.png)。
