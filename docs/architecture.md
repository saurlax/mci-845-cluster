# System Architecture

六块 MCI 845 核心板安装在同一块集群底板上。Slot 0 运行集群管理软件，Slot 1–5 作为工作节点。原理图、PCB 布局、装配文档和管理软件统一使用以下槽位编号。

| Slot | Connector | Role | Network Port | Reset or Power Control |
| --- | --- | --- | --- | --- |
| Slot 0 | J1 | 管理节点 | 待定 | 待定 |
| Slot 1 | J2 | 工作节点 | 待定 | 待定 |
| Slot 2 | J3 | 工作节点 | 待定 | 待定 |
| Slot 3 | J4 | 工作节点 | 待定 | 待定 |
| Slot 4 | J5 | 工作节点 | 待定 | 待定 |
| Slot 5 | J6 | 工作节点 | 待定 | 待定 |

底板设计确定后，在这里记录供电入口和各槽供电方式、节点之间的网络拓扑，以及 Slot 0 访问复位或电源控制接口的方式。
