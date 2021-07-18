from selenium import webdriver
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

driver = webdriver.Chrome()

eventName = []
eventDate = []
eventOrganizer = []
url = []


driver.get("https://www.townscript.com/in/online/must-visit?page=44")

content = driver.page_source
htmlPage = soup(content)
eventUrl = htmlPage.findAll("div", {"class": "ls-card"})


for a in eventUrl:
    url.append("https://www.townscript.com" + a.a["href"])

print(url)
for u in url:
    driver.get(u)
    eventDetails = driver.page_source
    pageSoup = soup(eventDetails)
    if(pageSoup.findAll("div", {"class": "error-page-content"})):
        continue
    else:
        event_name = pageSoup.find("div", {"class": "event-name"}).h1.text
        event_date = pageSoup.find("div", {"class": "other-info"}).span.text
        event_organizer = pageSoup.find(
            "div", {"class": "organizer-info"}).span.text
        eventName.append(event_name)
        eventDate.append(event_date)
        eventOrganizer.append(event_organizer)

df = pd.DataFrame({'Event_Name': eventName,
                  'Event_Date': eventDate, 'Event_Organizer': eventOrganizer})
df.to_csv('townscriptEvents-6.csv', index=False, encoding='utf-8')
