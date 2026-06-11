"""好友屏蔽面板 — 编辑好友黑名单。"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.config import AppConfig


class FriendBlockPanel(QWidget):
    """好友黑名单编辑页。"""

    config_changed = pyqtSignal(object)

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._build_ui()
        self._load_config()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 8, 10, 8)
        root.setSpacing(10)

        title = QLabel("好友黑名单（前缀匹配）", self)
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #1e293b;")
        root.addWidget(title)

        hint = QLabel("命中黑名单的好友将被跳过，不执行帮忙和偷菜。", self)
        hint.setStyleSheet("color: #64748b;")
        root.addWidget(hint)

        self._list = QListWidget(self)
        self._list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        root.addWidget(self._list, 1)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        self._input = QLineEdit(self)
        self._input.setPlaceholderText("输入好友昵称前缀，例如: 广告号")
        self._btn_add = QPushButton("新增", self)
        self._btn_remove = QPushButton("删除选中", self)
        row.addWidget(self._input, 1)
        row.addWidget(self._btn_add)
        row.addWidget(self._btn_remove)
        root.addLayout(row)

        self._btn_add.clicked.connect(self._on_add)
        self._btn_remove.clicked.connect(self._on_remove)
        self._input.returnPressed.connect(self._on_add)

    def _load_config(self):
        self._list.clear()
        values = list(self.config.features.friend.blacklist or [])
        seen = set()
        for text in values:
            value = str(text or "").strip()
            if not value or value in seen:
                continue
            seen.add(value)
            self._list.addItem(QListWidgetItem(value))

    def _on_add(self):
        text = str(self._input.text() or "").strip()
        if not text:
            return
        for i in range(self._list.count()):
            if self._list.item(i).text() == text:
                self._input.clear()
                return
        self._list.addItem(QListWidgetItem(text))
        self._input.clear()
        self._save()

    def _on_remove(self):
        row = self._list.currentRow()
        if row < 0:
            return
        self._list.takeItem(row)
        self._save()

    def _save(self):
        values: list[str] = []
        for i in range(self._list.count()):
            text = str(self._list.item(i).text() or "").strip()
            if text:
                values.append(text)
        self.config.features.friend.blacklist = values
        self.config_changed.emit(self.config)

    def set_config(self, config: AppConfig):
        self.config = config
        self._load_config()

