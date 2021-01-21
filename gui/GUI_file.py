__author__ = 'Administrator'

from PySide.QtGui import *
from PySide.QtCore import Slot,QTime,SIGNAL
import socket


###################################################################################

class GUI_file:

    host = ''
    port = 0
    port_suffix = '2345'

    def __init__(self):

        f = open('server.config','r')
        self.host = f.readline().split('=')[1].rstrip()
        f.close()

    
    def openDialog(self,frame,c,tableWidget):

        self.c = c
        self.tableWidget = tableWidget
        #dialog
        self.dialog = QDialog(frame)
        self.dialog.setWindowTitle('File-Download')
        self.dialog.setMinimumSize(650,150)

        
        vlayout = QVBoxLayout()
       
        hlayout = QHBoxLayout()
        self.tcmd = QTextEdit()
        self.tcmd.setMaximumHeight(40)
        font = QFont('Arial',10,QFont.Bold)
        self.tcmd.setFont(font)

        pathLabel = QLabel('Path')
        hlayout.addWidget(pathLabel)
        btn = QPushButton('Download')
        btn.clicked.connect(self.cmd_module)
        btn.setMaximumHeight(40)
        hlayout.addWidget(self.tcmd)
        hlayout.addWidget(btn)
        vlayout.addLayout(hlayout)

        self.tout = QTextEdit()
        self.tout.setMinimumHeight(60)
        self.tout.setReadOnly(True)
        vlayout.addWidget(self.tout)
        
        #show
        self.dialog.setLayout(vlayout)
        self.dialog.exec_()



    def cmd_module(self):
        
        row = self.tableWidget.selectedIndexes()[0].row()
        self.port = int(str(row) + self.port_suffix)
        self.c.send('exec file:'+str(self.port))
        
        path = self.tcmd.toPlainText()
        self.c.send(path)
        sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        sf.bind((self.host, self.port))        
        sf.listen(5)
        cf, addr = sf.accept() 
        #write output in upload_dir
        data = cf.recv(1024)
        tmp = path.split('\\')
        down_file = 'download_dir//' + tmp[len(tmp)-1] 
        f = open(down_file,"wb")
        while data:
            f.write(data)
            data = cf.recv(1024)
        
        print "file_download output recieved !!"
        cf.close() 
        ##display in tout
        self.tout.clear()
        self.tout.append("File download complete !!\n\n")
        self.tout.append("Downloaded path = " + down_file + '\n\n')
        self.tout.append(':) :) :)\n')
        

