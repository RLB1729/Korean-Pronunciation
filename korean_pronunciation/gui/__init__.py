"""GUI package for Korean Pronunciation Converter."""

from korean_pronunciation.gui.window import MainWindow


def run_gui():
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
