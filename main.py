"""Chạy giao diện: python main.py."""
import logging
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from controllers.prime_controller import PrimeController
from ui.main_window import MainWindow


def configure_logging():
    """Gửi tiến độ INFO ra stdout, giữ cảnh báo và lỗi ở stderr."""
    progress_handler = logging.StreamHandler(sys.stdout)
    progress_handler.setLevel(logging.INFO)
    progress_handler.addFilter(lambda record: record.levelno < logging.WARNING)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[progress_handler, error_handler],
    )


def main():
    """Mở giao diện tối đa và khởi tạo database trong worker sau khi hiện cửa sổ."""
    app = QApplication(sys.argv)
    # app.setApplicationName("LI App")
    # app.setOrganizationName("LI_App")
    # app.setStyle("Fusion")
    # configure_logging()
    window = MainWindow()
    controller = PrimeController(window)
    window.showMaximized()
    QTimer.singleShot(0, controller.initialize_database)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
