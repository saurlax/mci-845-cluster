# Assembly Models

主工程为 140 × 65 mm，当前装配包含六块 845 核心板和 Delta AFC0712DD-TP10 7020 风扇。Zero 3W、四根铜柱及直插排母模型均已移除，保留四个安装孔和禁铜区，供用户自行安装与接线。

## Local Library

当前机器的本地模型库为 `C:\Users\saurl\Documents\LCEDA-Pro\libraries`，模型文件已安装。在其他机器上，将本目录绑定的 STEP 文件复制到嘉立创 EDA 专业版配置的本地 3D 模型库，并更新工程模型绑定中的库路径。路径按 Windows 本地目录格式保存。

7020 模型来自台达官方 STEP。辅助排针为尺寸参考模型。Zero、铜柱与加高排母 STEP 保留为历史试排资源，当前工程已解除这些模型及其机械封装的引用。

## Component Packages

`model-bindings.csv` 和 `model-bindings.json` 记录电气元件及新增机械件的模型绑定。六块核心板共享 `mci-845-coreboard-vertical.step`。常规芯片、阻容、电感及连接器使用 EDA 目录中的封装模型，CH348L 使用 LQFP-100、14 × 14 mm 本体模型。保险、电感和辅助排针采用对应包络的参考模型。

模型补齐保留原有网络和 DNP 属性。底板仅保留 Zero 四个安装孔，无 Zero 或铜柱装配模型及直插 40 pin 排母。UART、RESET、电源的杜邦线连接、接口区重新布线及铺铜属于后续电气设计。

## Preview

[Native EDA Assembly](../../../enclosure/mci-845-eda-assembly-140x65-7020.glb) 由 EDA 原生三维导出转换，导出时关闭缺失模型自动生成。
