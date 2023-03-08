from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QPushButton, QWidget, QListWidget, QFileDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import QThread, QObject, pyqtSignal, Qt, QUrl

	
class mylistwidget(QListWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		print("a")
	
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
			print("a")
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			print("b")
			event.setDropAction(Qt.DropAction.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			print("c")
			event.setDropAction(Qt.DropAction.CopyAction)	
			event.accept()
			iteminos = []
			for url in event.mimeData().urls():
				print("t")
				if url.isLocalFile():
					print("s")
					print(url.toLocalFile())
					iteminos.append(url.toLocalFile())
			print(iteminos)
			self.addItems(iteminos)
		else:
			event.ignore()	
			

