# -*- coding: utf-8 -*-
"""
simulate_deploy.py - 模拟部署启动脚本 / Simulation Deployment Script

本脚本专门用于在本地进行"安全模拟"，它强制使用独立的 SQLite 数据库文件，
确保绝对不会连接到您的生产环境 SQL Server，也不会接触任何敏感数据。

This script is specifically for "safe simulation" locally. It forces the use of 
an independent SQLite database file, ensuring it NEVER connects to your 
production SQL Server or touches any sensitive data.
"""

import os
import sys
import random
from datetime import datetime, timedelta, date
from werkzeug.security import generate_password_hash

# 1. 配置环境 (Environment Setup)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# [关键] 强制指向本地临时数据库，覆盖任何其他配置
# [CRITICAL] Force point to local temporary DB, overriding all other configs
DB_FILE = os.path.join(BASE_DIR, 'simulation_safe.db')
os.environ['APP_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
os.environ['APP_SECRET_KEY'] = 'simulation-demo-key-123456'

# 导入应用 (必须在设置环境变量之后)
from core import create_app, db
from core.models import (
    User, Company, Contract, Department, Person, 
    Task, ProcurementItem, SalesInfo, Acceptance,
    Feedback, ProjectFile
)

app = create_app()

def init_demo_data():
    """初始化演示数据"""
    with app.app_context():
        # 总是尝试创建表（如果不存在）
        db.create_all()
        
        # 1. 初始化管理员
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("[-] [1/7] 创建管理员账户...")
            admin = User(
                username='admin',
                real_name='模拟管理员',
                email='admin@demo.local',
                phone='13800000000',
                wechat='demo_wechat',
                role='admin',
                password_hash=generate_password_hash('123456')
            )
            db.session.add(admin)
        
        # 2. 初始化部门
        dept_names = ['销售部', '研发部', '生产部', '采购部', '财务部', '售后服务部']
        depts = {}
        if Department.query.count() == 0:
            print("[-] [2/7] 创建部门架构...")
            for name in dept_names:
                d = Department(name=name)
                db.session.add(d)
                depts[name] = d
            db.session.commit()
        else:
            for d in Department.query.all():
                depts[d.name] = d

        # 3. 初始化人员
        persons_data = [
            ('张伟', '销售总监', '销售部'),
            ('李娜', '销售经理', '销售部'),
            ('王强', '研发总监', '研发部'),
            ('刘洋', '机械工程师', '研发部'),
            ('陈静', '电气工程师', '研发部'),
            ('赵敏', '采购经理', '采购部'),
            ('周杰', '采购专员', '采购部'),
            ('孙刚', '生产主管', '生产部'),
            ('吴平', '车间组长', '生产部'),
            ('郑快', '售后工程师', '售后服务部')
        ]
        
        persons = []
        if Person.query.count() == 0:
            print("[-] [3/7] 录入人员档案...")
            for name, title, dept_name in persons_data:
                if dept_name in depts:
                    p = Person(name=name, position=title, department_id=depts[dept_name].id)
                    db.session.add(p)
                    persons.append(p)
            db.session.commit()
        else:
            persons = Person.query.all()

        # 4. 初始化客户公司
        companies_data = ['未来科技有限公司', '蓝天重工集团', '东海造船厂', '华南精密制造', '北极星汽车工业', '中铁建设集团', '宏大化工股份']
        companies = []
        if Company.query.count() == 0:
            print("[-] [4/7] 建立客户档案...")
            for name in companies_data:
                c = Company(name=name)
                db.session.add(c)
                companies.append(c)
            db.session.commit()
        else:
            companies = Company.query.all()

        # 5. 初始化合同/项目 (涵盖所有请求的状态)
        # 状态列表: 生产中、进行中、已验收、未启动、延误、验收/问题
        contracts_data = [
            ('CORE-2025-001', '智能物流分拣系统', '未来科技有限公司', '生产中', 120),
            ('CORE-2025-002', '高精度数控机床改造', '蓝天重工集团', '进行中', 90),
            ('CORE-2025-003', '船舶自动化控制平台', '东海造船厂', '已验收', 180),
            ('CORE-2025-004', '精密零部件视觉检测线', '华南精密制造', '未启动', 60),
            ('CORE-2025-005', '新能源汽车电池包组装线', '北极星汽车工业', '延误', 150),
            ('CORE-2025-006', '化工反应釜监控系统', '宏大化工股份', '验收/问题', 100),
            ('CORE-2025-007', '高铁隧道通风控制系统', '中铁建设集团', '生产中', 200)
        ]
        
        contracts = []
        if Contract.query.count() == 0:
            print("[-] [5/7] 生成模拟项目合同...")
            for idx, (code, name, company_name, status, days) in enumerate(contracts_data):
                # 找到对应公司
                comp = next((c for c in companies if c.name == company_name), companies[0])
                
                # 计算日期
                start_date = date.today() - timedelta(days=random.randint(0, 60))
                delivery_date = start_date + timedelta(days=days)
                
                # 随机指派负责人
                our_mgr = persons[idx % len(persons)]
                
                c = Contract(
                    project_code=code,
                    contract_number=f'CTR-{datetime.now().year}-{idx+1:03d}',
                    name=name,
                    company_id=comp.id,
                    planned_delivery_date=delivery_date,
                    client_manager=f'客户经理{idx+1}',
                    client_contact=f'1390000{idx+1:04d}',
                    our_manager=our_mgr.name, # 负责人名称
                    status=status,
                    created_by_id=admin.id
                )
                db.session.add(c)
                contracts.append(c)
                
                # 5.1 销售信息
                sales = SalesInfo(
                    contract=c,
                    quote_amount=random.randint(50, 500) * 10000,
                    quote_date=start_date - timedelta(days=30),
                    deal_date=start_date,
                    sales_person_id=persons[0].id, # 销售总监负责
                    remarks="模拟销售记录"
                )
                db.session.add(sales)

            db.session.commit()
        else:
            contracts = Contract.query.all()

        # 6. 为项目生成任务、采购、验收、反馈和文件
        if Task.query.count() == 0:
            print("[-] [6/7] 生成任务、采购、验收与文件明细...")
            for contract in contracts:
                # -------------------------------------------------
                # 6.1 生成任务 (未启动的项目不生成进行中任务)
                # -------------------------------------------------
                if contract.status != '未启动':
                    tasks_def = [
                        ('机械结构设计', '研发部', 10),
                        ('电气原理图设计', '研发部', 7),
                        ('PLC程序开发', '研发部', 14),
                        ('关键零部件采购', '采购部', 20),
                        ('设备组装调试', '生产部', 30)
                    ]
                    
                    base_date = date.today() - timedelta(days=30)
                    for t_name, dept_name, duration in tasks_def:
                        dept = depts.get(dept_name)
                        if dept:
                            # 根据合同状态调整任务状态
                            task_status = '进行中'
                            if contract.status in ['已验收', '验收/问题']:
                                task_status = '已完成'
                            elif contract.status == '延误' and random.random() > 0.5:
                                task_status = '延误' # 假设任务也有延误状态，或者仍为进行中
                            
                            task = Task(
                                contract_id=contract.id,
                                department_id=dept.id,
                                title=t_name,
                                start_date=base_date,
                                end_date=base_date + timedelta(days=duration),
                                status=task_status,
                                remarks="模拟任务数据"
                            )
                            db.session.add(task)
                            base_date += timedelta(days=5)

                # -------------------------------------------------
                # 6.2 生成采购项
                # -------------------------------------------------
                if contract.status not in ['未启动']:
                    items = [
                        ('西门子 PLC S7-1200', '套', 2),
                        ('伺服电机 1.5KW', '台', 4),
                        ('精密导轨 2000mm', '根', 10),
                        ('工业触摸屏 10寸', '台', 2),
                        ('高强度铝型材', '米', 100)
                    ]
                    for item_name, unit, qty in items:
                        if random.random() > 0.3:
                            proc_status = '已到货' if contract.status in ['已验收', '生产中', '验收/问题'] else '已下单'
                            proc = ProcurementItem(
                                contract_id=contract.id,
                                item_name=item_name,
                                quantity=qty,
                                unit=unit,
                                expected_date=date.today() + timedelta(days=15),
                                status=proc_status,
                                remarks="模拟BOM清单"
                            )
                            db.session.add(proc)

                # -------------------------------------------------
                # 6.3 生成验收记录 (针对已验收/验收问题项目)
                # -------------------------------------------------
                if contract.status in ['已验收', '验收/问题', '生产中']:
                    stages = ['出厂验收 (FAT)', '现场验收 (SAT)']
                    for stage in stages:
                        # 只有已验收的项目才有 SAT
                        if stage == '现场验收 (SAT)' and contract.status not in ['已验收', '验收/问题']:
                            continue
                            
                        acc_status = '通过'
                        if contract.status == '验收/问题' and stage == '现场验收 (SAT)':
                            acc_status = '不通过' # 模拟问题
                        
                        acceptance = Acceptance(
                            contract_id=contract.id,
                            stage_name=stage,
                            person_id=persons[-1].id, # 售后工程师负责验收
                            date=date.today() - timedelta(days=random.randint(1, 20)),
                            status=acc_status,
                            remarks="模拟验收记录"
                        )
                        db.session.add(acceptance)

                # -------------------------------------------------
                # 6.4 生成反馈/问题 (针对验收/问题项目)
                # -------------------------------------------------
                if contract.status == '验收/问题':
                    fb = Feedback(
                        contract_id=contract.id,
                        content="现场调试时发现输送带速度不稳定，且噪音较大，客户要求整改。",
                        feedback_time=datetime.utcnow() - timedelta(days=2),
                        handler_id=persons[-1].id, # 售后工程师处理
                        result="正在排查电机驱动参数",
                        is_resolved=False
                    )
                    db.session.add(fb)
                elif contract.status == '已验收':
                    fb = Feedback(
                        contract_id=contract.id,
                        content="操作界面字体太小，希望调整。",
                        feedback_time=datetime.utcnow() - timedelta(days=10),
                        handler_id=persons[2].id, # 研发总监处理
                        result="已更新 HMI 程序 V2.0",
                        completion_time=datetime.utcnow() - timedelta(days=8),
                        is_resolved=True
                    )
                    db.session.add(fb)

                # -------------------------------------------------
                # 6.5 生成项目文件
                # -------------------------------------------------
                file_types = ['contract', 'tech', 'drawing']
                for ft in file_types:
                    pf = ProjectFile(
                        contract_id=contract.id,
                        uploader_id=admin.id,
                        file_type=ft,
                        version='V1.0',
                        author=contract.our_manager,
                        original_filename=f'{contract.project_code}_{ft}_v1.pdf',
                        stored_filename=f'fake_file_{random.randint(1000,9999)}.pdf', # 模拟文件名
                        content_type='application/pdf',
                        file_size=random.randint(1024, 102400),
                        is_public=(ft == 'contract')
                    )
                    db.session.add(pf)
            
            db.session.commit()

        print("[-] [7/7] 模拟数据初始化完成！")

if __name__ == '__main__':
    # 1. 初始化数据
    init_demo_data()
    
    # 2. 启动服务
    try:
        from waitress import serve
        print("\n" + "="*60)
        print("              CORE ERP 安全模拟模式")
        print("="*60)
        print(f" [模式] 独立模拟环境 (不连接 SQL Server)")
        print(f" [数据] {DB_FILE}")
        print(f" [地址] http://127.0.0.1:8080")
        print("-" * 60)
        print(" [登录账号] admin")
        print(" [登录密码] 123456")
        print("="*60 + "\n")
        
        serve(app, host='0.0.0.0', port=8080)
    except ImportError:
        print("错误: 请先安装 waitress (pip install waitress)")
