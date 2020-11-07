from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import string
import boto3
def scrap_review(url):
    my_url = url
    
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div",{"class":"apphub_UserReviewCardContent"})
    
    reviews = {}
    text_lst = []
    date_lst = []
    recommend_lst = []
    for container in containers:
        recommend = container.find("div",{"class":'title'}).text
        date_text = container.find("div",{"class":'apphub_CardTextContent'}).text
        date_text = date_text.replace("\t","")
        date_text = date_text.replace("\n","")
        x = date_text.split("\r")
        date = x[0][8:]
        text = x[1]
        text_lst.append(text)
        date_lst.append(date)
        recommend_lst.append(recommend)
    reviews["review"] = text_lst
    reviews["date"] = date_lst
    reviews["recommend"] = recommend_lst
    return(reviews)

def put_reviwew(review):
    DYNAMODB = boto3.resource('dynamodb')
    table = DYNAMODB.Table('Reviews')
    table.put_item(Item=review )

def lambda_handler(event,context):
    reviews_dict = scrap_review("https://steamcommunity.com/app/814380/reviews/?p=1&browsefilter=mostrecent")
    for i in range(len(reviews_dict["review"])):
        temp_dict = {}
        temp_dict["date"] = reviews_dict["date"][i]
        temp_dict["review"] = reviews_dict["review"][i]
        temp_dict["recommend"] = reviews_dict["recommend"][i]
        put_reviwew(temp_dict)
