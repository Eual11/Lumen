# -*- mode: python ; coding: utf-8 -*-

ONEFILE = True

EXCLUDES = [
    'tkinter',
    'matplotlib',
    'pyqtgraph',      
    'pandas',
    'scipy',
    'PIL',
    'IPython',
    'pytest',
    'setuptools',
    'pip',
]

PRUNE_BINARIES = (
    'Qt6Quick',
    'Qt6Qml',
    'Qt6QmlModels',
    'Qt6Pdf',
    'Qt6VirtualKeyboard',
    'QtQuick',
    'QtQml',
    'QtPdf',
    'platforminputcontexts',
)


a = Analysis(
    ['lumen.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDES,
    noarchive=False,
    optimize=1,
)

a.binaries = [b for b in a.binaries if not any(k in b[0] for k in PRUNE_BINARIES)]
a.datas = [d for d in a.datas if not any(k in d[0] for k in PRUNE_BINARIES)]

pyz = PYZ(a.pure)

if ONEFILE:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='Lumen',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='Lumen',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico',
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name='Lumen',
    )
