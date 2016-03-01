# Extracting main article content from a url, using BeautifulSoup

from bs4 import BeautifulSoup
import urllib2

# First function is for WashingtonPost: It will take in the url and return the article & title_of_article
# Exploiting the property of www.washingtonpost.com- that it encloses the main body of the article in a special <article></article> tag;

def WashingtonPost(url):
    # Download the URL
    webpage = urllib2.urlopen(url).read().decode('utf8')

    # Soup object
    soup = BeautifulSoup(webpage)
    someText = ' '.join(map(lambda x: x.text, soup.find_all('article')))

    # We have everything in between our article tags; but that also includes some crud we do not need; Real stuff is inside <p></p>
    soup2 = BeautifulSoup(someText)
    articleBody = ' '.join(map(lambda x: x.text, soup2.find_all('p')))

    return soup.title.text, articleBody


# Use the above function
url = "https://www.washingtonpost.com/politics/on-a-fateful-super-tuesday-polls-have-opened-across-the-south-and-new-england/2016/03/01/995c7ec4-df64-11e5-846c-10191d1fc4ec_story.html?hpid=hp_hp-top-table-main_supertuesdayweb-715am%3Ahomepage%2Fstory"

output = WashingtonPost(url)    # Returns a list of two items

print "TITLE:", output[0]
print "Article Body:", output[1]