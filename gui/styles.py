"""主题样式常量 — 清新青蓝风格

目标：
  轻盈底色 + 高对比文字 + 柔和青蓝强调色。
"""


class Colors:
    # 背景
    WINDOW_BG = "#ECF8F4"
    WINDOW_BG_ALT = "#F4FBFF"
    CARD_BG = "#FFFFFF"
    SIDEBAR_BG = "#E8F5F0"
    SIDEBAR_ITEM_HOVER = "rgba(15, 118, 110, 10)"
    SIDEBAR_ITEM_SELECTED = "#0F766E"
    SIDEBAR_ITEM_SELECTED_BG = "rgba(15, 118, 110, 15)"
    SIDEBAR_ITEM_SELECTED_HOVER = "rgba(15, 118, 110, 24)"
    TITLEBAR_BG = "#E8F5F0"
    INPUT_BG = "#FFFFFF"
    INPUT_BG_FOCUS = "#FFFFFF"

    # 强调色
    PRIMARY = "#0EA5A6"
    PRIMARY_HOVER = "#0D9488"
    SUCCESS = "#22C55E"
    SUCCESS_HOVER = "#16A34A"
    WARNING = "#F59E0B"
    WARNING_HOVER = "#D97706"
    DANGER = "#EF4444"
    DANGER_HOVER = "#DC2626"

    # 文字
    TEXT = "#0F172A"
    TEXT_SECONDARY = "#475569"
    TEXT_DIM = "#94A3B8"

    # 边框
    BORDER = "rgba(15, 23, 42, 16)"
    BORDER_STRONG = "rgba(15, 23, 42, 24)"
    BORDER_FOCUS = "rgba(13, 148, 136, 120)"

    # 滚动条
    SCROLLBAR_TRACK = "transparent"
    SCROLLBAR_HANDLE = "rgba(15, 23, 42, 24)"

    # 选中
    SELECTION_BG = "rgba(14, 165, 166, 20)"


# ── 全局样式表 ────────────────────────────────────────────

GLASS_STYLESHEET = f"""
QWidget {{
    color: {Colors.TEXT};
    font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    font-size: 13px;
}}

QGroupBox {{
    background-color: rgba(255, 255, 255, 235);
    border: 1px solid {Colors.BORDER};
    border-radius: 10px;
    margin-top: 22px;
    padding: 20px 16px 14px 16px;
    font-weight: 600;
    font-size: 13px;
    color: {Colors.TEXT};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 4px;
    padding: 0 6px;
    color: {Colors.TEXT_DIM};
    background-color: {Colors.CARD_BG};
    font-weight: 600;
    font-size: 12px;
    letter-spacing: 0.5px;
}}

QCheckBox {{
    spacing: 8px;
    color: {Colors.TEXT};
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid rgba(15, 23, 42, 35);
    border-radius: 4px;
    background: {Colors.INPUT_BG};
}}
QCheckBox::indicator:checked {{
    background: {Colors.PRIMARY};
    border-color: {Colors.PRIMARY};
    image: url(gui/icons/check.svg);
}}

QLineEdit, QSpinBox, QTimeEdit, QComboBox {{
    background-color: {Colors.INPUT_BG};
    border: 1px solid {Colors.BORDER};
    border-radius: 8px;
    padding: 6px 10px;
    color: {Colors.TEXT};
    selection-background-color: {Colors.SELECTION_BG};
    min-height: 24px;
}}
QLineEdit:focus, QSpinBox:focus, QTimeEdit:focus, QComboBox:focus {{
    border-color: {Colors.BORDER_FOCUS};
}}

QSpinBox::up-button {{
    subcontrol-position: top right;
    width: 20px;
    border: none;
    background: transparent;
    border-top-right-radius: 7px;
}}
QSpinBox::down-button {{
    subcontrol-position: bottom right;
    width: 20px;
    border: none;
    background: transparent;
    border-bottom-right-radius: 7px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: rgba(14, 165, 166, 20);
}}
QSpinBox::up-arrow {{
    image: url(gui/icons/arrow_up.svg);
    width: 10px;
    height: 6px;
}}
QSpinBox::down-arrow {{
    image: url(gui/icons/arrow_down.svg);
    width: 10px;
    height: 6px;
}}

QComboBox::down-arrow {{
    image: url(gui/icons/arrow_down.svg);
    width: 10px;
    height: 6px;
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {Colors.CARD_BG};
    color: {Colors.TEXT};
    border: 1px solid {Colors.BORDER_STRONG};
    border-radius: 10px;
    selection-background-color: rgba(14, 165, 166, 12);
    selection-color: {Colors.TEXT};
    outline: none;
    padding: 6px;
    font-size: 13px;
}}
QComboBox QAbstractItemView::item {{
    min-height: 32px;
    padding: 4px 10px;
    border-radius: 6px;
    margin: 2px 4px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: rgba(14, 165, 166, 10);
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: rgba(14, 165, 166, 14);
    color: {Colors.PRIMARY};
    font-weight: 600;
}}

QScrollBar:vertical {{
    background: {Colors.SCROLLBAR_TRACK};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {Colors.SCROLLBAR_HANDLE};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(15, 23, 42, 42);
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QLabel {{
    color: {Colors.TEXT};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QMessageBox {{
    background-color: {Colors.CARD_BG};
    color: {Colors.TEXT};
}}
QMessageBox QLabel {{
    color: {Colors.TEXT};
    background: transparent;
}}
QMessageBox QPushButton {{
    background-color: {Colors.CARD_BG};
    color: {Colors.TEXT};
    border: 1px solid {Colors.BORDER};
    border-radius: 6px;
    padding: 6px 20px;
    min-width: 80px;
}}
QMessageBox QPushButton:hover {{
    background-color: rgba(14, 165, 166, 8);
}}
QMessageBox QDialogButtonBox {{
    background-color: {Colors.CARD_BG};
}}
QMessageBox QScrollArea {{
    background: transparent;
}}

QToolTip {{
    background-color: {Colors.CARD_BG};
    color: {Colors.TEXT};
    border: 1px solid {Colors.BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}
"""


def glass_button_style(color: str, hover: str) -> str:
    return f"""
        QPushButton {{
            background-color: {color};
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 90);
            border-radius: 10px;
            padding: 0 20px;
            font-weight: 600;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton:disabled {{
            background-color: rgba(148, 163, 184, 45);
            border: 1px solid rgba(148, 163, 184, 60);
            color: {Colors.TEXT_DIM};
        }}
    """


def ghost_button_style() -> str:
    return f"""
        QPushButton {{
            background-color: transparent;
            border: 1px solid transparent;
            color: {Colors.TEXT_SECONDARY};
            padding: 4px 12px;
            font-size: 12px;
            border-radius: 6px;
        }}
        QPushButton:hover {{
            background-color: rgba(14, 165, 166, 10);
            border-color: rgba(14, 165, 166, 25);
            color: {Colors.TEXT};
        }}
    """
