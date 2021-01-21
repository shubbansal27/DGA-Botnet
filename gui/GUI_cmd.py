__author__ = 'Administrator'

from PySide.QtGui import *
from PySide.QtCore import Slot,QTime,SIGNAL
import socket


###################################################################################

class GUI_cmd:

    host = ''
    port = 0
    port_suffix = '2346'

    def __init__(self):

        f = open('server.config','r')
        self.host = f.readline().split('=')[1].rstrip()
        f.close()

    
    def openDialog(self,frame,c,tableWidget):

        self.c = c
        self.tableWidget = tableWidget
        #dialog
        self.dialog = QDialog(frame)
        self.dialog.setWindowTitle('Console')
        self.dialog.setMinimumSize(600,300)

        
        vlayout = QVBoxLayout()
        self.tout = QTextEdit()
        self.tout.setMinimumHeight(250)
        self.tout.setReadOnly(True)
        vlayout.addWidget(self.tout)

        hlayout = QHBoxLayout()
        self.tcmd = QTextEdit()
        self.tcmd.setMaximumHeight(40)
        font = QFont('Arial',10,QFont.Bold)
        self.tcmd.setFont(font)
        
        btn = QPushButton('Submit')
        btn.clicked.connect(self.cmd_module)
        btn.setMaximumHeight(40)
        hlayout.addWidget(self.tcmd)
        hlayout.addWidget(btn)
        vlayout.addLayout(hlayout)

        #show
        self.dialog.setLayout(vlayout)
        self.dialog.exec_()



    def cmd_module(self):
        
        row = self.tableWidget.selectedIndexes()[0].row() + 1
        self.port = int(str(row) + self.port_suffix)
        #print str(row),self.port_suffix,self.port
        self.c.send('exec cmd:'+str(self.port))
        
        command = self.tcmd.toPlainText()
        self.c.send(command)
        sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        sf.bind((self.host, self.port))        
        sf.listen(5)
        cf, addr = sf.accept() 
        #write output in upload_dir
        data = cf.recv(1024)
        f = open('upload_dir//cmd_'+str(self.port)+'.txt',"wb")
        #print 'upload_dir//cmd_'+str(self.port)+'.txt'
        while data:
            f.write(data)
            data = cf.recv(1024)
        
        print "cmd output recieved !!"
        cf.close() 
        ##display in tout
        self.tout.clear()
        f = open('upload_dir//cmd_'+str(self.port)+'.txt',"r")
        for line in f:
            self.tout.append(line)
        f.close()
            

