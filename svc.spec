# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['svc.py'],
    pathex=[],
    binaries=[],
    datas=[("svc.ui", '.'), ("icon.ico", '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
#a.datas += Tree("C:\\Users\\bomes\\AppData\\Local\\Programs\\Python\Python311\\Lib\\site-packages\\moviepy", prefix='moviepy')
a.datas += Tree("/usr/local/lib/python3.10/dist-packages/moviepy", prefix='moviepy')
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='svc',
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
	icon=['icon.ico']
)
