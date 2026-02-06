# -*- coding: utf-8 -*-
"""
run.py - 开发服务器入口 / Development Server Entry Point

本模块用于启动 Flask 开发服务器：
This module is used to start the Flask development server:

Usage / 使用方法:
    python run.py

Features / 功能特点:
- 自动创建数据库表 / Auto-create database tables
- 开启调试模式 / Enable debug mode
- 监听所有网络接口 (0.0.0.0) / Listen on all network interfaces

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

from core import create_app, db

app = create_app()


if __name__ == '__main__':
    # Create tables in the database if they do not exist
    with app.app_context():
        db.create_all()

    # Key: Explicitly specify the host + a relatively uncommon port + disable auto-reload
    app.run(
        debug=True,
        #host="127.0.0.1",
        host="0.0.0.0",
        port=8000,
        use_reloader=False,
    )