# -*- coding: utf-8 -*-
"""
user_mgmt.py - 用户管理模块 / User Management Module

本模块提供管理员对用户的增删改查、角色分配、启用禁用等功能：
This module provides admin CRUD operations for users, role assignment, enable/disable:

- list_users: 用户列表 / List users
- new_user: 新建用户 / Create user
- edit_user: 编辑用户 / Edit user
- toggle_user: 启用/禁用 / Enable/disable user
- reset_password: 重置密码 / Reset password
- delete_user: 删除用户 / Delete user
- approve_user: 审核用户 / Approve pending user

仅 admin / boss 角色可访问。

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import random
import string
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, abort
)
from werkzeug.security import generate_password_hash

from . import db
from .models import User, ROLE_CHOICES, ROLE_LABELS
from .auth import login_required

user_mgmt_bp = Blueprint('user_mgmt', __name__)


# ─── 权限装饰器 ───────────────────────────────────────────

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


# ─── 工具函数 ─────────────────────────────────────────────

def _generate_temp_password(length=8):
    """生成随机临时密码"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def _get_current_user():
    """获取当前登录用户"""
    user_id = session.get('user_id')
    return User.query.get(user_id) if user_id else None


# ─── 用户列表 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users')
@admin_required
def list_users():
    """用户列表页"""
    user = _get_current_user()
    users = User.query.order_by(User.created_at.desc()).all()
    pending_count = User.query.filter_by(status='pending').count()

    return render_template(
        'admin/users.html',
        user=user,
        users=users,
        role_labels=ROLE_LABELS,
        role_choices=ROLE_CHOICES,
        pending_count=pending_count,
    )


# ─── 新建用户 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    """管理员创建新用户"""
    user = _get_current_user()

    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        real_name = (request.form.get('real_name') or '').strip()
        email = (request.form.get('email') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        wechat = (request.form.get('wechat') or '').strip()
        password = (request.form.get('password') or '').strip()
        role = request.form.get('role', 'customer')

        # 校验必填
        if not username or not real_name or not password:
            flash('用户名、真实姓名和密码为必填项')
            return render_template(
                'admin/user_form.html', user=user,
                role_choices=ROLE_CHOICES, mode='new', form_data=request.form,
            )

        # 检查用户名重复
        if User.query.filter_by(username=username).first():
            flash('该用户名已被占用')
            return render_template(
                'admin/user_form.html', user=user,
                role_choices=ROLE_CHOICES, mode='new', form_data=request.form,
            )

        # 检查邮箱重复（如果填了邮箱）
        if email and User.query.filter_by(email=email).first():
            flash('该邮箱已被占用')
            return render_template(
                'admin/user_form.html', user=user,
                role_choices=ROLE_CHOICES, mode='new', form_data=request.form,
            )

        new_u = User(
            username=username,
            real_name=real_name,
            email=email or f'{username}@local',
            phone=phone or '',
            wechat=wechat or '',
            password_hash=generate_password_hash(password),
            role=role,
            is_active=True,
            status='active',  # 管理员创建的用户直接可用
        )
        db.session.add(new_u)
        db.session.commit()

        flash(f'用户 {real_name}（{username}）创建成功，角色：{ROLE_LABELS.get(role, role)}')
        return redirect(url_for('user_mgmt.list_users'))

    return render_template(
        'admin/user_form.html', user=user,
        role_choices=ROLE_CHOICES, mode='new', form_data={},
    )


# ─── 编辑用户 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """编辑用户信息（可修改角色）"""
    current = _get_current_user()
    target = User.query.get_or_404(user_id)

    if request.method == 'POST':
        target.real_name = (request.form.get('real_name') or target.real_name).strip()
        target.email = (request.form.get('email') or target.email).strip()
        target.phone = (request.form.get('phone') or '').strip()
        target.wechat = (request.form.get('wechat') or '').strip()
        target.role = request.form.get('role', target.role)

        db.session.commit()
        flash(f'用户 {target.real_name} 信息已更新')
        return redirect(url_for('user_mgmt.list_users'))

    return render_template(
        'admin/user_form.html', user=current,
        role_choices=ROLE_CHOICES, mode='edit', target=target,
        form_data={
            'username': target.username,
            'real_name': target.real_name,
            'email': target.email,
            'phone': target.phone,
            'wechat': target.wechat,
            'role': target.role,
        },
    )


# ─── 启用/禁用 ────────────────────────────────────────────

@user_mgmt_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id):
    """启用或禁用用户"""
    current = _get_current_user()
    target = User.query.get_or_404(user_id)

    # 自我保护：不能禁用自己
    if target.id == current.id:
        flash('不能禁用自己的账号')
        return redirect(url_for('user_mgmt.list_users'))

    target.is_active = not target.is_active
    db.session.commit()

    status_text = '启用' if target.is_active else '禁用'
    flash(f'用户 {target.real_name} 已{status_text}')
    return redirect(url_for('user_mgmt.list_users'))


# ─── 重置密码 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users/<int:user_id>/reset_pwd', methods=['POST'])
@admin_required
def reset_password(user_id):
    """重置用户密码为随机临时密码"""
    target = User.query.get_or_404(user_id)
    temp_pwd = _generate_temp_password()
    target.password_hash = generate_password_hash(temp_pwd)
    db.session.commit()

    flash(f'用户 {target.real_name} 的密码已重置为：{temp_pwd}（请告知该用户）')
    return redirect(url_for('user_mgmt.list_users'))


# ─── 删除用户 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """删除用户"""
    current = _get_current_user()
    target = User.query.get_or_404(user_id)

    # 自我保护：不能删除自己
    if target.id == current.id:
        flash('不能删除自己的账号')
        return redirect(url_for('user_mgmt.list_users'))

    name = target.real_name
    db.session.delete(target)
    db.session.commit()

    flash(f'用户 {name} 已删除')
    return redirect(url_for('user_mgmt.list_users'))


# ─── 审核用户 ─────────────────────────────────────────────

@user_mgmt_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@admin_required
def approve_user(user_id):
    """审核通过待审核用户，同时可指定角色"""
    target = User.query.get_or_404(user_id)
    role = request.form.get('role', 'customer')

    target.status = 'active'
    target.role = role
    db.session.commit()

    flash(f'用户 {target.real_name} 已审核通过，角色：{ROLE_LABELS.get(role, role)}')
    return redirect(url_for('user_mgmt.list_users'))
