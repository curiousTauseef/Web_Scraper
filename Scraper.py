# Extracting main article content from a url, using BeautifulSoup
from bs4 import BeautifulSoup
import urllib2

################################################################################
# First function is for WashingtonPost: It will take in the url and return the article & title_of_article
# Exploiting the property of www.washingtonpost.com- that it encloses the main body of the article in a special <article></article> tag;

def WashingtonPost(url):
    # Download the URL
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)
    
    inside_article = str(soup.find_all('article'))
    # We are inside the <article> </article> tags now
    # The real info is inside the <p> tags of these <article> tags!
    
    soup2 = BeautifulSoup(inside_article, "html.parser")
    #"html.parser" is a crucial argument : http://stackoverflow.com/questions/14822188/dont-put-html-head-and-body-tags-automatically-beautifulsoup

    articleBody = ' '.join(map(lambda x: x.text, soup2.find_all('p')))
    
    return soup.title.text, articleBody

################################################################################
# Second function is for TheHindu: returns the article & title_of_article
# Exploiting the property- that it encloses the main body of the article in a <p class="body"></p>;

def TheHindu(url):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)

    # It contains a sub-heading in a div "articleLead"; Let's take care of that
    sub_heading = ''.join(soup.find("div", {"class" : "articleLead"}).text)
    
    articleBody = ' '.join(map(lambda x: x.text, soup.find_all("p", {"class" : "body"})))
    
    article = sub_heading + articleBody
    return soup.title.text, article


# Using the above functions

#url1 = "https://www.washingtonpost.com/politics/on-a-fateful-super-tuesday-polls-have-opened-across-the-south-and-new-england/2016/03/01/995c7ec4-df64-11e5-846c-10191d1fc4ec_story.html?hpid=hp_hp-top-table-main_supertuesdayweb-715am%3Ahomepage%2Fstory"

url2 = "http://www.thehindu.com/business/budget/highlights-of-union-budget-201617/article8295451.ece?homepage=true"

#output = WashingtonPost(url1)    # Returns a list of two items
output = TheHindu(url2)
print "TITLE:", output[0]
print "Article Body:", output[1]