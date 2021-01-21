__author__ = 'Administrator'

from PySide.QtGui import *
from PySide.QtCore import Slot,QTime,SIGNAL
import socket
import thread

###################################################################################

class GUI_usb:

    host = ''
    port = 0
    port_suffix = '2347'
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
        self.dialog.setWindowTitle('USB-monitor')
        self.dialog.setMinimumSize(600,300)

        
        vlayout = QVBoxLayout()
        self.tout = QTextEdit()
        self.tout.setMinimumHeight(250)
        self.tout.setReadOnly(True)
        vlayout.addWidget(self.tout)

        hlayout = QHBoxLayout()
        btn = QPushButton('Start driver')
        btn.clicked.connect(self.usb_module)
        btn.setMaximumHeight(40)
        hlayout.addWidget(btn)
        vlayout.addLayout(hlayout)

        #show
        self.dialog.setLayout(vlayout)
        self.dialog.exec_()


    def thread_usb_server(self,x):

        print 'debug-1'
        while True:        
            sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
            sf.bind((self.host, self.port))        
            sf.listen(5)
        
            cf, addr = sf.accept() 
            #write output in upload_dir
        
            data = cf.recv(1024)
            f = open('upload_dir//usb_'+str(self.port)+'.txt',"wb")
            while data:

                dat = data.split(' ')
                self.tmp_buffer = self.tmp_buffer + dat[0]
                #f.write(data + ' ==> ' + self.tmp_buffer+'\n')

                #row = self.tableWidget.selectedIndexes()[0].row()
                row = int(str(self.port)[0])-1

                if dat[0] == '1':
                    data = 'USB inserted, drive: '+ dat[1] + '\n'
                    self.tableWidget.setItem(row,4,QTableWidgetItem(str('Online ('+dat[1]+':)')))
                    self.tableWidget.item(row, 4).setBackground(QColor(0,255,0))
                    f.write(data)
                    self.tmp_buffer = ''
                elif dat[0] == '0':
                    data = 'USB removed\n'
                    self.tableWidget.setItem(row,4,QTableWidgetItem(str('Offline')))
                    self.tableWidget.item(row, 4).setBackground(QColor(255,120,120))
                    f.write(data)
                    self.tmp_buffer = ''
                else:    
                    if self.tmp_buffer == '222':
                        data = 'USB removed\n'
                        self.tableWidget.setItem(row,4,QTableWidgetItem(str('Offline')))
                        self.tableWidget.item(row, 4).setBackground(QColor(255,120,120))
                        f.write(data)
                        self.tmp_buffer = ''
                    
                data = cf.recv(1024)
                
            print "usb output recieved !!"
            cf.close()
            
           #self.tout.clear()
            f = open('upload_dir//usb_'+str(self.port)+'.txt',"r")
            for line in f:
                self.tout.append(line)
            f.close()


    def usb_module(self):

        row = self.tableWidget.selectedIndexes()[0].row() + 1
        self.port = int(str(row) + self.port_suffix)        
        self.c.send('exec usb_monitor:'+str(self.port))
        try:
            thread.start_new_thread( self.thread_usb_server, ('',) )
        except:
            print "Error: unable to start usb_monitor_server thread"
            


