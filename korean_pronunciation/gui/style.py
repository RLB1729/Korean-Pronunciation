"""Modern, clean stylesheet for the Korean Pronunciation GUI."""

STYLE_SHEET = """
QMainWindow {
    background-color: #f3f4f6;
}

QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #1f2937;
}

QLabel {
    font-weight: 500;
    margin-bottom: 2px;
    color: #4b5563;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 1.5px solid #3b82f6;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    line-height: 1.5;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
}

QTextEdit:focus {
    border: 1.5px solid #3b82f6;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    color: #374151;
}

QPushButton:hover {
    background-color: #f9fafb;
    border-color: #9ca3af;
}

QPushButton:pressed {
    background-color: #f3f4f6;
}

QPushButton:disabled {
    background-color: #e5e7eb;
    color: #9ca3af;
    border-color: #e5e7eb;
}

QPushButton#convertButton {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #2563eb;
}

QPushButton#convertButton:hover {
    background-color: #1d4ed8;
}

QPushButton#convertButton:pressed {
    background-color: #1e40af;
}

QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 12px;
}
"""
