"""主窗口 — 浅色毛玻璃侧边栏导航布局（单实例版）"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget,
    QTabWidget,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image

from loguru import logger

from models.config import AppConfig
from core.bot_engine import BotEngine
from gui.styles import Colors, GLASS_STYLESHEET, glass_button_style
from gui.widgets.sidebar import Sidebar
from gui.widgets.log_panel import LogPanel
from gui.widgets.status_panel import StatusPanel
from gui.widgets.settings_panel import SettingsPanel
from gui.widgets.template_panel import TemplatePanel
from gui.widgets.land_detail_panel import LandDetailPanel
from gui.widgets.task_panel import TaskPanel
from gui.widgets.feature_panel import FeaturePanel
from gui.widgets.global_settings_panel import GlobalSettingsPanel
from gui.widgets.friend_block_panel import FriendBlockPanel
from utils.logger import get_log_signal


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self.engine = BotEngine(config)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setWindowTitle("QQ Farm Vision Bot | F11老板键")
        self.setMinimumSize(1100, 680)
        self.resize(1200, 740)

        self.setStyleSheet(GLASS_STYLESHEET)

        central = QWidget()
        central.setObjectName("mainRoot")
        self.setCentralWidget(central)
        central.setStyleSheet(
            f"""
            QWidget#mainRoot {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {Colors.WINDOW_BG},
                    stop:0.55 {Colors.WINDOW_BG_ALT},
                    stop:1 #F7FCFB
                );
            }}
            """
        )

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # 左侧导航栏
        self._sidebar = Sidebar()
        self._sidebar.navigation_changed.connect(self._on_navigation)
        body.addWidget(self._sidebar)

        # 内容区
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 12, 16, 12)
        content_layout.setSpacing(8)

        self._stack = QStackedWidget()
        self._stack.setStyleSheet("background: transparent; border: none;")

        # 运行控制子页面
        self._status_page = self._build_status_page()
        self._land_panel = LandDetailPanel(self.config)
        self._land_panel.refresh_requested.connect(self._on_land_refresh_requested)
        self._land_panel.config_changed.connect(self._on_config_changed)
        self._task_panel = TaskPanel(self.config)
        self._task_panel.config_changed.connect(self._on_config_changed)
        self._log_panel = LogPanel()

        # 参数设置子页面
        self._feature_panel = FeaturePanel(self.config)
        self._feature_panel.config_changed.connect(self._on_config_changed)
        self._settings_panel = SettingsPanel(self.config)
        self._template_panel = TemplatePanel(self.engine.cv_detector)
        self._template_panel._get_window_keyword = self._get_active_window_keyword
        self._template_panel._get_window_select_rule = self._get_active_window_select_rule
        self._global_panel = GlobalSettingsPanel()
        self._friend_block_panel = FriendBlockPanel(self.config)
        self._friend_block_panel.config_changed.connect(self._on_config_changed)

        # 页面 0: 运行控制
        self._run_tabs = QTabWidget()
        self._run_tabs.setDocumentMode(True)
        self._run_tabs.addTab(self._status_page, "状态总览")
        self._run_tabs.addTab(self._task_panel, "任务调度")
        self._run_tabs.addTab(self._log_panel, "运行日志")
        self._stack.addWidget(self._run_tabs)

        # 页面 1: 参数设置
        self._params_tabs = QTabWidget()
        self._params_tabs.setDocumentMode(True)
        self._params_tabs.addTab(self._settings_panel, "参数设置")
        self._params_tabs.addTab(self._feature_panel, "功能配置")
        self._params_tabs.addTab(self._land_panel, "地块详情")
        self._params_tabs.addTab(self._template_panel, "模板管理")
        self._params_tabs.addTab(self._global_panel, "全局设置")
        self._stack.addWidget(self._params_tabs)

        # 页面 2: 好友屏蔽
        self._stack.addWidget(self._friend_block_panel)

        # 状态面板定时刷新（每秒）
        self._status_refresh_timer = QTimer(self)
        self._status_refresh_timer.setInterval(1000)
        self._status_refresh_timer.timeout.connect(self._refresh_status)

        content_layout.addWidget(self._stack)
        body.addWidget(content, 1)
        root.addLayout(body, 1)

    def _build_status_page(self) -> QWidget:
        """构建状态页：截图预览 + 统计面板 + 控制按钮"""
        page = QWidget()
        page.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # 上半部分：统计面板（左）+ 截图预览（右）
        top = QHBoxLayout()
        top.setSpacing(12)

        left_container = QVBoxLayout()
        left_container.setSpacing(8)

        self._status_panel = StatusPanel()
        left_container.addWidget(self._status_panel, 1)
        left_container.addStretch()

        top.addLayout(left_container, 1)

        preview_card = QFrame()
        preview_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Colors.CARD_BG};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
            """
        )
        preview_card.setFixedWidth(300)
        pv_layout = QVBoxLayout(preview_card)
        pv_layout.setContentsMargins(6, 6, 6, 6)
        self._screenshot_label = QLabel("启动后显示\n实时截图")
        self._screenshot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._screenshot_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(0, 0, 0, 10);
                border: 1px dashed {Colors.BORDER};
                border-radius: 8px;
                color: {Colors.TEXT_DIM};
                font-size: 14px;
            }}
            """
        )
        pv_layout.addWidget(self._screenshot_label)
        top.addWidget(preview_card)

        layout.addLayout(top, 1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._btn_start = self._make_btn("开始", Colors.SUCCESS, Colors.SUCCESS_HOVER)
        self._btn_pause = self._make_btn("暂停", Colors.WARNING, Colors.WARNING_HOVER)
        self._btn_stop = self._make_btn("停止", Colors.DANGER, Colors.DANGER_HOVER)

        self._btn_pause.setEnabled(False)
        self._btn_stop.setEnabled(False)

        self._btn_start.clicked.connect(self._on_start)
        self._btn_pause.clicked.connect(self._on_pause)
        self._btn_stop.clicked.connect(self._on_stop)

        for b in (self._btn_start, self._btn_pause, self._btn_stop):
            btn_row.addWidget(b)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return page

    def _make_btn(self, text: str, color: str, hover: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(38)
        btn.setStyleSheet(glass_button_style(color, hover))
        return btn

    def _connect_signals(self):
        self.engine.log_message.connect(self._log_panel.append_log)
        self.engine.screenshot_updated.connect(self._on_screenshot_updated)
        self.engine.detection_result.connect(self._on_screenshot_updated)
        self.engine.state_changed.connect(self._on_state_changed)
        self.engine.stats_updated.connect(self._status_panel.update_stats)
        self.engine.stats_updated.connect(self._on_stats_for_task_panel)
        self.engine.config_updated.connect(self._on_config_updated)

        get_log_signal().new_log.connect(self._log_panel.append_log)
        self._settings_panel.config_changed.connect(self._on_config_changed)
        self._settings_panel.web_server_toggled.connect(self._on_web_server_toggled)

    # ── 导航切换 ────────────────────────────────────────────

    def _on_navigation(self, key: str):
        page_map = {
            "run": 0,
            "params": 1,
            "friend_block": 2,
        }
        idx = page_map.get(key, 0)
        self._stack.setCurrentIndex(idx)

    # ── 截图更新 ────────────────────────────────────────────

    def _update_screenshot(self, image: Image.Image):
        """更新截图预览"""
        try:
            image = image.convert("RGB")
            data = image.tobytes("raw", "RGB")
            qimg = QImage(
                data,
                image.width,
                image.height,
                3 * image.width,
                QImage.Format.Format_RGB888,
            )
            pixmap = QPixmap.fromImage(qimg)
            scaled = pixmap.scaled(
                self._screenshot_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._screenshot_label.setPixmap(scaled)
        except Exception:
            pass

    def _on_screenshot_updated(self, image: Image.Image):
        self._update_screenshot(image)

    # ── 控制按钮 ────────────────────────────────────────────

    def _on_start(self):
        if self.engine.start():
            self._btn_start.setEnabled(False)
            self._btn_pause.setEnabled(True)
            self._btn_stop.setEnabled(True)
            self._status_refresh_timer.start()

    def _on_pause(self):
        if self._btn_pause.text() == "暂停":
            self.engine.pause()
            self._btn_pause.setText("恢复")
            self._status_refresh_timer.stop()
        else:
            self.engine.resume()
            self._btn_pause.setText("暂停")
            self._status_refresh_timer.start()

    def _on_stop(self):
        self.engine.stop()
        self._btn_start.setEnabled(True)
        self._btn_pause.setEnabled(False)
        self._btn_stop.setEnabled(False)
        self._btn_pause.setText("暂停")
        self._status_refresh_timer.stop()

    def _on_state_changed(self, state: str):
        """Bot 状态变化时更新按钮"""
        state_map = {"running": True, "paused": True, "idle": False, "error": False}
        running = state_map.get(state, False)
        paused = state == "paused"
        self._btn_start.setEnabled(not running)
        self._btn_pause.setEnabled(running)
        self._btn_stop.setEnabled(running)
        self._btn_pause.setText("恢复" if paused else "暂停")
        self._refresh_status()

    def _refresh_status(self):
        """定时刷新状态面板数据"""
        if self._stack.currentIndex() == 0 and self._run_tabs.currentWidget() is self._status_page:
            self._status_panel.update_stats(self.engine.scheduler.get_stats())
        if (
            self._stack.currentIndex() == 0
            and self._run_tabs.currentWidget() is self._task_panel
            and self.engine
            and self.engine._task_snapshots
        ):
            self._task_panel.refresh_snapshots(self.engine._task_snapshots)

    def _on_stats_for_task_panel(self, _stats):
        """stats_updated 信号触发时同步刷新任务调度面板"""
        if (
            self._stack.currentIndex() == 0
            and self._run_tabs.currentWidget() is self._task_panel
            and self.engine
            and self.engine._task_snapshots
        ):
            self._task_panel.refresh_snapshots(self.engine._task_snapshots)

    def _on_config_changed(self, config: AppConfig):
        self.config = config
        self.engine.update_config(config)

    def _on_config_updated(self, config: AppConfig):
        """引擎配置更新时同步 GUI（如地块巡查完成、Web 端修改配置）"""
        if config != self.config:
            return
        self._settings_panel.config = config
        self._settings_panel._loading += 1
        self._settings_panel._load_config()
        self._settings_panel._loading -= 1
        self._land_panel.set_config(config)
        self._task_panel.set_config(config)
        self._feature_panel.set_config(config)
        self._friend_block_panel.set_config(config)

    def _on_land_refresh_requested(self):
        """地块详情页「立即刷新」按钮：触发 OCR 识别个人信息"""
        try:
            if not self.engine.action_executor:
                logger.debug("地块刷新: action_executor 为 None，尝试初始化")
                if not self.engine.start():
                    logger.warning("地块刷新: start() 失败")
                    return

            rect = self.engine._prepare_window()
            if rect:
                self.engine._sync_head_profile_from_ocr(rect)
                self.engine._sync_detail_exp(rect)
            else:
                self.engine._sync_head_profile_from_ocr()
        except Exception:
            pass

    def _on_web_server_toggled(self, start: bool):
        """Web 服务启动/停止"""
        logger.info(f"MainWindow._on_web_server_toggled: start={start}")
        logger.info(f"self.web_server: {getattr(self, 'web_server', None) is not None}")

        if start:
            logger.info("调用 _start_web_server")
            import main as _main

            _main._start_web_server(self.config, self)
        else:
            logger.info("调用 web_server.stop()")
            web = getattr(self, 'web_server', None)
            if web:
                logger.info(f"找到 web_server 实例: {id(web)}")
                web.stop()
                self.web_server = None
                logger.info("web_server.stop() 已调用")
            else:
                logger.warning("self.web_server 为 None，无法停止 Web 服务")

    def closeEvent(self, event):
        self.unregister_hotkeys()
        self.engine.stop()
        super().closeEvent(event)

    # ── 全局热键 ──────────────────────────────────────────

    def register_hotkeys(self):
        """注册 F9/F10/F11 全局热键"""
        try:
            import keyboard

            keyboard.on_press_key("f9", lambda _: self._on_hotkey_pause())
            keyboard.on_press_key("f10", lambda _: self._on_hotkey_stop())
            keyboard.on_press_key("f11", lambda _: self._on_hotkey_boss_key())
            logger.info("全局热键已注册: F9=暂停/恢复, F10=停止, F11=老板键（隐藏窗口）")
        except Exception as e:
            logger.warning(f"全局热键注册失败（可能需要管理员权限）: {e}")

    def unregister_hotkeys(self):
        """注销全局热键"""
        try:
            import keyboard

            keyboard.unhook_all()
        except Exception:
            pass

    def _on_hotkey_pause(self):
        """F9: 暂停/恢复"""
        if self._btn_start.isEnabled():
            return
        if self._btn_pause.text() == "暂停":
            self.engine.pause()
            self._btn_pause.setText("恢复")
            self.engine.log_message.emit("[热键] F9 已暂停")
        else:
            self.engine.resume()
            self._btn_pause.setText("暂停")
            self.engine.log_message.emit("[热键] F9 已恢复")

    def _on_hotkey_stop(self):
        """F10: 停止"""
        if self._btn_start.isEnabled():
            return
        self.engine.stop()
        self._btn_start.setEnabled(True)
        self._btn_pause.setEnabled(False)
        self._btn_stop.setEnabled(False)
        self._btn_pause.setText("暂停")
        self.engine.log_message.emit("[热键] F10 已停止")

    def _on_hotkey_boss_key(self):
        """F11: 老板键（隐藏/显示游戏窗口）"""
        result = self.engine.toggle_game_window()
        if result.get("hidden"):
            self.setWindowTitle("QQ Farm Vision Bot - 游戏已完美隐藏 | F11恢复")
        else:
            self.setWindowTitle("QQ Farm Vision Bot | F11老板键")

    # ── 模板面板回调 ───────────────────────────────────────

    def _get_active_window_keyword(self) -> str:
        return self.config.window_title_keyword or "QQ经典农场"

    def _get_active_window_select_rule(self) -> str:
        return self.config.window_select_rule or "auto"
