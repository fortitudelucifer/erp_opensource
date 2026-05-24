# -*- coding: utf-8 -*-
"""
build.py - CORE ERP 打包构建脚本 / Build Script

将项目打包为可独立运行的 Windows 便携版：
Builds the project into a standalone Windows portable package:

Usage / 使用方法:
    python installer/build.py

输出:
    installer/build/  ← 可独立运行的完整程序

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

import os
import sys
import shutil
import urllib.request
import zipfile
import subprocess

# ─── 配置 ─────────────────────────────────────────────────

PYTHON_VERSION = '3.12.8'
PYTHON_EMBED_URL = f'https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip'
GET_PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'
NSSM_URL = 'https://nssm.cc/release/nssm-2.24.zip'

# 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BUILD_DIR = os.path.join(SCRIPT_DIR, 'build')
PYTHON_DIR = os.path.join(BUILD_DIR, 'python')
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, 'downloads')

# 需要复制的源码文件/目录
SOURCE_ITEMS = [
    'core',
    'config.py',
    'launcher.py',
    'wsgi.py',
    'requirements.txt',
]

# 排除的文件模式
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '.git',
    '.vs',
    'simulation_safe.db',
]


def log(msg):
    print(f'[BUILD] {msg}')


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# ─── Step 1: 下载 Python Embedded ─────────────────────────

def download_python_embed():
    """下载 Python Embedded zip"""
    ensure_dir(DOWNLOAD_DIR)
    zip_name = f'python-{PYTHON_VERSION}-embed-amd64.zip'
    zip_path = os.path.join(DOWNLOAD_DIR, zip_name)

    if os.path.exists(zip_path):
        log(f'Python Embedded 已存在: {zip_name}')
        return zip_path

    log(f'下载 Python {PYTHON_VERSION} Embedded...')
    log(f'URL: {PYTHON_EMBED_URL}')
    urllib.request.urlretrieve(PYTHON_EMBED_URL, zip_path)
    log(f'下载完成: {zip_name}')
    return zip_path


# ─── Step 2: 解压并配置 Python ────────────────────────────

def setup_python(zip_path):
    """解压 Python Embedded 并启用 import"""
    if os.path.exists(PYTHON_DIR):
        log('清理旧的 Python 目录...')
        shutil.rmtree(PYTHON_DIR)

    log('解压 Python Embedded...')
    ensure_dir(PYTHON_DIR)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(PYTHON_DIR)

    # 修改 ._pth 文件以启用 import site
    pth_files = [f for f in os.listdir(PYTHON_DIR) if f.endswith('._pth')]
    if pth_files:
        pth_path = os.path.join(PYTHON_DIR, pth_files[0])
        log(f'修改 {pth_files[0]} 以启用 import...')
        with open(pth_path, 'r') as f:
            content = f.read()
        # 去掉 import site 前的注释
        content = content.replace('#import site', 'import site')
        # 添加上层目录到路径（让 Python 能找到项目代码）
        content += '\n..\n'
        with open(pth_path, 'w') as f:
            f.write(content)
        log('import site 已启用')


# ─── Step 3: 安装 pip ─────────────────────────────────────

def install_pip():
    """下载并安装 pip"""
    python_exe = os.path.join(PYTHON_DIR, 'python.exe')
    get_pip_path = os.path.join(DOWNLOAD_DIR, 'get-pip.py')

    if not os.path.exists(get_pip_path):
        log('下载 get-pip.py...')
        urllib.request.urlretrieve(GET_PIP_URL, get_pip_path)

    log('安装 pip...')
    subprocess.run(
        [python_exe, get_pip_path, '--no-warn-script-location'],
        check=True
    )
    log('pip 安装完成')


# ─── Step 4: 安装依赖 ─────────────────────────────────────

def install_dependencies():
    """安装项目依赖"""
    python_exe = os.path.join(PYTHON_DIR, 'python.exe')
    req_file = os.path.join(SCRIPT_DIR, 'requirements_build.txt')

    log('安装项目依赖...')
    subprocess.run(
        [python_exe, '-m', 'pip', 'install',
         '-r', req_file,
         '--no-warn-script-location',
         '--disable-pip-version-check'],
        check=True
    )
    log('依赖安装完成')


# ─── Step 5: 复制源码 ─────────────────────────────────────

def should_exclude(name):
    """检查文件/目录是否应该排除"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern:
            return True
    return False


