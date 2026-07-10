import sys
from PyQt6.QtWidgets import QApplication
from styles import DARK_STYLE

from ui import MainWindow



app = QApplication(sys.argv)
app.setStyleSheet(DARK_STYLE)

window = MainWindow()
window.show()

sys.exit(app.exec())
