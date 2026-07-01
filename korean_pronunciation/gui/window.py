"""Main window class for the Korean Pronunciation GUI."""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QStatusBar,
)
from PySide6.QtCore import Slot
from PySide6.QtGui import QGuiApplication

from korean_pronunciation.gui.engine_worker import PronunciationWorker
from korean_pronunciation.gui.style import STYLE_SHEET


class MainWindow(QMainWindow):
    """Main application window for the Korean Pronunciation Converter."""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Korean Pronunciation Converter")
        self.resize(500, 550)
        self.setMinimumSize(400, 450)
        self.setStyleSheet(STYLE_SHEET)

        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # Header / Title
        header_label = QLabel("Korean Pronunciation Converter")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #111827; margin-bottom: 8px;")
        main_layout.addWidget(header_label)

        # Input Section
        input_label = QLabel("Input")
        main_layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter Korean word or sentence here...")
        self.input_field.setClearButtonEnabled(True)
        main_layout.addWidget(self.input_field)

        # Action Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("convertButton")
        self.convert_btn.setToolTip("Convert input text to pronunciations (Enter)")
        btn_layout.addWidget(self.convert_btn)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setToolTip("Copy all pronunciations to clipboard")
        btn_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setToolTip("Clear input and results")
        btn_layout.addWidget(self.clear_btn)

        main_layout.addLayout(btn_layout)

        # Output Section
        output_label = QLabel("Pronunciations")
        main_layout.addWidget(output_label)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setPlaceholderText("Results will be shown here...")
        main_layout.addWidget(self.output_field)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connections
        self.input_field.returnPressed.connect(self.start_conversion)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.clear_btn.clicked.connect(self.clear_all)

        # Initial focus
        self.input_field.setFocus()

    @Slot()
    def start_conversion(self):
        text = self.input_field.text().strip()
        if not text:
            self.status_bar.showMessage("Please enter some text to convert.")
            self.output_field.setPlaceholderText("Please enter some text to convert.")
            self.output_field.clear()
            return

        # Disable controls during background work to prevent concurrent runs
        self.set_controls_enabled(False)
        self.status_bar.showMessage("Converting...")
        self.output_field.clear()

        # Start worker thread
        self.worker = PronunciationWorker(text)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)
        self.worker.start()

    @Slot(list)
    def on_conversion_finished(self, results):
        self.set_controls_enabled(True)
        self.status_bar.showMessage("Ready")

        if not results:
            self.output_field.setHtml(
                "<span style='color: #6b7280; font-style: italic;'>No valid pronunciations found.</span>"
            )
            return

        # Format output cleanly with numbering
        formatted_results = []
        for i, res in enumerate(results, 1):
            formatted_results.append(f"{i}. {res['pronunciation']}")

        self.output_field.setPlainText("\n\n".join(formatted_results))
        self.input_field.setFocus()

    @Slot(str)
    def on_conversion_error(self, err_msg):
        self.set_controls_enabled(True)
        self.status_bar.showMessage(f"Error: {err_msg}")
        self.output_field.setPlainText(f"An error occurred during processing:\n{err_msg}")
        self.input_field.setFocus()

    @Slot()
    def copy_to_clipboard(self):
        text = self.output_field.toPlainText().strip()
        if not text:
            self.status_bar.showMessage("Nothing to copy.")
            return

        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        self.status_bar.showMessage("Pronunciations copied to clipboard.")

    @Slot()
    def clear_all(self):
        self.input_field.clear()
        self.output_field.clear()
        self.status_bar.showMessage("Ready")
        self.output_field.setPlaceholderText("Results will be shown here...")
        self.input_field.setFocus()

    def set_controls_enabled(self, enabled: bool):
        self.input_field.setEnabled(enabled)
        self.convert_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.copy_btn.setEnabled(enabled)
