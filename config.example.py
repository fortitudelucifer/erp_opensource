# -*- coding: utf-8 -*-
"""
config.example.py - 配置文件示例 / Configuration Example

本文件是配置模板，使用前请复制为 config.py 并修改相关配置：
This file is a configuration template. Copy it to config.py and modify before use:

Usage / 使用方法:
    1. 复制此文件为 config.py / Copy this file to config.py
    2. 修改 SECRET_KEY 为随机字符串 / Change SECRET_KEY to a random string
    3. 配置数据库连接 / Configure database connection
    4. 设置公司名称和远程访问 URL / Set company name and remote access URL

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os

# 获取当前文件的绝对目录路径 / Get absolute directory path of current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # [安全配置] 请务必修改为一个随机的长字符串！
    # 这关系到您用户 session 的加密安全
    SECRET_KEY = os.environ.get('APP_SECRET_KEY', 'CHANGE_THIS_TO_A_RANDOM_SECRET_KEY')

    # [数据库] SQL Server 连接字符串
    # 格式: mssql+pyodbc://用户名:密码@主机地址/数据库名?driver=ODBC+Driver+17+for+SQL+Server
    # 示例: mssql+pyodbc://sa:YourStrongPassword@localhost/erp_db?driver=ODBC+Driver+17+for+SQL+Server
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_DATABASE_URI',
        'mssql+pyodbc://sa:YOUR_PASSWORD_HERE@localhost/erp_db?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # [个性化定制]
    # 公司名称 (将显示在网页标题、登录页等位置)
    COMPANY_NAME = "我的工业制造有限公司"
    # 页脚版权文字
    COPYRIGHT_TEXT = "2026 我的工业制造有限公司 版权所有"

    # [异地访问/远程登录配置]
    # 如果您使用 Tailscale 等内网穿透工具进行异地办公，请将此处的 URL 改为您的 Tailscale 机器域名
    # 示例: 'https://win-xxxx.tailxxxx.ts.net'
    # 默认本地开发使用: 'http://127.0.0.1:8000'
    APP_BASE_URL = os.environ.get('APP_BASE_URL', 'http://127.0.0.1:8000')

    # [消息通知后端]
    #可选值: "dummy" (仅打印日志), "email", "ding", "wecom"
    NOTIFICATION_BACKEND = "dummy"

    # [文件上传]
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'core', 'uploads')
