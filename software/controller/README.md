# Cluster Controller

管理软件计划运行在 Slot 0 的 MCI 845 核心板上。第一版维护六个槽位的节点清单，并按槽位查询在线状态。槽位编号和角色见[系统架构](../../docs/architecture.md)。

硬件为每槽提供独立的低有效复位线。接入软件控制时，通过外部控制器以开漏方式驱动对应槽位。[J11 针位与接法](../../hardware/design/management-header.md)

部署配置和安装说明随软件一起维护。
