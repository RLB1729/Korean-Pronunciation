"""Background worker thread for pronunciation engine conversion."""

from PySide6.QtCore import QThread, Signal
from korean_pronunciation import get_pronunciations


class PronunciationWorker(QThread):
    """QThread worker to run the pronunciation engine in the background.

    Keeps the main GUI thread responsive during heavy text processing.
    """
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def run(self):
        try:
            results = get_pronunciations(self.text)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))
