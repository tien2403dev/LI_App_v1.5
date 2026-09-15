from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QScrollArea, QTabWidget, QVBoxLayout, QWidget
from ui.widgets.filter_panel import FilterPanel
from ui.pages.summary_page import SummaryPage
from ui.pages.yield_slot_page import YieldSlotPage


class PrimePage(QWidget):
    import_requested = pyqtSignal()
    cum_import_requested = pyqtSignal()
    filter_applied = pyqtSignal(object)
    file_management_requested = pyqtSignal()
    send_mail_requested = pyqtSignal()

    def __init__(self):
        """Khởi tạo đối tượng và các thành phần liên quan."""
        super().__init__()
        self.current_criteria = None
        self.filter_panel = FilterPanel()
        self.import_button = self.filter_panel.import_prime_button
        self.cum_import_button = self.filter_panel.import_cum_button
        self.filter_panel.import_prime_clicked.connect(self.import_requested)
        self.filter_panel.import_cum_clicked.connect(self.cum_import_requested)
        self.filter_panel.filter_applied.connect(self._apply_filter)
        self.filter_status = QLabel()
        self.filter_status.setWordWrap(True)
        self.filter_status.setStyleSheet("color:#475569; font-size:12px;")
        content = QWidget()
        content.setObjectName("liAppBackground")
        content.setAttribute(Qt.WA_StyledBackground, True)

        # Chỉ đổi nền ngoài, không áp dụng cho bảng hoặc biểu đồ.
        content.setStyleSheet("""
            QWidget#liAppBackground {
                background-color: #E5EDF7;
            }
        """)

        body = QVBoxLayout(content)
        self.body_layout = body
        # body.setContentsMargins(24, 24, 24, 24)
        body.addWidget(self.filter_panel)
        body.addWidget(self.filter_status)
        self.tabs = QTabWidget()
        self.summary_page = SummaryPage()
        self.tabs.addTab(self.summary_page, "📊 Summary")
        self.yield_slot_page = YieldSlotPage()
        self.tabs.addTab(self.yield_slot_page, "📈 Yield Slot")
        self.file_management_page = None
        self.file_management_host = QWidget()
        self.file_management_layout = QVBoxLayout(self.file_management_host)
        self.file_management_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(self.file_management_host, "🗃 File Management")
        self.send_mail_page = None
        self.send_mail_host = QWidget()
        self.send_mail_layout = QVBoxLayout(self.send_mail_host)
        self.send_mail_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(self.send_mail_host, "📤 Send Mail")
        self.tabs.setStyleSheet("""
            QTabBar::tab { background:#F1F5F9; color:#245585; padding:6px 32px;
                border:1px solid #D4DFEB; border-top-left-radius:5px;
                border-top-right-radius:5px; margin-right:4px; }
            QTabBar::tab:selected { background:white; color:#0078D7;
                border-bottom:2px solid #1684E8; }
            QTabWidget::pane { border:1px solid #D4DFEB; background:white; }
        """)
        body.addWidget(self.tabs, 1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(content)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        self.set_import_enabled(False)
        self.set_filters_ready(False)
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def set_import_enabled(self, enabled):
        """Thực hiện set import enabled cho chức năng tương ứng."""
        self.filter_panel.set_import_buttons_enabled(enabled)
        if not enabled:
            self.filter_panel.apply_filter_button.setEnabled(False)

    def set_filters_ready(self, ready):
        """Thực hiện set filters ready cho chức năng tương ứng."""
        self.filter_panel.apply_filter_button.setEnabled(ready)

    def load_filter_options(self, result):
        """Thực hiện load filter options cho chức năng tương ứng."""
        self.filter_panel.load_options(result)
        self.current_criteria = None
        self.filter_status.clear()
        self.set_filters_ready(True)

    def _apply_filter(self, criteria):
        """Thực hiện apply filter cho chức năng tương ứng."""
        self.current_criteria = criteria
        self.filter_status.setText(
            f"Đã chọn điều kiện: {criteria.date_from} → {criteria.date_to} | "
            f"EQP: {criteria.eqp or 'Tất cả'} | SLOT: {criteria.slot or 'Tất cả'} | "
            f"Tier: {len(criteria.tiers)} | Model: {len(criteria.models)} | "
            f"Scrap Code: {len(criteria.scrap_codes)}")
        self.filter_applied.emit(criteria)

    def _on_tab_changed(self, index):
        """Apply current controls only to the newly visible tab, after initialization."""
        if self.tabs.currentWidget() is self.send_mail_host:
            self.send_mail_requested.emit()
            return
        is_files = self.tabs.currentWidget() is self.file_management_host
        # Giữ bộ lọc và lề chung cho mọi tab, kể cả File Management.
        if is_files:
            self.file_management_requested.emit()
            return
        if index < 0 or not self.filter_panel.apply_filter_button.isEnabled():
            return
        self._apply_filter(self.filter_panel.get_filter_criteria())


    def open_file_management(self, database_path):
        """Tạo tab sau khi database sẵn sàng; đọc lại danh sách khi quay lại tab."""
        if self.file_management_page is None:
            from ui.pages.file_management_page import FileManagementPage
            self.file_management_page = FileManagementPage(database_path, self)
            self.file_management_layout.addWidget(self.file_management_page)
        self.file_management_page.load_if_needed(force=True)

    def open_send_mail(self, database_path):
        """Chỉ tạo giao diện Send Mail sau khi database sẵn sàng."""
        if self.send_mail_page is None:
            from ui.pages.send_mail_page import SendMailTab
            self.send_mail_page = SendMailTab(database_path, self)
            self.send_mail_layout.addWidget(self.send_mail_page)
        self.send_mail_page.load_if_needed()
