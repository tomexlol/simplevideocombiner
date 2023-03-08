from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QPushButton, QWidget, QListWidget, QFileDialog, QMessageBox, QLabel, QProgressBar
from PyQt6 import uic
from PyQt6.QtCore import QThread, QObject, pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QIcon
import VideoConcatenator
import customwidgets
from proglog import TqdmProgressBarLogger
import os
import subprocess, platform
import sys






#esto es para que windows no le ponga icono de python generico en la taskbar
import ctypes
myappid = u'simplevideocombiner' # arbitrary string
if platform.system() == 'Windows':
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


#contextlib for nostdout(). redirigir stderr a otro lado evita que el proglog logee en la consola
#sin esto crashea si corre sin consola xddd
#with nostdout():
#    foo()
import contextlib
import io

@contextlib.contextmanager
def nostdout():
	save_stderr = sys.stderr
	save_stdout = sys.stdout
	sys.stdout = open('trash', 'w')
	sys.stderr = open('trash2', 'w')
	yield
	sys.stdout.close()
	sys.stderr.close()
	sys.stdout = save_stdout
	sys.stderr = save_stderr
	os.remove('trash')
	os.remove('trash2')
	
   
#fixes crash when writing text for windows users
from moviepy.config import change_settings
if platform.system() == 'Windows':    # Windows
	change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe"})




#custom logger para pasar el percentage a la barrita
#no se sacar esta declaración de aca xdd
class MyBarLogger(TqdmProgressBarLogger):
	def callback(self, **changes):
		if len(self.bars):
			percentage = next(reversed(self.bars.items()))[1]['index'] / next(reversed(self.bars.items()))[1]['total']
			asd = barrita(percentage)     


#esto probablemente este implementado como el culo pero funciona no me puedo quejar la verdad
class barrita(QObject):
	progress_signal = pyqtSignal(float)
	def __init__(self, p):
		super().__init__()
		self.p = p
		self.progress_signal.connect(window.update_loading_bar)
		self.progress_signal.emit(p)

		       


#el worker es para que no se cuelgue en el proceso final. toma los parametros necesarios y lo corre en otro thread
class Worker(QObject):
	finished = pyqtSignal()
	result = pyqtSignal(str)
	
	
	def __init__(self, items, settings_clipnumber, settings_filename, settings_timestamps, loggerino):
		super().__init__()
		self.items = items
		self.settings_clipnumber = settings_clipnumber
		self.settings_filename = settings_filename
		self.settings_timestamps = settings_timestamps
		self.loggerino = loggerino


	def run(self):
		with nostdout():
			Combiner = VideoConcatenator.VideoCombinator(self.items)
			Combiner.mergeVideos(self.settings_clipnumber, self.settings_filename, self.settings_timestamps, self.loggerino)
			self.result.emit(f"{os.getcwd()}/SimplyCombinedVideo.mp4")
			self.finished.emit()
		


