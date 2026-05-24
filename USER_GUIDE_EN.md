# 📚 System User Guide

This manual combines real system screenshots to introduce the core functional modules of **CORE ERP v3.0.0** in detail.

---

## 0. 🚀 Installation & Deployment

### One-Click Installer (Recommended)

CORE ERP provides a Windows one-click installer — no technical background required:

1. **Download** `CoreERP-Setup-v3.0.0.exe`
2. **Double-click to run** the installer, click "Yes" on the UAC prompt
3. Follow the wizard and click "Next", wait for installation to complete (about 30 seconds)
4. **Browser opens automatically** after installation

> **What you get after installation:**
> - ✅ CORE ERP runs as a Windows service in the background, starts on boot
> - ✅ Desktop shortcut — double-click to open the system
> - ✅ Firewall configured automatically — LAN devices can access directly
> - ✅ Data stored in `C:\CoreERP\data\` directory

### Source Code (Developers)

For developers who need to customize or debug:

```bash
git clone https://github.com/fortitudelucifer/erp_opensource.git
cd erp_opensource
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
# Visit http://127.0.0.1:8000
```

---

## 1. 🛠️ Setup Wizard — v3 New

On first launch, the system automatically enters the Setup Wizard to guide you through initialization:

### Step 1: Company Information
- Enter your **company name** — it will appear in the system title bar and navigation
- The system automatically generates a 6-digit **invite code** for employee registration verification

### Step 2: Admin Account
- Create the system administrator account (username + full name + password)
- This account has the highest privileges and can manage all features

### Step 3: Complete
- Click "Get Started" to enter the system dashboard
- The admin will see an **onboarding card** on first login (5-step quick start)

> ⚠️ The Setup Wizard only appears on first launch. Configuration is saved to `data/config.json` afterward.

---

## 2. 🎉 First-Login Onboarding — v3 New

After the admin logs in for the first time, an onboarding card appears at the top of the dashboard:

| Step | Content | Action |
|------|---------|--------|
| ① View Invite Code | Staff need this code to register | → Go to Settings |
| ② Create Staff Accounts | Create accounts and assign roles for each employee | → Go to User Management |
| ③ Share the LAN Address | Tell staff the address to access the system | Displays current URL |
| ④ Learn Core Features | Project management, org, operation logs | → Go to Help Center |
| ⑤ Done | You've mastered the basics | Dismiss guide |

Click "Don't show again" to permanently hide the onboarding card.

---

## 3. Authentication

The system provides secure login and registration mechanisms, supporting permission isolation for multiple roles.

### Login
- Supports login by username or full name
- Login page features brand logo and gradient background animation

### Register (Invite Code Required)
- Staff registration requires the **6-digit invite code** provided by the admin
- Fill in username, full name, phone number, WeCom ID, etc.
- Default role after registration is `employee`

### Role Permissions

| Role | Permission Scope |
|------|-----------------|
| **admin** | System administrator with all privileges |
| **boss** | General manager — view all data and reports |
| **manager** | Department manager — manage department projects and personnel |
| **employee** | Regular staff — view and handle assigned tasks |
| **customer** | Client — view related contract progress only |

![Auth Interface](assets/auth.png)

---

## 4. Dashboard

Adopts a Bento Grid style modern dashboard, intuitively presenting core KPIs:

- **Multi-dimensional Status Visualization**: Six-color light effects to semantically display project status
- **Key Metrics**: Total contracts, active, at-risk, delivered this month
- **Delivery Trend Chart**: ECharts line chart showing the past 6 months
- **Department Load Distribution**: ECharts pie chart showing task share by department
- **Recent Operation Logs**: Real-time display of the latest system actions
- **Quick Actions**: One-click to create a contract or view all projects

![Dashboard](assets/base.png)

---

## 5. Project & Contract Management

### 5.1 Project List

Displays all contracts in card or list format, supporting quick filtering by status. Administrators can create new projects here with one click.

![Project List](assets/list.png)

### 5.2 Project Overview

Click any project to enter the details page — the "cockpit" of project management. View basic info, progress overview, and entrances to all associated sub-modules.

![Project Overview](assets/overview.png)

### 5.3 Sales Info

Records contract quote amount, deal date, and sales person in charge, achieving seamless connection from sales to production.

![Sales Info](assets/sales.png)

### 5.4 Team Assignment

Flexible matrix management. Administrators can assign leaders for each functional department (Mechanical, Electrical, Software, etc.) for each project, and the system automates notifications.

![Team Assignment](assets/leaders.png)

---

## 6. Tasks & Scheduling

### 6.1 Task Management

The execution center of core production links. Supports adding, deleting, modifying, and checking tasks, updating progress in real-time (0% - 100%).

![Task List](assets/tasks.png)

### 6.2 Task Overview & Gantt Chart

Visually displays project progress bars and critical nodes, helping managers control the overall schedule.

![Task Overview](assets/task_overview.png)

### 6.3 Personal View

Employees can focus on "Tasks Assigned to Me", reducing information interference and improving execution efficiency.

![Personal View](assets/task_overview_person.png)

---

## 7. Supply Chain & Delivery

### 7.1 Procurement Management

Project-dimension procurement list management. Track material ordering and arrival status to ensure production materials arrive on time.

![Procurement](assets/procurements.png)

### 7.2 Acceptance Process

Supports multi-level acceptance system (FAT Factory Acceptance / SAT Site Acceptance). QC personnel can mark acceptance results online (Pass/Fail).

![Acceptance](assets/acceptances.png)

### 7.3 Feedback

The last link of closed-loop management. Record client feedback and issues after delivery, assign specific personnel to handle, and support tracking resolution progress.

![Feedback](assets/feedbacks.png)

---

## 8. Knowledge Base & File Management

The system automatically establishes an independent file archiving space for each contract. Supports upload and version management of contract scans, technical drawings, and acceptance reports, ensuring data is not lost or confused.

![File Management](assets/files.png)

---

## 9. Organization

### 9.1 Department Management

Customize enterprise functional departments (e.g., R&D, Purchasing, Production) to build a clear organization tree.

![Department Management](assets/departments.png)

### 9.2 Personnel Profile

Maintain detailed employee info (Phone, Email, WeChat). The system uses this info to achieve automated message notification delivery.

![Personnel](assets/persons.png)

---

## 10. Audit & Notification

### 10.1 Operation Logs

The system comes with a "Black Box" that completely records all personnel's addition, deletion, modification, and query operations, supporting multi-dimensional tracing to guarantee data security.

![Logs](assets/logs.png)

### 10.2 Notifications

Integrated multi-channel notifications (Email, DingTalk, WeCom) ensure critical task changes reach relevant responsible persons in time.

![Notifications](assets/notify.png)

---

## 11. 👥 User Management — v3 New

Accessible by **admin** and **boss** roles only (Navigation: "Admin → User Management").

### Features
- **View User List**: Username, full name, role, and registration time for all registered users
- **Create User**: Admin creates accounts for staff directly — no invite code needed
- **Edit User**: Modify user role, contact info, etc.
- **Delete User**: Remove accounts that are no longer needed
- **Role Assignment**: Choose from admin / boss / manager / employee / customer

---

## 12. ⚙️ System Settings — v3 New

Accessible by **admin** and **boss** roles only (Navigation: "Admin → System Settings"), with three tabs:

### Tab 1: Basic Settings
- **Company Name**: Change the company name shown in the system title bar
- **Invite Code Management**: View the current invite code, regenerate with one click

### Tab 2: Remote Access
Provides detailed tutorials for three remote access solutions:

| Solution | Difficulty | Cost |
|----------|------------|------|
| **Tailscale** (Recommended) | ⭐ Simple | Free |
| **FRP Tunnel** | ⭐⭐⭐ Medium | ~¥50-100/mo |
| **Cloud Server Deployment** | ⭐⭐⭐⭐ Advanced | ¥100-300/mo |

Each solution has collapsible step-by-step instructions and configuration examples.

### Tab 3: System Information
- **Service Status**: Shows Windows service status (Running / Stopped)
- **Uptime**: Shows how long the service has been running
- **Version Info**: Current version number
- **Restart Service**: One-click restart of CORE ERP service
- **About**: Version, tech stack, open source license, GitHub link

---

## 13. ❓ Help Center — v3 New

Accessible by all logged-in users (Navigation: "❓ Help").

### Features
- **Category Tags**: 🚀 Getting Started | 📋 Project Management | 👥 User & Permissions | 🔧 System Maintenance
- **FAQ Accordion**: Click a question to expand the answer, click again to collapse
- **15+ FAQs**: Covers everything from registration to data backup

### Sample FAQs
- How does admin create staff accounts?
- How to view and manage the invite code?
- How do staff register and log in?
- How can other computers on the LAN access the system?
- How to back up data?
- What to do if the service won't start?
- How to update to a new version?

---

## ❓ Troubleshooting

**Q1: "Access Denied" error during installation?**

- **Cause**: Installation requires admin privileges.
- **Solution**: Right-click the installer → "Run as Administrator".

**Q2: Other LAN computers can't access the system?**

- **Check**: Confirm both computers are on the same LAN (same Wi-Fi or wired network).
- **Solution**: Check if Windows Firewall allows port 8000 (the installer configures this automatically, but third-party firewalls may block it).

**Q3: Forgot the admin password?**

- **Solution**: Delete `C:\CoreERP\data\erp.db` and `C:\CoreERP\data\config.json`, then restart the service to re-initialize.
- ⚠️ **Warning**: This will erase all data. Back up the `data` folder first.

**Q4: How to back up data?**

- Periodically copy the `C:\CoreERP\data\` folder to a USB drive or cloud storage. The core data file is `data/erp.db`.

**Q5: How to update to a new version?**

- Back up the `data` folder → Download new installer → Install over existing directory → Data is preserved automatically.

**Q6: Port 8000 is occupied?**

- **Check**: Run `netstat -ano | findstr :8000` to find the occupying process.
- **Solution**: Modify the `--port` parameter in `launcher.py`, or close the program using the port.

**Q7: `Non-UTF-8 code` error on startup? (Developers)**

- **Solution**: In VSCode, convert the file encoding to **UTF-8 without BOM**.
