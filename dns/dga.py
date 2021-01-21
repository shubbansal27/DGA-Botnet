import urllib2
from bs4 import BeautifulSoup            

def generate(word1,word2):
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
    

def twitter_dga(catg):
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
    return generate(word1,word2)


def date_dga(year,month,day):

    domain = ''

    for i in range(16):
        year = ((year ^ 8 * year) >> 11) ^ ((year & 0xFFFFFFF0) << 17)
        month = ((month ^ 4 * month) >> 25) ^ 16 * (month & 0xFFFFFFF8)
        day = ((day ^ (day << 13)) >> 19) ^ ((day & 0xFFFFFFFE) << 12)
        domain += chr(((year ^ month ^ day) % 25) + 97)

    domain = domain+'.nsproject.in'
    return domain

