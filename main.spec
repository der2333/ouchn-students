# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置。

只收集 Playwright 的驱动程序（node.exe + cli.js），**不包含任何浏览器内核**：
程序启动时使用用户电脑上已安装的 Chrome / Edge。

构建：pyinstaller main.spec --clean --noconfirm
"""

import os

from PyInstaller.utils.hooks import collect_all

# 收集 playwright 包（含 driver），其中不含 Chromium / Chrome / Edge 内核
datas, binaries, hiddenimports = collect_all("playwright")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="OUCHN学习助手",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    # 程序通过 print/input 与用户交互，必须保留控制台窗口
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 版本信息：减少杀毒软件误报
    version=os.path.join(SPECPATH, "version_info.txt"),
)
