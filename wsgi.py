# -*- coding: utf-8 -*-
"""
wsgi.py - 生产服务器入口 / Production Server Entry Point

本模块用于在生产环境中使用 Waitress WSGI 服务器启动应用：
This module is used to start the application with Waitress WSGI server in production:

Usage / 使用方法:
    python wsgi.py

Features / 功能特点:
- 使用 Waitress 作为生产级 WSGI 服务器 / Use Waitress as production WSGI server
- 仅监听本地回环地址 (127.0.0.1) / Listen on localhost only
- 配合 Tailscale 实现零成本远程访问 / Combine with Tailscale for zero-cost remote access

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os
import sys

# 将当前目录加入 Python 路径 / Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import create_app

app = create_app()


if __name__ == "__main__":
    from waitress import serve
    print("正在启动生产服务器 (Waitress)...")
    # 仅监听本地，配合 Tailscale 使用
    serve(app, host='127.0.0.1', port=8000)