# -*- coding: utf-8 -*-
"""
launcher.py - CORE ERP 统一启动入口 / Unified Launcher

产品化部署的唯一入口：
The single entry point for productized deployment:

- 首次运行 → 自动打开设置向导
- 非首次运行 → 直接启动生产服务

Usage / 使用方法:
    python launcher.py              # 默认端口 8000
    python launcher.py --port 9000  # 自定义端口
    python launcher.py --setup      # 强制进入设置向导

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os
import sys
import json
import webbrowser
import argparse
import threading

# 确保项目根目录在 Python 路径中
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')


def ensure_data_dir():
    """确保 data 目录及子目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'uploads'), exist_ok=True)


def is_first_run():
    """检测是否为首次运行"""
    if not os.path.exists(CONFIG_JSON_PATH):
        return True
    try:
        with open(CONFIG_JSON_PATH, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            return not cfg.get('setup_complete', False)
    except (json.JSONDecodeError, IOError):
        return True


def open_browser_delayed(url, delay=1.5):
    """延迟打开浏览器（等待服务器启动）"""
    def _open():
        import time
        time.sleep(delay)
        webbrowser.open(url)
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def main():
    parser = argparse.ArgumentParser(description='CORE ERP 启动器')
    parser.add_argument('--port', type=int, default=8000, help='服务端口号 (默认: 8000)')
    parser.add_argument('--setup', action='store_true', help='强制进入设置向导')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    args = parser.parse_args()

    ensure_data_dir()

    # 如果强制 setup 模式，删除 config.json
    if args.setup and os.path.exists(CONFIG_JSON_PATH):
        os.remove(CONFIG_JSON_PATH)
        print('[CORE ERP] 已清除配置，将进入设置向导...')

    first_run = is_first_run()

    # 创建 Flask 应用
    from core import create_app
    app = create_app()

    # 确保数据库表已创建
    with app.app_context():
        from core import db
        db.create_all()

    # 获取本机局域网 IP
    import socket
    local_ip = '127.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    url = f'http://127.0.0.1:{args.port}'

    if first_run:
        print('=' * 50)
        print('  CORE ERP - 首次启动')
        print('  请在浏览器中完成初始设置')
        print(f'  {url}/setup')
        print('=' * 50)
    else:
        lan_url = f'http://{local_ip}:{args.port}'
        print('=' * 50)
        print('  CORE ERP - 服务已启动')
        print(f'  本机访问: {url}')
        print(f'  局域网访问: {lan_url}')
        print()
        print(f'  ★ 告诉员工打开浏览器访问: {lan_url}')
        print('  按 Ctrl+C 停止服务')
        print('=' * 50)

    # 自动打开浏览器
    if not args.no_browser:
        target = f'{url}/setup' if first_run else url
        open_browser_delayed(target)

    # 启动服务
    try:
        from waitress import serve
        print(f'\n[Waitress] 生产服务器已启动，监听 0.0.0.0:{args.port}')
        serve(app, host='0.0.0.0', port=args.port)
    except ImportError:
        print('\n[Flask] 开发服务器已启动（建议安装 waitress 用于生产环境）')
        app.run(host='0.0.0.0', port=args.port, debug=False)


if __name__ == '__main__':
    main()
