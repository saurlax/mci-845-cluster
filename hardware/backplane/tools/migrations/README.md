# Backplane Migration Scripts

这些脚本记录从早期工程迁移模型、移动顶面供电器件和调整 Zero 安装孔的过程。脚本会写入 EDA 工程和本地模型库，适用于对应的迁移前快照。日常编辑从 [EDA 主工程](../../mci-845-backplane/mci-845-backplane.eprj3) 开始。

重跑 `integrate-models.py` 时，从 [Radxa 官方来源](../../../reference-models/radxa-zero-3w/README.md#source)下载并核对 STEP，将解压文件保存为 `hardware/reference-models/radxa-zero-3w/radxa-zero-3w-v1.11.step`。在对应的主工程快照中执行脚本，并将迁移前的试排工程目录作为位置参数传入。
