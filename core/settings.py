# -*- coding: utf-8 -*-
"""
settings.py - 系统设置模块 / System Settings Module

管理员通过网页调整系统配置：
Admin adjusts system configuration through web interface:

- 基本设置: 公司名称、版权文字 / Basic: company name, copyright
- 远程访问: Tailscale 中文引导 / Remote: Tailscale guide
- 系统信息: 版本、数据库大小 / System: version, DB size

仅 admin / boss 角色可访问。

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os
import sys
import json
import platform
import subprocess
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort, current_app
)

from . import db
from .models import User

settings_bp = Blueprint('settings', __name__)

# 版本号
CORE_ERP_VERSION = '3.0.0'

# 配置文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')


def admin_required(view):
    """仅允许 admin / boss 角色访问"""
    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('请先登录')
            return redirect(url_for('auth.login'))
        user = User.query.get(user_id)
        if not user or user.role not in ('admin', 'boss'):
            abort(403)
        return view(**kwargs)
    return wrapped_view


def _load_config():
    """读取 config.json"""
    if os.path.exists(CONFIG_JSON_PATH):
        try:
            with open(CONFIG_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save_config(data):
    """写入 config.json"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_db_size():
    """获取数据库文件大小（SQLite 模式）"""
    db_path = os.path.join(DATA_DIR, 'erp.db')
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        if size < 1024:
            return f'{size} B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.1f} KB'
        else:
            return f'{size / (1024 * 1024):.1f} MB'
    return '未找到'


def _get_current_user():
    user_id = session.get('user_id')
    return User.query.get(user_id) if user_id else None


# ─── 设置主页 ─────────────────────────────────────────────

@settings_bp.route('/settings')
@admin_required
def index():
    """系统设置主页"""
    user = _get_current_user()
    cfg = _load_config()
    tab = request.args.get('tab', 'basic')

    # 服务状态
    service_status = _get_service_status()

    # 系统信息
    sys_info = {
        'version': CORE_ERP_VERSION,
        'python_version': platform.python_version(),
        'os': f'{platform.system()} {platform.release()}',
        'db_mode': cfg.get('db_mode', 'sqlite'),
        'db_size': _get_db_size(),
        'user_count': User.query.count(),
        'service_status': service_status,
    }

    return render_template(
        'admin/settings.html',
        user=user,
        cfg=cfg,
        tab=tab,
        sys_info=sys_info,
    )


# ─── 修改基本设置 ─────────────────────────────────────────

@settings_bp.route('/settings/company', methods=['POST'])
@admin_required
def update_company():
    """修改公司名称和版权文字"""
    cfg = _load_config()

    company_name = (request.form.get('company_name') or '').strip()
    copyright_text = (request.form.get('copyright_text') or '').strip()

    if not company_name:
        flash('公司名称不能为空')
        return redirect(url_for('settings.index', tab='basic'))

    cfg['company_name'] = company_name
    cfg['copyright_text'] = copyright_text or f'2026 {company_name} 版权所有'
    _save_config(cfg)

    # 即时更新当前 app config
    current_app.config['COMPANY_NAME'] = cfg['company_name']
    current_app.config['COPYRIGHT_TEXT'] = cfg['copyright_text']

    flash('公司信息已更新')
    return redirect(url_for('settings.index', tab='basic'))


# ─── 重新生成邀请码 ───────────────────────────────────────

@settings_bp.route('/settings/invite-code/regenerate', methods=['POST'])
@admin_required
def regenerate_invite_code():
    """重新生成员工注册邀请码"""
    import random
    cfg = _load_config()
    cfg['invite_code'] = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    _save_config(cfg)

    flash(f'邀请码已更新为: {cfg["invite_code"]}')
    return redirect(url_for('settings.index', tab='basic'))


# ─── 服务管理 ─────────────────────────────────────────────

def _get_service_status():
    """获取 CORE ERP Windows 服务状态"""
    try:
        result = subprocess.run(
            ['sc', 'query', 'CoreERP'],
            capture_output=True, text=True, timeout=5
        )
        if 'RUNNING' in result.stdout:
            return 'running'
        elif 'STOPPED' in result.stdout:
            return 'stopped'
        elif result.returncode != 0:
            return 'not_installed'
    except Exception:
        pass
    return 'unknown'


@settings_bp.route('/settings/service/restart', methods=['POST'])
@admin_required
def restart_service():
    """重启 CORE ERP 服务"""
    nssm_path = os.path.join(BASE_DIR, 'nssm.exe')
    if not os.path.exists(nssm_path):
        flash('未找到 nssm.exe，无法管理服务')
        return redirect(url_for('settings.index', tab='system'))

    try:
        subprocess.Popen(
            [nssm_path, 'restart', 'CoreERP'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        flash('服务正在重启，请等待几秒后刷新页面...')
    except Exception as e:
        flash(f'重启失败: {e}')

    return redirect(url_for('settings.index', tab='system'))


# ─── 引导关闭 ─────────────────────────────────────────────

@settings_bp.route('/settings/guide/dismiss', methods=['POST'])
@admin_required
def dismiss_guide():
    """关闭首次登录引导"""
    cfg = _load_config()
    cfg['guide_dismissed'] = True
    _save_config(cfg)
    flash('引导已关闭')
    return redirect(url_for('home'))
