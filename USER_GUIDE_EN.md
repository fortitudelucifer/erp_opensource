# 📚 System User Guide

This manual combines real system screenshots to introduce the core functional modules of the **Industrial Flow ERP System (Open Source Edition)** in detail.

---

## 0. 🛠️ Zero-to-Hero Deployment Guide

Designed for non-technical managers/users, this guide covers the entire process from **"One-Click Simulation"** to **"Production Environment Hosting"**.

### 🚀 Phase 1: One-Click Simulation (Start in 1 Minute)

If you just want to quickly experience the system functions without configuring a complex SQL Server database, we provide a **"Safe Simulation Mode"**.

1.  **Download Source**: Click `Code` -> `Download ZIP` on the GitHub page and unzip it to your computer (e.g., `D:\erp_opensource`).
2.  **Install Python**: Visit [Python Official Site](https://www.python.org/downloads/) to download and install Python 3.8+ (Make sure to check `"Add Python to PATH"` during installation).
3.  **Install Dependencies**: Open the folder, type `cmd` in the address bar and press Enter, then run the following command (if you are unsure if git is installed, you can download it manually):
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start Simulation**:
    ```bash
    python simulate_deploy.py
    ```
5.  **Access**: Open a browser and visit `http://127.0.0.1:8080` (Account: `admin` / Password: `123456`).
    > **Note**: Simulation mode uses a temporary SQLite database. Data may be lost after restart and is for demonstration only!

---

### 🏭 Phase 2: Production Deployment (Formal Use)

When you decide to put it into formal production use, please configure it as follows.

#### 1. Prerequisites

- **Python 3.8+**: Ensure it is installed.
- **Git** (Optional): Recommended to install [Git for Windows](https://git-scm.com/download/win) for future updates.
- **SQL Server 2022 Developer**: Free developer edition database provided by Microsoft.
  - [Download Link](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) -> Select "Developer" version.
  - Select **"Basic"** installation.
  - After installation, click **"Install SSMS"** (SQL Server Management Studio) for graphical database management.
  - **Installation Reference**: https://www.bilibili.com/video/BV13o4y1V7Jb?spm_id_from=333.788.videopod.episodes&vd_source=d49e0c134bc6c6180dab2a3de3c221f0

#### 2. Database Setup

1.  Open **SSMS (SQL Server Management Studio)** and connect to your local database instance (usually just click "Connect").
2.  Click **"New Query"** on the toolbar.
3.  Copy and execute the following SQL statement (Select code and press `F5`):

    ```sql
    -- 1. Create Database
    CREATE DATABASE ERP_PROD;
    GO

    -- 2. Create Login Account (Please change your password!)
    CREATE LOGIN erp_user WITH PASSWORD = 'StrongPassword123!';
    GO

    -- 3. Grant Permissions
    USE ERP_PROD;
    GO
    CREATE USER erp_user FOR LOGIN erp_user;
    GO
    ALTER ROLE db_owner ADD MEMBER erp_user;
    GO
    ```

#### 3. Configuration

1.  In the project root directory, find `config.example.py`, copy it and rename it to `config.py`.
2.  Open `config.py` with Notepad or VS Code and modify the following key items:

    ```python
    # Generate a random secret key (Any random string works)
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY_HERE'

    # Modify database connection string (Corresponds to database settings above)
    # Format: mssql+pyodbc://username:password@host/dbname?driver=ODBC+Driver+17+for+SQL+Server
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://erp_user:StrongPassword123!@localhost/ERP_PROD?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes'

    # Modify Company Name
    COMPANY_NAME = "Your Factory Name"
    ```

3.  **Initialize Table Structure**:
    Run once in CMD:
    ```bash
    python run.py
    ```
    Seeing `Running on http://0.0.0.0:8000` means configuration is successful and table structures are automatically created. **Press `Ctrl+C` to stop running**, we are ready for the next stage.

---

### 🛡️ Phase 3: Windows Service Hosting (Unattended)

To make ERP start automatically on boot and restart on crash like a Windows system service, we use the `NSSM` tool.

1.  **Download NSSM**: Visit [NSSM Official Site](https://nssm.cc/download) to download the latest version (e.g., 2.24).
2.  **Unzip**: Copy `nssm.exe` from the `win64` folder to your ERP project directory (e.g., `D:\erp_opensource\`).
3.  **Install Service**:
    Open CMD as **Administrator** (Right click Start Menu -> Windows PowerShell (Admin)), enter project directory, and run:
    ```bash
    .\nssm.exe install MyERPService
    ```
4.  **Fill in the popup window**:
    - **Path**: Select your python.exe (e.g., `C:\Python39\python.exe` or `python.exe` in virtual env).
      - _Tip_: Type `where python` in CMD to check path.
    - **Startup directory**: Your project directory (e.g., `D:\erp_opensource`).
    - **Arguments**: `wsgi.py`
5.  **Click "Install service"**.
6.  **Start Service**:
    ```bash
    .\nssm.exe start MyERPService
    ```
    🎉 **Congratulations!** Your ERP is now running silently in the background. Even if you log out or restart the computer, it will start automatically. Visit `http://127.0.0.1:8000` to use.

---

### 🌍 Phase 4: Zero-Cost Remote Access (Tailscale)

Since it is deployed on the intranet, how to access it from home or on a business trip?

1.  **Register Tailscale**: Visit [tailscale.com](https://tailscale.com/) to sign up with a Microsoft/Google account.
2.  **Install Client**:
    - **Server Side**: Install Tailscale on the computer running ERP and log in.
    - **Client Side**: Install Tailscale on your laptop or phone and log in to the same account.
3.  **Get Domain**: Tailscale will assign you a fixed Machine Name and IP.
    - Check the assigned domain (MagicDNS) in Tailscale console, e.g., `https://win-server.tail-scale.ts.net`.
4.  **Update Config**:
    Modify `config.py`:
    ```python
    APP_BASE_URL = 'http://YourTailscaleIP:8000'
    # Or if you configured Tailscale Funnel, you can fill in the domain directly
    ```
5.  **Done**: Wherever you are, as long as you connect to Tailscale, you can access ERP safely as if you were in the company.

---

### ❓ Troubleshooting

**Q1: `Non-UTF-8 code` error on startup?**

- **Cause**: Windows Visual Studio/Notepad sometimes saves files in GBK encoding by default.
- **Solution**: Open the error file with VS Code, click the encoding format in the lower right corner, select **"Save with Encoding"** -> **"UTF-8"**.

**Q2: `socket access permission denied` or port occupied?**

- **Solution**: Port 8000 might be occupied by other software. Please open `wsgi.py` (Production Mode) or `run.py` (Simulation Mode), change `port=8000` to `port=8080` or other numbers.

**Q3: SQL Server connection failed?**

- **Check**: Make sure you enabled TCP/IP protocol for SQL Server.
- **Solution**: Open **"Sql Server Configuration Manager"** -> **"SQL Server Network Configuration"** -> **"Protocols for MSSQLSERVER"** -> Right click **"TCP/IP"** and select **"Enable"**, then restart SQL Server service.

---

## 1. Authentication

The system provides secure login and registration mechanisms, supporting permission isolation for multiple roles (Admin, Dept Leader, Staff, Client).

![Auth Interface](assets/auth.png)

---

## 2. Dashboard

Adopts a Bento Grid style modern dashboard, intuitively presenting core customized KPIs:

- **Six-color Status Light**: Production, Processing, Risk, Issue, Accepted, Unstarted.
- **Key Metrics**: Pending Tasks, Projects Delivered This Month, Active Contract Total, etc.

![Dashboard](assets/base.png)

---

## 3. Project & Contract Management

### 3.1 Project List

Displays all contracts in card or list format, supporting quick filtering by status. Administrators can create new projects here with one click.

![Project List](assets/list.png)

### 3.2 Project Overview

Click any project to enter the details page. This is the "Cockpit" of project management. You can view project basic info, progress overview, and entrances to all associated sub-modules.

![Project Overview](assets/overview.png)

### 3.3 Sales Info

Records contract quote amount, deal date, and sales person in charge, achieving seamless connection from sales to production.

![Sales Info](assets/sales.png)

### 3.4 Team Assignment

Flexible matrix management. Administrators can assign leaders for each functional department (Mechanical, Electrical, Software, etc.) for each project, and the system automates notifications.

![Team Assignment](assets/leaders.png)

---

## 4. Tasks & Scheduling

### 4.1 Task Management

The execution center of core production links. Supports adding, deleting, modifying, and checking tasks, updating progress in real-time (0% - 100%).

![Task List](assets/tasks.png)

### 4.2 Task Overview & Gantt Chart

Visually displays project progress bars and critical nodes, helping managers control the overall schedule.

![Task Overview](assets/task_overview.png)

### 4.3 Personal View

Employees can focus on "Tasks Assigned to Me", reducing information interference and improving execution efficiency.

![Personal View](assets/task_overview_person.png)

---

## 5. Supply Chain & Delivery

### 5.1 Procurement Management

Project-dimension procurement list management. Track material ordering and arrival status to ensure production materials arrive on time.

![Procurement](assets/procurements.png)

### 5.2 Acceptance Process

Supports multi-level acceptance system (FAT Factory Acceptance / SAT Site Acceptance). QC personnel can mark acceptance results online (Pass/Fail).

![Acceptance](assets/acceptances.png)

### 5.3 Feedback

The last link of closed-loop management. Record client feedback and issues after delivery, assign specific personnel to handle, and support tracking resolution progress.

![Feedback](assets/feedbacks.png)

---

## 6. Knowledge Base & File Management

The system automatically establishes an independent file archiving space for each contract. Supports upload and version management of contract scans, technical drawings, and acceptance reports, ensuring data is not lost or confused.

![File Management](assets/files.png)

---

## 7. Organization

### 7.1 Department Management

Customize enterprise functional departments (e.g., R&D, Purchasing, Production) to build a clear organization tree.

![Department Management](assets/departments.png)

### 7.2 Personnel Profile

Maintain detailed employee info (Phone, Email, WeChat). The system uses this info to achieve automated message notification reach.

![Personnel](assets/persons.png)

---

## 8. Audit & Notification

### 8.1 Operation Logs

The system comes with a "Black Box" that completely records addition, deletion, modification, and query operations of all personnel, supporting multi-dimensional tracing to guarantee data security.

![Logs](assets/logs.png)

### 8.2 Notifications

Integrated multi-channel notifications (Email, DingTalk, WeCom) ensure critical task changes reach relevant responsible persons in time.

![Notifications](assets/notify.png)
