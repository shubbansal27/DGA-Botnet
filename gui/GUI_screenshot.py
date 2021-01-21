__author__ = 'Administrator'

from PySide.QtCore import *
from PySide.QtGui import *
import socket


###################################################################################

class GUI_screenshot:

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
        self.dialog.setWindowTitle('Screenshot')
        self.dialog.setMinimumSize(800,600)

        
        vlayout = QVBoxLayout()
        self.tout = QLabel()
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Dark)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.tout)
        vlayout.addWidget(scrollArea)

        hlayout = QHBoxLayout()

        #btn1
        btn = QPushButton('Take Screenshot')
        btn.clicked.connect(self.receive_screen_shot)
        hlayout.addWidget(btn)
        vlayout.addLayout(hlayout)
        #btn2
        btn2 = QPushButton('size:Original')
        btn2.clicked.connect(self.changeSizeOriginal)
        hlayout.addWidget(btn2)
        #btn3
        btn3 = QPushButton('size:800-600')
        btn3.clicked.connect(self.changeSize800_600)
        hlayout.addWidget(btn3)
        
        #show
        self.dialog.setLayout(vlayout)
        self.dialog.exec_()



    def changeSizeOriginal(self):
        file = 'upload_dir\\scr_'+str(self.port)+'.jpg'
        image = QImage(file)
        self.tout.setPixmap(QPixmap.fromImage(image))


    def changeSize800_600(self):
        file = 'upload_dir\\scr_'+str(self.port)+'.jpg'
        image = QPixmap(file)
        self.tout.setPixmap(image.scaled(800,600,Qt.KeepAspectRatio))
        

    def receive_screen_shot(self):

        row = self.tableWidget.selectedIndexes()[0].row() + 1
        self.port = int(str(row) + self.port_suffix)   
        self.c.send('exec screenshot:'+str(self.port))
        
        sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        sf.bind((self.host, self.port))        
        sf.listen(5)
        cf, addr = sf.accept() 
        #write output in upload_dir
        data = cf.recv(1024)
        f = open('upload_dir\\scr_'+str(self.port)+'.jpg',"wb")
        while data:
            f.write(data)
            data = cf.recv(1024)
        
        print "screenshot output recieved !!"
        cf.close()
        
        file = 'upload_dir\\scr_'+str(self.port)+'.jpg'
        image = QPixmap(file)
        self.tout.setPixmap(image.scaled(800,600,Qt.KeepAspectRatio))
        
            

