import sys
import threading
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTextEdit
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt          # <-- import Qt
from PyQt5.QtGui import QFont

from backend.server import MobilWheelTCPServer


# =========================
# LOGGER -> UI
# =========================
class LogEmitter(QObject):
    log_signal = pyqtSignal(str)


log_emitter = LogEmitter()


class QtLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        log_emitter.log_signal.emit(msg)


# =========================
# UI (XWheel - Dark Blue Theme)
# =========================
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XWheel")
        self.setGeometry(200, 200, 550, 450)

        self.server = None
        self.server_thread = None

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Widgets
        self.status = QLabel("Status: OFFLINE")
        self.status.setAlignment(Qt.AlignCenter)          # <-- corrigido
        self.status.setFont(QFont("Segoe UI", 12, QFont.Bold))

        self.ip_label = QLabel("IP: -")
        self.ip_label.setAlignment(Qt.AlignCenter)        # <-- corrigido
        self.ip_label.setFont(QFont("Segoe UI", 10))

        self.start_btn = QPushButton("START SERVER")
        self.stop_btn = QPushButton("STOP SERVER")

        # Logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setFont(QFont("Consolas", 9))

        # Adiciona ao layout
        layout.addWidget(self.status)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.logs)

        self.setLayout(layout)

        # Conexões dos botões
        self.start_btn.clicked.connect(self.start_server)
        self.stop_btn.clicked.connect(self.stop_server)

        # Conecta o sinal de log
        log_emitter.log_signal.connect(self.append_log)

        # Configura logger global com handler Qt
        handler = QtLogHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

        # Aplica o tema dark blue + azul via QSS
        self.apply_dark_blue_theme()

    def apply_dark_blue_theme(self):
        """Estilo dark blue com detalhes em azul claro"""
        self.setStyleSheet("""
            QWidget {
                background-color: #0A192F;
                color: #E6F1FF;
                font-family: "Segoe UI", "Roboto", sans-serif;
            }

            QLabel {
                background-color: transparent;
                padding: 4px;
            }

            QPushButton {
                background-color: #1E3A5F;
                border: 1px solid #2C5282;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
                color: #90CDF4;
            }

            QPushButton:hover {
                background-color: #2C5282;
                border-color: #63B3ED;
                color: #FFFFFF;
            }

            QPushButton:pressed {
                background-color: #0F2C4F;
            }

            QTextEdit {
                background-color: #0B1120;
                border: 1px solid #2C5282;
                border-radius: 6px;
                padding: 8px;
                color: #CBD5E0;
                selection-background-color: #2C5282;
            }

            QScrollBar:vertical {
                background: #0A192F;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #2C5282;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #4299E1;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    # =========================
    def append_log(self, msg):
        self.logs.append(msg)

    # =========================
    def start_server(self):
        if self.server_thread and self.server_thread.is_alive():
            return

        self.server = MobilWheelTCPServer()

        def run():
            try:
                ip = self.server._get_ip()
                log_emitter.log_signal.emit(f"IP: {ip}:{self.server.port}")
                self.ip_label.setText(f"IP: {ip}:{self.server.port}")
                self.server.start()
            except Exception as e:
                logging.error(f"Erro server: {e}")

        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()

        self.status.setText("Status: ONLINE")
        self.status.setStyleSheet("color: #4ADE80;")

    # =========================
    def stop_server(self):
        if self.server:
            self.server.running = False
            self.status.setText("Status: OFFLINE")
            self.status.setStyleSheet("color: #F87171;")
            logging.info("Servidor parado")


# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())