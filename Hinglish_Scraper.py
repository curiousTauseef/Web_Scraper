from bs4 import BeautifulSoup
import urllib2


# Scraping Hinglish SMS from http://www.santabanta.com/sms/clean/hinglish/450/

def SantaBanta_SMS(url):
    direc = 'santabanta_data/'
    for i in range(1,32):
        webpage = urllib2.urlopen(url+str(i)).read().decode('utf8')
        soup = BeautifulSoup(webpage)
        text = ' '.join(map(lambda x: x.text, soup.find_all("span", {"class":"sms_text display_block"})))
        f = open(direc+'sms_'+str(i)+'.txt', 'w')
        f.write(text.encode('utf8'))
        f.close()


# Hinglish jokes: http://jokes.lipy.com/tags/hinglish/page/1

def JokesLipy(url):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)
    text = ' '.join(map(lambda x: x.text, soup.findAll("div", {"class":"j-q-description"})))
    return text


#url = 'http://www.santabanta.com/sms/clean/hinglish/450/?page='
#SantaBanta_SMS(url)

url = 'http://jokes.lipy.com/tags/hinglish/page/1'
print JokesLipy(url)