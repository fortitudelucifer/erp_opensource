# 📚 系统功能演示手册 / System User Guide

本手册结合真实系统截图，为您详细介绍 **工业流程 ERP 系统 (开源版)** 的各个核心功能板块。

---

## 1. 认证与安全 (Authentication)

系统提供安全的登录与注册机制，支持多种角色（管理员、部门负责人、普通员工、客户）的权限隔离。

![认证界面](assets/auth.png)

---

## 2. 全局看板 (Dashboard)

采用 Bento Grid 风格的现代化仪表盘，直观呈现企业核心 KPI：
- **六色状态光效**: 生产中、进行中、延误、验收/问题、已验收、未启动。
- **关键指标**: 待办任务数、本月交付项目数、进行中合同总额等。

![系统首页](assets/base.png)

---

## 3. 项目与合同管理 (Project Management)

### 3.1 项目列表 (Project List)
以卡片或列表形式展示所有合同，支持按状态快速筛选。管理员可在此处一键创建新立项。

![项目列表](assets/list.png)

### 3.2 项目概览 (Project Overview)
点击任意项目进入详情页，这里是项目管理的“驾驶舱”。您可以查看项目基本信息、进度概况以及所有关联的子模块入口。

![项目概览](assets/overview.png)

### 3.3 销售与报价 (Sales Info)
记录合同的报价金额、成交日期及销售负责人，实现从销售端到生产端的无缝衔接。

![销售信息](assets/sales.png)

### 3.4 团队指派 (Team Assignment)
灵活的矩阵式管理。管理员可为每个项目指定各职能部门（机械、电气、软件等）的负责人，系统会自动通知相关人员。

![团队指派](assets/leaders.png)

---

## 4. 生产任务与排期 (Tasks & Scheduling)

### 4.1 任务管理 (Task Management)
核心生产环节的执行中心。支持任务的增删改查，实时更新进度（0% - 100%）。

![任务列表](assets/tasks.png)

### 4.2 任务概览与甘特图 (Task Overview)
可视化展示项目进度条和关键节点，帮助管理者把控整体工期。

![任务概览](assets/task_overview.png)

### 4.3 个人任务视图 (Personal View)
员工可专注查看“指派给我的”任务，减少信息干扰，提升执行效率。

![个人任务](assets/task_overview_person.png)

---

## 5. 供应链与交付 (Supply Chain & Delivery)

### 5.1 采购管理 (Procurement)
项目维度的采购清单管理。追踪物料的下单、到货状态，确保生产物料及时到位。

![采购管理](assets/procurements.png)

### 5.2 验收流程 (Acceptance)
支持多级验收体系（FAT 出厂验收 / SAT 现场验收）。质检人员可在线标记验收结果（通过/不通过）。

![验收记录](assets/acceptances.png)

### 5.3 售后反馈 (Feedback)
闭环管理的最后一环。记录客户在交付后的反馈与问题，并指派专人处理，支持追踪解决进度。

![售后反馈](assets/feedbacks.png)

---

## 6. 知识库与文件管理 (File Management)

系统自动为每个合同建立独立的文件归档空间。支持合同扫描件、技术图纸、验收报告的上传与版本管理，确保资料不丢失、不混淆。

![文件管理](assets/files.png)

---

## 7. 组织架构 (Organization)

### 7.1 部门管理 (Departments)
自定义企业职能部门（如研发部、采购部、生产部），构建清晰的组织树。

![部门管理](assets/departments.png)

### 7.2 人员档案 (Personnel)
维护员工详细信息（电话、邮箱、微信）。系统利用这些信息实现自动化的消息通知触达。

![人员档案](assets/persons.png)

---

## 8. 审计与通知 (Audit & Notification)

### 8.1 操作日志 (Operation Logs)
系统自带“黑匣子”，完整记录所有人员的增删改查操作，支持多维度追溯，保障数据安全。

![操作日志](assets/logs.png)

### 8.2 消息通知 (Notifications)
集成多通道通知（邮件、钉钉、企微），确保关键任务变动及时触达相关负责人。

![通知记录](assets/notify.png)
