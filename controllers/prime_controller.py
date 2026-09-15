from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSlot
from config.paths import DATABASE_PATH, LOG_ENCODING
from ui.dialogs.import_dialogs import ImportDialogs
from workers.database_init_worker import DatabaseInitWorker
from workers.prime_import_worker import PrimeImportWorker
from workers.cum_import_worker import CumImportWorker
from workers.filter_option_worker import FilterOptionWorker
from workers.summary_worker import SummaryWorker
from workers.slot_summary_worker import SlotSummaryWorker


class PrimeController(QObject):
    """Điều phối UI và worker; không đọc log hoặc truy vấn SQL."""
    def __init__(self, window, database_path=DATABASE_PATH, encoding=LOG_ENCODING):
        """Khởi tạo trạng thái và các thành phần cần cho đối tượng."""
        super().__init__(window)
        self.window = window
        self.database_path = database_path
        self.encoding = encoding
        self.dialogs = ImportDialogs(window)
        self._thread = None
        self._worker = None
        self._kind = None
        self._outcome = None
        self._ready = False
        self._closing = False
        self._summary_key = None
        self._slot_key = None
        self._pending_slot_key = None
        self._pending_summary_key = None
        window.prime_page.import_requested.connect(self.choose_import)
        window.prime_page.cum_import_requested.connect(self.choose_cum_import)
        window.prime_page.filter_applied.connect(self.load_summary)
        window.close_requested.connect(self.request_close)
        window.prime_page.file_management_requested.connect(self.open_file_management)
        window.prime_page.send_mail_requested.connect(self.open_send_mail)

    @property
    def busy(self):
        """Cho biết đang có worker khởi tạo hoặc import chạy."""
        return self._thread is not None

    def _start(self, worker, kind):
        """Gắn worker vào QThread và khóa hai nút import đến khi tác vụ kết thúc."""
        self._worker = worker
        self._kind = kind
        self._outcome = None
        self._thread = QThread(self)
        worker.moveToThread(self._thread)
        self._thread.started.connect(worker.run)
        worker.failed.connect(self._failed)
        worker.finished.connect(self._thread.quit)
        worker.finished.connect(worker.deleteLater)
        self._thread.finished.connect(self._finished)
        self._thread.finished.connect(self._thread.deleteLater)
        self.window.prime_page.set_import_enabled(False)
        self.window.prime_page.tabs.tabBar().setEnabled(False)
        self._thread.start()

    @pyqtSlot()
    def initialize_database(self):
        """Tạo schema cho database mới hoặc kiểm tra database đã tồn tại."""
        if self.busy or self._closing:
            return
        self._ready = False
        worker = DatabaseInitWorker(self.database_path)
        worker.succeeded.connect(self._initialized)
        self._start(worker, "init")

    @pyqtSlot()
    def _initialized(self):
        """Đánh dấu database đã sẵn sàng cho việc import."""
        self._ready = True
        self._outcome = ("success", None)

    @pyqtSlot(str)
    def _failed(self, message):
        """Lưu thông báo lỗi để hiển thị sau khi worker kết thúc."""
        self._outcome = ("error", message)

    @pyqtSlot(object)
    def _succeeded(self, result):
        """Lưu kết quả import để hiển thị sau khi worker kết thúc."""
        self._outcome = ("success", result)

    @pyqtSlot(str)
    def _progress(self, message):
        """Cập nhật tiến độ khi cửa sổ chưa được yêu cầu đóng."""
        if not self._closing:
            self.dialogs.update_progress(message)

    @pyqtSlot()
    def _finished(self):
        """Dọn worker, khôi phục nút và hiển thị kết quả hoặc đóng cửa sổ an toàn."""
        kind, outcome = self._kind, self._outcome
        self._worker = None
        self._thread = None
        self._kind = None
        if kind not in ("summary", "slot") or self._closing:
            self.dialogs.end_progress()
        if self._closing:
            self._finish_close_when_idle()
            return
        # Chính nút Import PRIME cũng cho phép thử lại khi khởi tạo DB lỗi.
        self.window.prime_page.set_import_enabled(True)
        self.window.prime_page.tabs.tabBar().setEnabled(True)
        if outcome is None or outcome[0] == "error":
            message = outcome[1] if outcome else "Tác vụ kết thúc mà không có kết quả."
            if kind == "init":
                message += "\nBấm Import PRIME để thử kết nối database lại."
            if kind == "summary":
                self._summary_key = None
                self.window.prime_page.summary_page.clear_result("Không thể tải dữ liệu.")
            if kind == "slot":
                self._slot_key = None
                self.window.prime_page.yield_slot_page.clear_result("Không thể tải dữ liệu.")
            self.dialogs.end_progress()
            self.dialogs.show_error(message)
        elif kind == "summary":
            try:
                self.window.prime_page.summary_page.load_result(outcome[1], self._pending_summary_key)
                self._summary_key = self._pending_summary_key
            except Exception as error:
                self._summary_key = None
                self.window.prime_page.summary_page.clear_result("Không thể hiển thị biểu đồ.")
                self.dialogs.end_progress()
                self.dialogs.show_error(str(error))
        elif kind == "slot":
            try:
                self.window.prime_page.yield_slot_page.load_result(outcome[1], self._pending_slot_key)
                self._slot_key = self._pending_slot_key
            except Exception as error:
                self._slot_key = None
                self.window.prime_page.yield_slot_page.clear_result("Không thể hiển thị biểu đồ.")
                self.dialogs.end_progress()
                self.dialogs.show_error(str(error))
        elif kind == "filters":
            self.window.prime_page.load_filter_options(outcome[1])
        elif kind == "cum":
            self._mark_file_data_changed("CUM")
            self.dialogs.show_cum_result(outcome[1])
        elif kind == "import":
            self._mark_file_data_changed("PRIME")
            self.dialogs.show_result(outcome[1])
        if kind in ("summary", "slot"):
            self.dialogs.end_progress()
            self.window.prime_page.set_filters_ready(True)
        if kind in ("init", "import", "cum") and self._ready and not self._closing:
            self.refresh_filter_options()

    @pyqtSlot()
    def choose_import(self):
        """Chọn khoảng ngày và thư mục nguồn cho Import PRIME."""
        if self.busy or self._closing:
            return
        if not self._ready:
            self.initialize_database()
            return
        selection = self.dialogs.choose_source()
        if selection is not None:
            self.start_import(*selection)

    def start_import(self, root, dates):
        """Khởi động worker PRIME khi database sẵn sàng và không có tác vụ khác."""
        if self.busy or self._closing or not self._ready:
            return
        worker = PrimeImportWorker(self.database_path, root, dates, self.encoding)
        worker.progress.connect(self._progress)
        worker.succeeded.connect(self._succeeded)
        self.dialogs.begin_progress(self.cancel_import)
        self._start(worker, "import")

    @pyqtSlot()
    def cancel_import(self):
        """Gửi cờ hủy an toàn tới worker import đang chạy."""
        if self._worker is not None and self._kind in ("import", "cum"):
            self._worker.request_cancel()

    @pyqtSlot()
    def request_close(self):
        """Hủy tác vụ đang chạy và đợi kết thúc trước khi đóng cửa sổ."""
        self._closing = True
        mail_page = self.window.prime_page.send_mail_page
        if mail_page is not None:
            mail_page.prepare_close()
        page = self.window.prime_page.file_management_page
        if page is not None:
            page.prepare_close()
        if self.busy:
            self.cancel_import()
            self.window.setEnabled(False)
        else:
            self._finish_close_when_idle()

    @pyqtSlot()
    def choose_cum_import(self):
        """Chọn một file CUM rồi khởi động worker khi database đã sẵn sàng."""
        if self.busy or self._closing:
            return
        if not self._ready:
            self.initialize_database()
            return
        source = self.dialogs.choose_cum_source()
        if source:
            self.start_cum_import(source)

    def start_cum_import(self, excel_path):
        """Chạy CUM dưới cùng bộ điều phối để không chồng tác vụ PRIME và CUM."""
        if self.busy or self._closing or not self._ready:
            return
        worker = CumImportWorker(self.database_path, excel_path)
        worker.progress.connect(self._progress)
        worker.succeeded.connect(self._succeeded)
        self.dialogs.begin_progress(self.cancel_import, "CUM")
        self._start(worker, "cum")

    @pyqtSlot()
    def refresh_filter_options(self):
        """Nạp sau khởi tạo/import; không quét database khi tick từng lựa chọn."""
        if self.busy or self._closing or not self._ready:
            return
        self._summary_key = None
        self._slot_key = None
        self.window.prime_page.yield_slot_page.clear_result()
        self.window.prime_page.summary_page.clear_result()
        self.window.prime_page.set_filters_ready(False)
        worker = FilterOptionWorker(self.database_path)
        worker.succeeded.connect(self._succeeded)
        self._start(worker, "filters")

    @pyqtSlot(object)
    def load_summary(self, criteria):
        """Chỉ query khi Date/Tier/Model/EQP đổi; chia sẻ vòng đời worker import."""
        if self.busy or self._closing or not self._ready:
            return
        if self.window.prime_page.tabs.currentWidget() is self.window.prime_page.file_management_host:
            self.open_file_management()
            return
        if self.window.prime_page.tabs.currentWidget() is self.window.prime_page.send_mail_host:
            self.open_send_mail()
            return
        key = (criteria.date_from, criteria.date_to,
               tuple(sorted({str(t) for t in criteria.tiers if t is not None})),
               tuple(sorted(set(criteria.models))), criteria.eqp or None)
        if self.window.prime_page.tabs.currentWidget() is self.window.prime_page.yield_slot_page:
            self.load_slot_summary((*key, criteria.slot), criteria.scrap_codes)
            return
        page = self.window.prime_page.summary_page
        page.set_scrap_codes(criteria.scrap_codes)
        if key == self._summary_key:
            try:
                page.set_scrap_codes(criteria.scrap_codes, redraw=True)
            except Exception as error:
                self.dialogs.show_error(str(error))
            return
        self._pending_summary_key = key
        self.window.prime_page.summary_page.set_loading(key[0], key[1])
        self.dialogs.begin_loading("Loading ...")
        worker = SummaryWorker(self.database_path, key)
        worker.succeeded.connect(self._succeeded)
        self._start(worker, "summary")

    def load_slot_summary(self, key, scrap_codes=()):
        """SEARCH chỉ tải tab Yield Slot đang mở; cache riêng với Summary."""
        page = self.window.prime_page.yield_slot_page
        page.set_scrap_codes(scrap_codes)
        if key == self._slot_key:
            try:
                page.set_scrap_codes(scrap_codes, redraw=True)
            except Exception as error:
                self.dialogs.show_error(str(error))
            return
        self._pending_slot_key = key
        page.set_loading(key[0], key[1])
        self.dialogs.begin_loading("Loading ...")
        cached_model = (page.model_summary.result
                        if self._slot_key and self._slot_key[:3] == key[:3] else None)
        worker = SlotSummaryWorker(self.database_path, key, cached_model=cached_model)
        worker.succeeded.connect(self._succeeded)
        self._start(worker, "slot")


    @pyqtSlot()
    def open_file_management(self):
        """Tải File Management độc lập bộ lọc thống kê, chỉ sau khởi tạo DB."""
        if self._ready and not self.busy and not self._closing:
            self.window.prime_page.open_file_management(self.database_path)

    def _mark_file_data_changed(self, data_type):
        """Làm mới đúng danh sách sau import PRIME/CUM thành công."""
        page = self.window.prime_page.file_management_page
        if page is not None:
            page.mark_data_changed(data_type)

    def _finish_close_when_idle(self):
        """Đợi cả worker File Management để đóng an toàn chỉ với một lần click."""
        page = self.window.prime_page.file_management_page
        mail_page = self.window.prime_page.send_mail_page
        if self.busy or (page is not None and page.is_busy()) or (mail_page is not None and mail_page.is_busy()):
            self.window.setEnabled(False)
            QTimer.singleShot(50, self._finish_close_when_idle)
            return
        self.window.finish_close()

    @pyqtSlot()
    def open_send_mail(self):
        """Mở cấu hình mail độc lập From/To/EQP/Model/Tier/Scrap Code."""
        if self._ready and not self.busy and not self._closing:
            self.window.prime_page.open_send_mail(self.database_path)
