# System Architecture

六块 MCI 845 核心板安装在同一块集群底板上。Slot 0 运行集群管理软件，Slot 1–5 作为工作节点。原理图、PCB 布局、装配文档和管理软件统一使用以下槽位编号。

| Slot | Connector | Role |
| --- | --- | --- |
| Slot 0 | J1 | 管理节点 |
| Slot 1 | J2 | 工作节点 |
| Slot 2 | J3 | 工作节点 |
| Slot 3 | J4 | 工作节点 |
| Slot 4 | J5 | 工作节点 |
| Slot 5 | J6 | 工作节点 |

底板的[网络拓扑](../hardware/README.md#panel-and-ethernet)、[供电分配](../hardware/README.md#dc-power)和 [J11 管理排针（UART、复位和辅助供电）](../hardware/design/management-header.md)见各自的设计说明。控制软件的集成计划见 [Cluster Controller](../software/controller/README.md)。
