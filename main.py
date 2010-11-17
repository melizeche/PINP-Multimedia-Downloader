#!/usr/bin/python

import sys
from PyQt4 import QtCore, QtGui, QtNetwork
#from PyQt4 import QtNetwork
from gui import Ui_MainWindow

import thread
import platform
import os
from threading import *
import thread, threading
import ConfigParser
import sys

from pinp import *
global t0,downPath, ver,confFile

ver='0.6.5'


class StartQT4(QtGui.QMainWindow):
	global index, info, t0	,downPath
	def __init__(self, parent=None):
		#print "2"
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.lineEdit.setText("Depeche")
		if platform.system() == 'Linux':
			print "Pinp Media Downloader "+ ver +" para " + platform.system()
		self.ui.statusbar.showMessage("Pinp Media Downloader "+ ver +" para " + platform.system())	
		
		self.ui.http =  QtNetwork.QHttp(self)
		self.ui.httpGetId=0
		self.ui.progressDialog = QtGui.QProgressDialog(self)
		
		self.ui.http.requestFinished.connect(self.httpRequestFinished)
		self.ui.http.dataReadProgress.connect(self.updateDataReadProgress)
		self.ui.http.responseHeaderReceived.connect(self.readResponseHeader)
		self.ui.progressDialog.canceled.connect(self.cancelDownload)
		#Conectamos las Funciones
		
		QtCore.QObject.connect(self.ui.actionSalir, QtCore.SIGNAL("activated()"), self.salir)
		#tab1
		QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("returnPressed()"), self.buscar)
		QtCore.QObject.connect(self.ui.searchButton, QtCore.SIGNAL("clicked()"), self.buscar)
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),self.bajar)
		#QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("currentRowChanged ()"), self.prueba)
		#tab3
		QtCore.QObject.connect(self.ui.dirButton, QtCore.SIGNAL("clicked()"), self.selectDir)
		###
		self.leerConf()
		####
		#QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),self.bajar) #thread.start_new_thread(self.bajar,(None,None)))

		#QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), thread.start_new_thread(self.bajar,(None,None)))

		#QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("itemClicked()"), self.bajar)

	
	def prueba(self):
		print "entre!"
	def leerConf(self):
		global downPath,confFile
		#Dependiendo si es Windows o Linux vemos donde se van a guardar por defecto los archivos
		if(platform.system() == 'Windows'):
			downPath = os.environ["USERPROFILE"]
		else:
			downPath = os.environ["HOME"]
			print downPath
		confFile = downPath + '//''.pinp.cfg'
		if(os.path.exists(confFile)):
			config = ConfigParser.RawConfigParser()
			config.read(confFile)
			downPath = config.get('download','path')
			self.ui.dirEdit.setText(downPath)
		else:
			#Dependiendo si es Windows o Linux vemos donde se van a guardar por defecto los archivos			
