from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from repositories.filter_option_repository import FilterOptionRepository


class FilterOptionWorker(QObject):
    succeeded = pyqtSignal(object)
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, database_path):
        super().__init__()
        self.database_path = database_path

    @pyqtSlot()
    def run(self):
        try:
            self.succeeded.emit(FilterOptionRepository(self.database_path).load_options())
        except Exception as error:
            self.failed.emit(str(error) or "Không thể nạp bộ lọc.")
        finally:
            self.finished.emit()
