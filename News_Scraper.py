# Extracting main article content from a url, using BeautifulSoup
from bs4 import BeautifulSoup
import urllib2
from cookielib import CookieJar
import requests

# The functions will take as input the url and return the article & title_of_article


# For WashingtonPost
# Article is inside <article></article>
def WashingtonPost(url):
    try:
        webpage = urllib2.urlopen(url).read().decode('utf8')
    except:
        return (None, None)
    soup = BeautifulSoup(webpage)
    
    inside_article = str(soup.find_all('article'))
    # The real info is inside the <p> tags of these <article> tags
    
    soup2 = BeautifulSoup(inside_article, "html.parser")
    #"html.parser" is a crucial argument : http://stackoverflow.com/questions/14822188/dont-put-html-head-and-body-tags-automatically-beautifulsoup

    articleBody = ' '.join(map(lambda x: x.text, soup2.find_all('p')))
    
    return soup.title.text, articleBody


# For TheHindu
# Article is inside <p class="body"></p>
def TheHindu(url):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)

    # It contains a sub-heading in a div "articleLead"; Let's take care of that
    sub_heading = ''.join(soup.find("div", {"class" : "articleLead"}).text)
    
    articleBody = ' '.join(map(lambda x: x.text, soup.find_all("p", {"class" : "body"})))
    
    article = sub_heading + articleBody
    return soup.title.text, article


# For TheNewYorkTimes
# Article is inside <p class="story-body-text story-content"></p>
def NYtimes(url):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    webpage = opener.open(url).read().decode('utf8')

    # Gives HTTP infinite loop error on using: webpage = urllib2.urlopen(url).read().decode('utf8')
    # Checkout: http://stackoverflow.com/questions/9926023/handling-rss-redirects-with-python-urllib2
    
    soup = BeautifulSoup(webpage)

    a_list_of_tags = soup.find_all("p", {"class" : "story-body-text story-content"})

    articleBody = ' '.join(map(lambda x: x.text, a_list_of_tags))
    
    return soup.title.text, articleBody


# For CNN
def CNN(url):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)
    # Article is inside <p> tags for money.cnn {except the last few <p> tags}
    if "money.cnn" in url:
        all_p_tags = []
        for tag in soup.findAll("p"):
            all_p_tags.append(tag)

        article = ""
        for x in all_p_tags[:-2]:
            article += x.text

    # Article inside <p class="zn-body__paragraph"> for edition.cnn
    elif "edition.cnn" in url:
        article = " ".join(map(lambda x: x.text, soup.find_all("p", {"class" : "zn-body__paragraph"})))

    return soup.title.text, article


# For Hindustan Times
def HindustanTimes(url):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)
    
    article = ' '.join(map(lambda x: x.text, soup.findAll("p")))

    return soup.title.text, article



# Main Scraper Function for Washington:
# Tech: It's either switch or innovation
def Scraper(url, distinguisher='2016'):
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    
    all_content = {}
    
    errors  = 0
    for link in soup.find_all('a'):
        try:
            _url = link['href']
            if _url not in all_content and '2016' in _url and 'washington' in _url and ('switch' in _url or 'innovation' in _url) and '.com/video/' not in _url:
                article = WashingtonPost(_url)
                if len(article) > 0:
                    all_content[_url] = article
#                print _url + "  "

        except:
            errors += 1

    return all_content

url = "https://www.washingtonpost.com/business/technology/"
print Scraper(url)

# Using the above functions

#url1 = "https://www.washingtonpost.com/politics/on-a-fateful-super-tuesday-polls-have-opened-across-the-south-and-new-england/2016/03/01/995c7ec4-df64-11e5-846c-10191d1fc4ec_story.html?hpid=hp_hp-top-table-main_supertuesdayweb-715am%3Ahomepage%2Fstory"
#url2 = "http://www.thehindu.com/business/budget/highlights-of-union-budget-201617/article8295451.ece?homepage=true"
#url3 = "http://www.nytimes.com/2016/03/02/technology/apple-and-fbi-face-off-before-house-judiciary-committee.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news"
#url4 = "http://money.cnn.com/2016/03/09/technology/bolt-electric-bike/index.html"
#url4 = "http://edition.cnn.com/2016/03/14/world/exomars-mars-methane-mission-launch-irpt/index.html"
#url5 = "http://www.hindustantimes.com/tech/reboot-reality-now-swim-with-sharks-sing-with-paul-mccartney-on-virtual-reality-headsets/story-beTNUkO5kkCxL9tUJIeeOO.html"
#url = "http://www.thehindu.com/sci-tech/technology/gadgets/apple-unveils-smaller-iphone-se-starting-at-399/article8382305.ece"

#output = WashingtonPost(url1)    # Returns a list of two items
#output = TheHindu(url)
#output = NYtimes(url3)
#output = CNN(url4)
#output = HindustanTimes(url5)
#url = raw_input('Enter a NYtimes url: ')
#print "\nTITLE:", output[0]
#print "\nArticle Body:", output[1]