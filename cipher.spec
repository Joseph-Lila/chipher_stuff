# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None

added_files = [
    ( 'D:/PycharmProjects/chipher_stuff/assets', 'assets' )
]


block_cipher = None


a = Analysis(
    ['D:\\PycharmProjects\\chipher_stuff\\main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['pycryptodomex', 'kivy==2.1.0', 'kivymd==0.104.2', 'kivymd_extensions.akivymd'],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    [],
    name='cipher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\PycharmProjects\\chipher_stuff\\assets\\images\\w1500_50462300.ico'],
)