class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.residing_folder = os.getcwd()
		try:
			os.chdir(sys._MEIPASS)
		except:
			pass
		uic.loadUi("svc.ui", self)
		self.setWindowIcon(QIcon('icon.ico'))
		os.chdir(self.residing_folder)
		#este lio con las folders es para el pyinstaller - sino al correr el .exe portable, tu cwd es un _temp horrible (sys._MEIPASS)y te queda todo ahi


		self.setFixedSize(705, 570)
		#buttons
		self.button_arrow_up = self.findChild(QPushButton, "button_arrow_up")
		self.button_arrow_down = self.findChild(QPushButton, "button_arrow_down")
		self.button_generate_video = self.findChild(QPushButton, "button_generate_video")
		self.button_browse_files = self.findChild(QPushButton, "button_browse_files")
		self.button_open_result = self.findChild(QPushButton, "button_open_result")
		self.button_open_result.hide()
		
		#settings checkboxes
		self.checkbox_settings_timestamps = self.findChild(QCheckBox, "checkbox_settings_timestamps")
		self.checkbox_settings_filename = self.findChild(QCheckBox, "checkbox_settings_filename")
		self.checkbox_settings_clipnumber = self.findChild(QCheckBox, "checkbox_settings_clipnumber")
		
		#list of video files
		self.list_video_files = self.findChild(customwidgets.mylistwidget, "list_video_files")
		
		#status above loading bar
		self.label_status = self.findChild(QLabel, "label_status")
		
		
		
		#loadingbar
		self.bar_loading = self.findChild(QProgressBar, "bar_loading")
		self.bar_loading.setRange(0, 100)
		self.bar_loading.setValue(0)
		self.bar_loading.hide()
		
		
		#button connections
		self.button_arrow_up.clicked.connect(self.arrowUp)
		self.button_arrow_down.clicked.connect(self.arrowDown)	
		self.button_browse_files.clicked.connect(self.fileBrowser)					
		self.button_generate_video.clicked.connect(self.videoGenerator)
		self.button_delete.clicked.connect(self.remove_from_list)
		self.button_open_result.clicked.connect(self.open_result)
		
		
	def fileBrowser(self):
		os.chdir(self.residing_folder)
		fname = QFileDialog.getOpenFileNames(self, "Select Video Files", "", "All Files (*)")
		if fname:
			self.list_video_files.addItems(fname[0])
		
	def arrowUp(self):
		currentRow = self.list_video_files.currentRow()
		currentItem = self.list_video_files.takeItem(currentRow)
		self.list_video_files.insertItem(currentRow - 1, currentItem)
		self.list_video_files.setCurrentRow(currentRow - 1)
		
	def arrowDown(self):		
		currentRow = self.list_video_files.currentRow()
		currentItem = self.list_video_files.takeItem(currentRow)
		self.list_video_files.insertItem(currentRow + 1, currentItem)
		self.list_video_files.setCurrentRow(currentRow + 1)	
	
	
	def videoGenerator(self):
		os.chdir(self.residing_folder)
		#no deberia hacer falta pero por las dudas. para evitar estar en sys._MEIPASS
		
		self.items = [self.list_video_files.item(x).text() for x in range(self.list_video_files.count())]
		
		self.myThread = QThread()
		self.log_object = MyBarLogger()
		self.worker = Worker(self.items, self.checkbox_settings_clipnumber.isChecked(), self.checkbox_settings_filename.isChecked(), self.checkbox_settings_timestamps.isChecked(), self.log_object)
		self.worker.moveToThread(self.myThread)
		self.worker.result.connect(self.handleResult)
		self.myThread.started.connect(self.worker.run)
		self.myThread.finished.connect(self.myThread.quit)
		self.button_generate_video.setEnabled(False)
		self.label_status.setText("Processing...")
		self.bar_loading.show()
		self.myThread.start()
	

		
	def handleResult(self, result):
		os.chdir(self.residing_folder)
		#no deberia hacer falta pero por las dudas. para evitar estar en sys._MEIPASS
		
		self.label_status.setText("Processing complete - Combined video ready!")
		self.button_generate_video.setEnabled(True)
		self.button_open_result.show()
		done_box = QMessageBox(window)
		done_box.setText(f"Your video is ready: \n {result}")
		done_box.setWindowTitle("SimpleVideoCombiner - Video Complete!")
		open_button = QPushButton("Open File")
		ok_button = QPushButton("Close")
		done_box.addButton(open_button, QMessageBox.ButtonRole.ActionRole)
		done_box.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
		done_box.exec()
		filepath = result
		window.filepath = result
		if done_box.clickedButton() == open_button:
			if platform.system() == 'Darwin':       # macOS
					subprocess.call(('open', filepath))
			elif platform.system() == 'Windows':    # Windows
				os.startfile(filepath)
			else:                                   # linux variants
				subprocess.call(('xdg-open', filepath))
		#funciona pero no se centerea..
		self.myThread.quit()

		
		#aca iria lo que queres que pase cuando esté listo
	
	
	def remove_from_list(self):
		self.list_video_files.takeItem(self.list_video_files.currentRow())

	
	def update_loading_bar(self, value):
		self.bar_loading.setValue(int(value * 100))


		
	def open_result(self):
		if platform.system() == 'Darwin':       # macOS
				subprocess.call(('open', self.filepath))
		elif platform.system() == 'Windows':    # Windows
			os.startfile(self.filepath)
		else:                                   # linux variants
			subprocess.call(('xdg-open', self.filepath))		



app = QApplication([])
window = MyWindow()
window.setWindowTitle("SimpleVideoCombiner")
window.show()
app.exec()