#			if(platform.system() == 'Windows'):
#				downPath = os.environ["USERPROFILE"]
#			else:
#				downPath = os.environ["HOME"]
#				print downPath
			# escribimos la configuracion
			self.ui.dirEdit.setText(downPath)
			#Creamos y guardamos la configuracion
			config = ConfigParser.RawConfigParser()
			config.add_section('download')
			config.set('download', 'path', downPath)
			with open(confFile, 'wb') as configfile:
				config.write(configfile)

	def selectDir(self):
		global downPath,confFile
		#print "sele"
		dialog = QtGui.QFileDialog(self)
		#dialog.setFileMode = QtGui.QFileDialog.Directory
		#dialog.open()
		#dir = open(dialog.getExistingDirectory()).read()
		dir = dialog.getExistingDirectory()
		self.ui.dirEdit.setText(dir)
		downPath = dir
		config = ConfigParser.RawConfigParser()
		config.add_section('download')
		config.set('download', 'path', dir)
		# Writing our configuration file to 'example.cfg'
		with open(confFile, 'wb') as configfile:
			config.write(configfile)
		
		#print dir
		#filename=QtGui.QFileDialog.getOpenFileName("", "*.py", self, "FileDialog")
		
	def GUIformat_bytes(self,bytes):
			if bytes is None:
				return 'N/A'
			if bytes == 0:
				exponent = 0
			else:
				exponent = long(math.log(float(bytes), 1024.0))
				suffix = 'bkMGTPEZY'[exponent]
				converted = float(bytes) / float(1024**exponent)
				return '%.2f%s' % (converted, suffix)
	
	def GUIcalc_speed(self,start, now, bytes):
		dif = now - start
		if bytes == 0 or dif < 0.001: # One millisecond
			return '%10s' % '---b/s'
		return '%10s' % ('%s/s' % self.GUIformat_bytes(float(bytes) / dif))
	
	
	def GUIdlProgress(self,count, blockSize, totalSize):
		global t0
		if t0==0:
			t0=time.time()
		percent = int(count*blockSize*100/totalSize)
		#tam=format_bytes(count*blockSize)
		sys.stdout.write("\r" + info[1] + " - " + info[2] + ".mp3" + "\t%d%% \t%s" % (percent, self.GUIcalc_speed(t0,time.time(),count*blockSize)))
		sys.stdout.flush()
		
	def guigodown(self):
	#	print info
		global info,downPath
		arch = downPath + '//' + info[1] + " - " + info[2] + ".mp3"
		urllib.urlretrieve(info[0], arch, reporthook=self.GUIdlProgress)


	class downThread(Thread):
		def __init__(self, name, *args):
			self.counter=0
			#print "4"
			#self.name=name
			a=name
			apply(Thread.__init__, (self, ) + args)
			#print "5"
			#run(Thread.__init__, (self, ) + args)
			#self.run(self)
        def run(self):
			#print "6"
			while self.counter < 200:
				print self.name, self.counter
				self.counter = self.counter + 1
				self.ui.lineEdit.setText(str(self.counter))
				time.sleep(1)


		

	
	def bajar(self):
		global index
		global info
		global t0
		t0=0
		select =  self.ui.listWidget.currentRow()
		#print select
		
		#print index[select][2]
		
		#print index[select][2]
		
		xml = rape(index[select][1])
		
		#print xml
		
		#print xml
		
		info = stripping(xml)
		#print info
		
		#self.guigodown()
		#print "1"
		# self.thread1=self.downThread("thread1")
		#print "2"
		#self.thread1.start()
		#self.thread1.jpio
		#self.thread1.run()
		#print "3"
		
		
		#Este funciona
		#self.guigodown()
		##Prueba Gui
		self.downloadFile()
		
		#arch = info[1] + " - " + info[2] + ".mp3"
		#urllib.urlretrieve(info[0], arch, reporthook=GUIdlProgress)    

	
		
	def buscar(self):
		global index
		print "buscando: "
		#self.ui.searchButton.setText("Buscando...")
		self.ui.listWidget.clear()
		#self.ui.lineEdit.setText("Depeche")
		#self.ui.listWidget.addItem("HOOOOL")
		#print self.ui.lineEdit.text().toASCII()
		st = unicode(self.ui.lineEdit.text())
		st= st.encode("utf-8")
		#print urllib.quote(st)
		#st.encode("ascii","ignore")
		#print self
		#print self.ui
		#print self.ui.lineEdit.displayText()
		#print self.ui.lineEdit.text()
		print st
		
		index = goHunt(st)
		#print index
		for i in range(len(index)):
			self.ui.listWidget.addItem(unicode(index[i][0]) + ".\t" + unicode(index[i][2]))
		#self.ui.searchButton.setText("Buscar")		
		
	def salir(self):
		print "Chauu"
		sys.exit(0)
		
	def downloadFile(self):
		global info,downPath
		print info[0]
		self.ui.http =  QtNetwork.QHttp(self)
		
		url = QtCore.QUrl(info[0])
		print url
		arch = downPath + '//' + info[1] + " - " + info[2] + ".mp3"
		fileInfo = QtCore.QFileInfo(url.path())
		fileName = fileInfo.fileName()
		#fileName = downPath + '//' + info[1] + " - " + info[2] + ".mp3"

		#if not fileName:
		#	fileName = 'index.html'

		if QtCore.QFile.exists(fileName):
			ret = QtGui.QMessageBox.question(self, "HTTP",
                    "Ya existe un archivo con el nombre %s en  "
                    "la carpeta" % fileName,
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Cancel)

			if ret == QtGui.QMessageBox.Cancel:
				return

			QtCore.QFile.remove(fileName)

		self.outFile = QtCore.QFile(fileName)
		if not self.outFile.open(QtCore.QIODevice.WriteOnly):
			QtGui.QMessageBox.information(self, "HTTP","Imposible guardar el archivo %s: %s." % (fileName, self.outFile.errorString()))
			self.outFile = None
			return

		#if url.scheme().lower() == 'https':
			#mode = QtNetwork.QHttp.ConnectionModeHttps
		#else:
			#mode = QtNetwork.QHttp.ConnectionModeHttp
		mode = QtNetwork.QHttp.ConnectionModeHttp
		port = url.port()

		if port == -1:
			port = 0
		
		#print self
		#print self.ui
		
		self.ui.http.setHost(url.host(), mode, port)
		

		#if url.userName():
		#	self.http.setUser(url.userName(), url.password())

		self.httpRequestAborted = False
		
		path = QtCore.QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
		if path:
			try:
				# Python v3.
				path = str(path, encoding='utf-8')
			except TypeError:
				# Python v2.
				path = str(path)
		else:
			path = '/'
		#path=info[0]
		self.ui.httpGetId = self.ui.http.get(path, self.outFile)

		self.ui.progressDialog.setWindowTitle("HTTP")
		self.ui.progressDialog.setLabelText("Descargando %s." % fileName)
		#self.ui.downloadButton.setEnabled(False)
		print ("Downloading %s." % fileName)
	
	def httpRequestFinished(self, requestId, error):
		http = QtNetwork.QHttp()
		if requestId != self.ui.httpGetId:
			return

		if self.httpRequestAborted:
			if self.outFile is not None:
				self.outFile.close()
				self.outFile.remove()
				self.outFile = None

			self.ui.progressDialog.hide()
			return

		self.ui.progressDialog.hide()
		self.outFile.close()

		if error:
			self.outFile.remove()
			QtGui.QMessageBox.information(self, "HTTP",
						"Fallo la descarga: %s." % self.ui.http.errorString())
		else:
			fileName = QtCore.QFileInfo(QtCore.QUrl(self.ui.lineEdit.text()).path()).fileName()
			self.ui.lineEdit.setText("Se descargo %s " % fileName)

		#self.downloadButton.setEnabled(True)
		self.outFile = None


	def updateDataReadProgress(self, bytesRead, totalBytes):
		if self.httpRequestAborted:
			return

		self.ui.progressDialog.setMaximum(totalBytes)
		self.ui.progressDialog.setValue(bytesRead)
		
	def readResponseHeader(self, responseHeader):
		# Check for genuine error conditions.
		if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
			QtGui.QMessageBox.information(self, "HTTP",
					"La descarga fallo: %s." % responseHeader.reasonPhrase())

	def cancelDownload(self):
		http = QtNetwork.QHttp()
		#self.ui.statusbar.push("Download canceled.")
		self.ui.httpRequestAborted = True
		self.ui.http.abort()
		#self.ui.downloadButton.setEnabled(True)
	
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    #print "1"
    #self = QtGui.QMainWindow
    #self.ui = Ui_MainWindow()
    #conectarSlots()
    myapp.show()
    sys.exit(app.exec_())
