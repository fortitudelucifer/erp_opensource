# 📚 系统功能演示手册 / System User Guide

本手册结合真实系统截图，为您详细介绍 **工业流程 ERP 系统 (开源版)** 的各个核心功能板块。

---

## 0. 🛠️ 零基础部署手册 (Zero-to-Hero Deployment Guide)

本手册专为非技术背景的管理者/用户设计，涵盖了从**“一键模拟体验”**到**“生产环境托管”**的全流程指南。

### 🚀 阶段一：一键模拟体验 (1分钟上手)

如果您只是想快速体验系统功能，无需配置复杂的 SQL Server 数据库，我们提供了一个**“安全模拟模式”**。

1. **下载源码**: 点击 GitHub 页面右上角的 `Code` -> `Download ZIP`，解压到您的电脑 (例如 `D:\erp_opensource`)。
2. **安装 Python**: 访问 [Python官网](https://www.python.org/downloads/) 下载并安装 Python 3.8+ (安装时务必勾选 `"Add Python to PATH"`).
3. **安装依赖**: 双击打开文件夹，在地址栏输入 `cmd` 回车，运行以下命令（如果不确定是否安装了 git，可手动下载）：
   ```bash
   pip install -r requirements.txt
   ```
4. **启动模拟**:
   ```bash
   python simulate_deploy.py
   ```
5. **访问**: 打开浏览器访问 `http://127.0.0.1:8080` (账号: `admin` / 密码: `123456`)。
   > **注意**: 模拟模式使用的是临时 SQLite 数据库，数据重启后可能会丢失，仅供演示！
   >

---

### 🏭 阶段二：生产环境部署 (正式使用)

当您决定正式投入生产使用时，请按照以下步骤配置。

#### 1. 环境准备 (Prerequisites)

- **Python 3.8+**: 确保已安装。
- **Git** (可选): 推荐安装 [Git for Windows](https://git-scm.com/download/win) 以便后续更新。
- **SQL Server 2022 Developer**: 微软提供的免费开发者版数据库。
  - [下载链接](https://www.microsoft.com/zh-cn/sql-server/sql-server-downloads) -> 选择 "Developer" 版本。
  - 安装时选择 **"基本 (Basic)"** 安装即可。
  - 安装完成后，点击 **"安装 SSMS"** (SQL Server Management Studio) 以便图形化管理数据库。
  - **安装参考链接**：https://www.bilibili.com/video/BV13o4y1V7Jb?spm_id_from=333.788.videopod.episodes&vd_source=d49e0c134bc6c6180dab2a3de3c221f0

#### 2. 初始化数据库 (Database Setup)

1. 打开 **SSMS (SQL Server Management Studio)**，连接到您的本地数据库实例 (通常直接点“连接”)。
2. 点击工具栏的 **"新建查询 (New Query)"**。
3. 复制并执行以下 SQL 语句（选中代码按 `F5` 执行）：

   ```sql
   -- 1. 创建数据库
   CREATE DATABASE ERP_PROD;
   GO

   -- 2. 创建登录账号 (请修改您的密码!)
   CREATE LOGIN erp_user WITH PASSWORD = 'StrongPassword123!';
   GO

   -- 3. 赋予权限
   USE ERP_PROD;
   GO
   CREATE USER erp_user FOR LOGIN erp_user;
   GO
   ALTER ROLE db_owner ADD MEMBER erp_user;
   GO
   ```

#### 3. 配置系统 (Configuration)

1. 在项目根目录，找到 `config.example.py`，将其复制一份并重命名为 `config.py`。
2. 用记事本或 VS Code 打开 `config.py`，修改以下关键项：

   ```python
   # 生成一个随机密钥 (随便敲一串乱码都行)
   SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY_HERE'

   # 修改数据库连接字符串 (对应上面的数据库设置)
   # 格式: mssql+pyodbc://用户名:密码@主机地址/数据库名?driver=ODBC+Driver+17+for+SQL+Server
   SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://erp_user:StrongPassword123!@localhost/ERP_PROD?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes'

   # 修改公司名称
   COMPANY_NAME = "您的工厂名称"
   ```
3. **初始化表结构**:
   在 CMD 中运行一次：

   ```bash
   python run.py
   ```

   看到 `Running on http://0.0.0.0:8000` 表示配置成功，表结构已自动创建。**此时按 `Ctrl+C` 停止运行**，我们准备配置下一阶段。

---

### 🛡️ 阶段三：Windows 服务托管 (无人值守)

为了让 ERP 像 Windows 系统服务一样开机自启、奔溃重启，我们使用 `NSSM` 工具。

1. **下载 NSSM**: 访问 [NSSM 官网](https://nssm.cc/download) 下载最新版 (如 2.24)。
2. **解压**: 将 `win64` 文件夹下的 `nssm.exe` 复制到您的 ERP 项目目录 (例如 `D:\erp_opensource\`)。
3. **安装服务**:
   以**管理员身份**打开 CMD (右键开始菜单 -> Windows PowerShell (管理员))，进入项目目录，运行：
   ```bash
   .\nssm.exe install MyERPService
   ```
4. **在弹出的窗口中填写**:
   - **Path**: 选择您的 python.exe (例如 `C:\Python39\python.exe` 或虚拟环境中的 `python.exe`)。
     - _提示_: 在 CMD 输入 `where python` 可查看路径。
   - **Startup directory**: 您的项目目录 (例如 `D:\erp_opensource`).
   - **Arguments**: `wsgi.py`
5. **点击 "Install service"**。
6. **启动服务**:
   ```bash
   .\nssm.exe start MyERPService
   ```

   🎉 **恭喜！** 您的 ERP 现在已在后台静默运行。即使您注销或重启电脑，它也会自动启动。访问 `http://127.0.0.1:8000` 即可使用。

---

### 🌍 阶段四：零成本异地访问 (Tailscale)

既然部署在内网，如何在家里或出差时访问？

1. **注册 Tailscale**: 访问 [tailscale.com](https://tailscale.com/) 使用微软/谷歌账号注册。
2. **安装客户端**:
   - **服务器端**: 在运行 ERP 的电脑上安装 Tailscale 并登录。
   - **客户端**: 在您的笔记本、手机上安装 Tailscale 并登录同一账号。
3. **获取域名**: Tailscale 会为您分配一个固定的机器名 (Machine Name) 和 IP。
   - 在 Tailscale 控制台查看分配的域名 (MagicDNS)，例如 `https://win-server.tail-scale.ts.net`。
4. **更新 Config**:
   修改 `config.py`：
   ```python
   APP_BASE_URL = 'http://您的TailscaleIP:8000'
   # 或者如果您配置了 Tailscale Funnel，可以直接填域名
   ```
5. **大功告成**: 无论您身在何处，只要连上 Tailscale，就能像在公司一样安全访问 ERP。

---

### ❓ 常见问题 (Troubleshooting)

**Q1: 启动时报错 `Non-UTF-8 code`?**

- **原因**: Windows 上 Visual Studio/记事本有时候默认保存为 GBK 编码。
- **解决**: 使用 VS Code 打开报错的文件，点击右下角的编码格式，选择 **"Save with Encoding"** -> **"UTF-8"**。

**Q2: 报错 `socket access permission denied` 或端口被占用?**

- **解决**: 端口 8000 可能被其他软件占用了。请打开 `wsgi.py` (生产模式) 或 `run.py` (模拟模式)，将 `port=8000` 改为 `port=8080` 或其他数字。

**Q3: SQL Server 无法连接?**

- **检查**: 确保您启用了 SQL Server 的 TCP/IP 协议。
- **解决**: 搜索打开 **"Sql Server Configuration Manager"** -> **"SQL Server 网络配置"** -> **"MSSQLSERVER 的协议"** -> 右键 **"TCP/IP"** 选择 **"启用"**，然后重启 SQL Server 服务。

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
