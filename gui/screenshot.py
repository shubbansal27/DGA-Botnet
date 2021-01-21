#import pyscreenshot as ImageGrab
from PIL import ImageGrab
from ctypes import windll, Structure, c_ulong, byref
import win32gui

def capture():

    #flags, hcursor, (x,y) = win32gui.GetCursorInfo()
    #print x,'-',y


    # fullscreen
    im=ImageGrab.grab()
    ##im.show()
     
    # part of the screen
    #if (x-150) >= 0 and (y-150) >= 0 and (x+200) <= 1535 and (y+200) <= 863 :
    #    im=ImageGrab.grab(bbox=(x-150,y-150,x+200,y+200))
    #    im.show()
    #else:
    #    im=ImageGrab.grab()
     
    # to file
    im.save('scr.jpg', 'JPEG')

