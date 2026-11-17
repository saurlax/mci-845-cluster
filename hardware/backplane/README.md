# Cluster Backplane

在此目录存放完整的嘉立创 EDA 专业版 v4 文件夹工程。提交时保留工程索引（`.eprj3`）、原理图（`.esch2`）、PCB 布局（`.epcb2`）和工程引用的本地库文件。

## Planning Draft

在桌面客户端打开 [MCI 845 Backplane](mci-845-backplane/mci-845-backplane.eprj3)。`J1` 至 `J6` 分别对应 Slot 0 至 Slot 5，`J1` 为管理节点。每个槽位符号的 22 个触点沿用[核心板测量编号](../../docs/coreboard-connector.md)。确认针脚和母座型号后，再分配网络并关联实际封装。

六块核心板横向插入，按两列三行排列。左列从上到下为 Slot 0、1、2，右列为 Slot 3、4、5。6020 风扇在左侧，RJ45 上联口在右侧居中。

PCB 草图暂用 120 × 56 mm 板框，列内相邻两槽按约 18 mm 中心距排布。矩形标记装配预留区。板框、槽间净空和支撑位置随核心板及散热片实测尺寸调整。

## Fabrication

送厂时，从对应修订的工程导出 Gerber、贴片 BOM 和贴片坐标，并一起上传到对应的 GitHub Release。
