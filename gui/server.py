from PySide.QtGui import *
import socket
import datetime,time
import thread


class server:

    host = ''
    port = 0
    sock_list = list()
    r = 0

    def __init__(self,mainRef,tableWidget):
        self.tableWidget = tableWidget
        self.mainRef = mainRef

        f = open('server.config','r')
        self.host = f.readline().split('=')[1].rstrip()
        self.port = int(f.readline().split('=')[1])
        f.close()
        

    def startListening(self,s):

        self.setLog('Server started...')  
        while(self.runningServer):
            c, addr = s.accept()
            self.setLog('Got new connection from ' + addr[0])

            ##get hostname from IP-address
            hostname = socket.gethostbyaddr(addr[0])[0]
            
            self.sock_list.append((addr[0],c))
            self.tableWidget.insertRow(self.r)
            self.tableWidget.setItem(self.r,0,QTableWidgetItem('connection#'+str(self.r+1)))
            self.tableWidget.setItem(self.r,1,QTableWidgetItem(str(hostname)))
            self.tableWidget.setItem(self.r,2,QTableWidgetItem(addr[0]))
            self.tableWidget.setItem(self.r,3,QTableWidgetItem(str(addr[1])))

            self.tableWidget.setItem(self.r,4,QTableWidgetItem(str('Offline')))
            self.tableWidget.item(self.r, 4).setBackground(QColor(255,120,120))
            
            self.tableWidget.setItem(self.r,5,QTableWidgetItem(str('Stopped')))
            self.tableWidget.item(self.r, 5).setBackground(QColor(255,120,120))
            
            self.r = self.r + 1
            #redraw graphTab
            self.mainRef.redrawGraphTab(self.sock_list)

            

        #s.close()
        self.setLog('Server stopped ') 
        

    def startServer(self):

        self.runningServer = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        s.bind((self.host, self.port))        
        s.listen(5)
        self.ss = s
        try:
            thread.start_new_thread( self.startListening, (s,) )
        except:
           print "Error: unable to start thread"

              

    def stopServer(self):
        self.runningServer = False
        ##attempt: local connection to break accept state of server
        #sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #sf.connect(('localhost', 12344))
        print 'server stopped !!'


    def addStatusLabel(self,labelStatus):
        self.labelStatus = labelStatus

    def setLog(self,msg):
        self.labelStatus.moveCursor(QTextCursor.End,QTextCursor.MoveAnchor)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.labelStatus.append('\n['+st+']:  '+msg)
        
        

