import win32api, win32con, win32gui
from ctypes import *
import thread
import socket

#
# Device change events (WM_DEVICECHANGE wParam)
#
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018

#
# type of device in DEV_BROADCAST_HDR
#
DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYPE_PORT = 0x00000003
DBT_DEVTYPE_NET = 0x00000004

#
# media types in DBT_DEVTYP_VOLUME
#
DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002

WORD = c_ushort
DWORD = c_ulong

class DEV_BROADCAST_HDR (Structure):
  _fields_ = [
    ("dbch_size", DWORD),
    ("dbch_devicetype", DWORD),
    ("dbch_reserved", DWORD)
  ]

class DEV_BROADCAST_VOLUME (Structure):
  _fields_ = [
    ("dbcv_size", DWORD),
    ("dbcv_devicetype", DWORD),
    ("dbcv_reserved", DWORD),
    ("dbcv_unitmask", DWORD),
    ("dbcv_flags", WORD)
  ]

def drive_from_mask (mask):
  n_drive = 0
  while 1:
    if (mask & (2 ** n_drive)): return n_drive
    else: n_drive += 1

class Notification:

  def __init__(self,host,port):

    self.host = host
    self.port = port
    
    message_map = {
      win32con.WM_DEVICECHANGE : self.onDeviceChange
    }

    wc = win32gui.WNDCLASS ()
    hinst = wc.hInstance = win32api.GetModuleHandle (None)
    wc.lpszClassName = "DeviceChangeDemo"
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
    wc.hCursor = win32gui.LoadCursor (0, win32con.IDC_ARROW)
    wc.hbrBackground = win32con.COLOR_WINDOW
    wc.lpfnWndProc = message_map
    classAtom = win32gui.RegisterClass (wc)
    style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
    self.hwnd = win32gui.CreateWindow (
      classAtom,
      "Device Change Demo",
      style,
      0, 0,
      win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
      0, 0,
      hinst, None
    )

  def onDeviceChange (self, hwnd, msg, wparam, lparam):

    f = open('usb.txt','wb')
    
    dev_broadcast_hdr = DEV_BROADCAST_HDR.from_address (lparam)
    #print wparam
    if wparam == DBT_DEVICEARRIVAL:
      #print "USB inserted !!"
      #f.write('USB inserted !!\n')

      if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:
        #print "It's a volume!"
        #f.write('Its a volume!\n')

        dev_broadcast_volume = DEV_BROADCAST_VOLUME.from_address (lparam)
        drive_letter = drive_from_mask (dev_broadcast_volume.dbcv_unitmask)
        #print "1 ", chr (ord ("A") + drive_letter)
        f.write('1 ' +  str(chr (ord ("A") + drive_letter)) + '\n')
      elif wparam == DBT_DEVICEREMOVECOMPLETE:
        #print 'USB removed !!'
        f.write('0 X\n')
    else:
      #print ' usb state changed!!'
      f.write('2 X\n')


    f.close()

    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sf.connect((self.host, self.port))
    f = open('usb.txt','rb')
    data = f.read(1024)
    while data:
        sf.send(data)
        data = f.read(1024)
    f.close()    
    sf.close()
  
    #print "usb-status Sending Completed"
    
    return 1


class usb_monitor:

  def thread_run(self,host,port):
    #print 'debug1'
    w = Notification(host,port)
    win32gui.PumpMessages ()

    
    

  def start(self,host,port):
    try:
      thread.start_new_thread( self.thread_run, (host,port,) )
    except:
      print "Error: unable to start usb_monitor thread"




#usb_monitor().start('172.17.12.67',12346)


#if __name__=='__main__':
#  w = Notification ()
#  win32gui.PumpMessages ()
