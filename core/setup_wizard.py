# -*- coding: utf-8 -*-
"""
setup_wizard.py - 首次启动设置向导 / First-Run Setup Wizard

首次启动时引导用户完成系统初始化：
Guides users through initial system setup on first run:

- Step 1: 公司名称 / Company name
- Step 2: 管理员账号 / Admin account
- Step 3: 完成 / Finish

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os
import json
import secrets

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from werkzeug.security import generate_password_hash

setup_bp = Blueprint('setup', __name__)

# 配置文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')


def is_setup_complete():
    """检查是否已完成初始设置"""
    if os.path.exists(CONFIG_JSON_PATH):
        try:
            with open(CONFIG_JSON_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                return cfg.get('setup_complete', False)
        except (json.JSONDecodeError, IOError):
            pass
    return False


def write_config(data):
    """写入配置到 data/config.json"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'uploads'), exist_ok=True)
    with open(CONFIG_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── Step 1: 公司名称 ─────────────────────────────────────

@setup_bp.route('/setup', methods=['GET', 'POST'])
def step1():
    """设置向导 Step 1: 输入公司名称"""
    if is_setup_complete():
        return redirect(url_for('home'))

    if request.method == 'POST':
        company_name = (request.form.get('company_name') or '').strip()
        if not company_name:
            flash('请输入公司名称')
            return render_template('setup/step1.html')

        # 暂存到 session 或直接传到 step2
        return render_template('setup/step2.html', company_name=company_name)

    return render_template('setup/step1.html')


# ─── Step 2: 管理员账号 ───────────────────────────────────

@setup_bp.route('/setup/finish', methods=['POST'])
def finish():
    """设置向导完成: 写入配置 + 创建管理员"""
    if is_setup_complete():
        return redirect(url_for('home'))

    company_name = (request.form.get('company_name') or '').strip()
    admin_username = (request.form.get('admin_username') or '').strip()
    admin_realname = (request.form.get('admin_realname') or '').strip()
    admin_password = (request.form.get('admin_password') or '').strip()

    # 校验
    if not company_name or not admin_username or not admin_password or not admin_realname:
        flash('请填写所有必填项')
        return render_template('setup/step2.html', company_name=company_name)

    import random
    invite_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    # 1. 写入 config.json
    config_data = {
        'secret_key': secrets.token_hex(32),
        'database_uri': f'sqlite:///{os.path.join(DATA_DIR, "erp.db")}',
        'db_mode': 'sqlite',
        'company_name': company_name,
        'copyright_text': f'2026 {company_name} 版权所有',
        'app_base_url': 'http://127.0.0.1:8000',
        'notification_backend': 'dummy',
        'upload_folder': os.path.join(DATA_DIR, 'uploads'),
        'invite_code': invite_code,
        'setup_complete': True,
    }
    write_config(config_data)

    # 2. 创建管理员用户（在当前 app context 中）
    from . import db
    from .models import User

    # 检查用户是否已存在
    existing = User.query.filter_by(username=admin_username).first()
    if not existing:
        admin_user = User(
            username=admin_username,
            real_name=admin_realname,
            email=f'{admin_username}@local',
            phone='',
            wechat='',
            password_hash=generate_password_hash(admin_password),
            role='admin',
            is_active=True,
            status='active',
        )
        db.session.add(admin_user)
        db.session.commit()

    # 3. 更新当前 app config（不需要重启）
    from flask import current_app
    current_app.config['COMPANY_NAME'] = company_name
    current_app.config['COPYRIGHT_TEXT'] = config_data['copyright_text']
    current_app.config['SECRET_KEY'] = config_data['secret_key']

    return render_template('setup/done.html', company_name=company_name)
