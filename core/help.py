# -*- coding: utf-8 -*-
"""
help.py - 帮助中心 / Help Center

提供 FAQ 和使用指南。

Author: fortitudelucifer
License: Apache-2.0
"""

from flask import Blueprint, render_template, session, redirect, url_for

help_bp = Blueprint('help', __name__)


@help_bp.route('/help')
def index():
    """帮助中心主页"""
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    return render_template('help/index.html')