def copy_source():
    """复制项目源码到构建目录"""
    log('复制源码...')

    for item in SOURCE_ITEMS:
        src = os.path.join(PROJECT_ROOT, item)
        dst = os.path.join(BUILD_DIR, item)

        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(
                src, dst,
                ignore=shutil.ignore_patterns(*EXCLUDE_PATTERNS)
            )
            log(f'  目录: {item}/')
        elif os.path.isfile(src):
            shutil.copy2(src, dst)
            log(f'  文件: {item}')

    # 创建空的 data 目录
    data_dir = os.path.join(BUILD_DIR, 'data')
    ensure_dir(data_dir)
    ensure_dir(os.path.join(data_dir, 'uploads'))
    log('  目录: data/ (空)')


# ─── Step 6: 下载 NSSM ────────────────────────────────────

def download_nssm():
    """下载 NSSM 并提取 nssm.exe"""
    nssm_dst = os.path.join(BUILD_DIR, 'nssm.exe')
    if os.path.exists(nssm_dst):
        log('nssm.exe 已存在')
        return

    zip_path = os.path.join(DOWNLOAD_DIR, 'nssm-2.24.zip')
    if not os.path.exists(zip_path):
        log('下载 NSSM...')
        urllib.request.urlretrieve(NSSM_URL, zip_path)

    log('提取 nssm.exe...')
    with zipfile.ZipFile(zip_path, 'r') as z:
        # 提取 win64 版本的 nssm.exe
        for member in z.namelist():
            if member.endswith('win64/nssm.exe'):
                data = z.read(member)
                with open(nssm_dst, 'wb') as f:
                    f.write(data)
                log('nssm.exe 已提取')
                return
    log('警告: 未在 zip 中找到 nssm.exe')


# ─── Step 7: 创建启动脚本 ─────────────────────────────────

def create_scripts():
    """创建启动脚本"""
    # start.bat - 手动启动模式（带窗口，用于调试）
    bat_path = os.path.join(BUILD_DIR, 'start.bat')
    bat_content = '''@echo off
chcp 65001 >nul 2>&1
title CORE ERP 服务
echo ========================================
echo   CORE ERP 正在启动...
echo   请勿关闭此窗口
echo   关闭此窗口 = 关闭服务
echo ========================================
echo.
cd /d "%~dp0"
python\\python.exe launcher.py --port 8000
pause
'''
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    log('创建 start.bat（手动模式）')

    # open.bat - 仅打开浏览器（服务模式下的桌面快捷方式）
    open_path = os.path.join(BUILD_DIR, 'open.bat')
    open_content = '''@echo off
start "" http://127.0.0.1:8000
'''
    with open(open_path, 'w', encoding='utf-8') as f:
        f.write(open_content)
    log('创建 open.bat（打开浏览器）')


# ─── 主流程 ───────────────────────────────────────────────

def main():
    print('=' * 50)
    print('  CORE ERP 构建工具 v2.0')
    print('=' * 50)
    print()

    # 清理旧构建
    if os.path.exists(BUILD_DIR):
        log('清理旧构建目录...')
        shutil.rmtree(BUILD_DIR)
    ensure_dir(BUILD_DIR)

    # 执行构建步骤
    zip_path = download_python_embed()
    setup_python(zip_path)
    install_pip()
    install_dependencies()
    copy_source()
    download_nssm()
    create_scripts()

    # 统计大小
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(BUILD_DIR):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
    size_mb = total_size / (1024 * 1024)

    print()
    print('=' * 50)
    log(f'构建完成！')
    log(f'输出目录: {BUILD_DIR}')
    log(f'总大小: {size_mb:.1f} MB')
    print()
    log('测试方法:')
    log(f'  cd {BUILD_DIR}')
    log(f'  start.bat')
    print('=' * 50)


if __name__ == '__main__':
    main()
