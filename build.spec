# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path


datas = [
    ('templates', 'templates'),
    ('gui/icons', 'gui/icons'),
    ('configs', 'configs'),
]

# OCR 资源（可选）：在本机环境自动探测 rapidocr_onnxruntime 安装目录
try:
    import rapidocr_onnxruntime as _rapidocr_onnxruntime

    _rapidocr_dir = Path(_rapidocr_onnxruntime.__file__).resolve().parent
    _rapidocr_cfg = _rapidocr_dir / 'config.yaml'
    _rapidocr_models = _rapidocr_dir / 'models'

    if _rapidocr_cfg.exists():
        datas.append((str(_rapidocr_cfg), 'rapidocr_onnxruntime'))
    if _rapidocr_models.exists():
        datas.append((str(_rapidocr_models), 'rapidocr_onnxruntime/models'))
except Exception:
    pass


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['PyQt6.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['easyocr', 'torch', 'torchvision', 'torchaudio'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='QQFarmBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)
