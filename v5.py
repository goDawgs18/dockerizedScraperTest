# from tokenize import Number
import requests
import json
# from urllib import request, parse
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from selenium import webdriver
import time

# fbServerUrl = "http://localhost:6060/"
# listGamePath = "games";
# listBetOfferingPath = "";

options = webdriver.ChromeOptions()
options.headless = True
# options.add_argument("window-size=1920x1080")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')        
driver = webdriver.Chrome(options=options)

baseUrl = "https://sportsbook.draftkings.com"
driver.get(baseUrl)
page_source = driver.page_source
# page = requests.get(baseUrl)
# print(page)
# print(page.content)

soup = BeautifulSoup(page_source, 'html.parser')

leagueLinks = soup.find_all('a', class_='sportsbook-navigation-item-link sportsbook-navigation-item-link--league')
print(leagueLinks[0].get('href'))

# for curr in leagueLinks:
#     print(curr.get("href"))

leagueUrl = baseUrl + leagueLinks[1].get("href")
leagueUrl = 'https://sportsbook.draftkings.com/leagues/baseball/88670847';
print(leagueUrl)
# leaguePage = requests.get(leagueUrl)
driver.get(url=leagueUrl)
page_source = driver.page_source
# time.sleep(1)
soup = BeautifulSoup(page_source, 'html.parser')
gameLinks = soup.find_all('a', class_='event-cell-link')
uniqueGameUrls = set()
for game in gameLinks:
    print(game.get('href'))
    uniqueGameUrls.add(game.get('href'))

for game in uniqueGameUrls: 
    gameUrl = baseUrl + game
    # gameUrl = baseUrl + uniqueGameUrls[2]

    # gamePage = requests.get(gameUrl)

    print(gameUrl)
    # <li class="sportsbook-breadcrumb__end" aria-current="page">&nbsp;/&nbsp;COL Rockies @ ARI Diamondbacks Odds</li>
    driver.get(gameUrl)
    page_source = driver.page_source
    # time.sleep(1)
    soup = BeautifulSoup(page_source, 'html.parser')

    gameTimeDiv = soup.find('div', class_='timer__timer-text')
    # print(str(gameTimeDiv))

    if(str(gameTimeDiv) == 'None'):
        print("skip")
    else:
    # if (gameTimeDiv):
        # print(gameTimeDiv)
        timeStr = gameTimeDiv.findChild('span').get_text()
        # print(timeStr)
        timeObj = datetime
        if (timeStr == '-:-:-'):
            break
        elif (timeStr.find("day") != -1):
            reg = re.compile(r"^(?P<amount>\d)\s*(?P<unit>\w*)$")
            output = reg.search(timeStr)
            timeData = datetime.strptime(output.group('amount'), '%d')
            delta = timedelta(days=timeData.day)
            timeObj = datetime.now() + delta
        elif(re.search(r"^\d{1,2}:\d{1,2}$", timeStr)):
            timeData = datetime.strptime(timeStr, '%M:%S')
            delta = timedelta(hours=timeData.hour, minutes=timeData.minute, seconds=timeData.second)
            timeObj = datetime.now() + delta
        elif(re.search(r"^\d{1,2}:\d{1,2}:\d{1,2}$", timeStr)):
            # ToDo: make this accept %M:%S format as
            timeData = datetime.strptime(timeStr, '%H:%M:%S')
            delta = timedelta(hours=timeData.hour, minutes=timeData.minute, seconds=timeData.second)
            timeObj = datetime.now() + delta
            # timeObj = datetime.strptime(timeStr, '%H:%M:%S') + datetime.now()
        print("time: " + str(timeObj))

        gameName = soup.find('li', class_="sportsbook-breadcrumb__end").getText();
        reg = re.compile(r"^\s*\/\s*(?P<awayTeam>(\w+\s*)+)\s+@\s*(?P<homeTeam>\w+\s*\w*)")
        results = reg.search(gameName)
        if (results):
            print(str(timeObj))
            gameDict = {
                "sport": "mlb",
                "homeTeam": results.group('homeTeam'),
                "awayTeam": results.group('awayTeam'),
                "dateTime": str(timeObj)
            }
            print(gameDict)
            # print("Home team: " + results.group('homeTeam'))
            # print("Away team: " + results.group('awayTeam'))
        else: 
            print(gameName)
            print("failed")

        
        # url = fbServerUrl + listGamePath
        # gameReq = requests.post(url, json=gameDict)
        # print(gameReq.json())
        # gameId = gameReq.json()['message']['_id']

        mainTable = soup.find("tbody")
        trs = mainTable.findChildren("tr")

        # for tr in trs:
        #     print(tr.getText())
        #     reg = re.compile(r"(?P<team>\w+)(\s*[\w\.]+)*(?P<spread>[+-]\d+\.\d+)(?P<spreadOdds>[+-]\d+)(?P<overUnder>[OU]\s*\d+\.?\d*)(?P<overUnderOdds>[+-]\d+)(?P<mlOdds>[+-]\d+)")
        #     x = reg.search(tr.getText())
        #     print(x)
        #     if (x):
        #         print(x.group('team'))
        #         print(x.group('spread'))
        #         print(x.group('spreadOdds'))
        #         print(x.group('overUnder'))
        #         print(x.group('overUnderOdds'))
        #         print(x.group('mlOdds'))

        #         betDict = {
        #             "type": "Game Points",
        #             "odds": int(x.group('overUnderOdds')),
        #             "subject": "game",
        #             "objective": x.group('overUnder'),
        #             "valid": True,
        #             "game": gameId
        #         }
        #         print(betDict)
        #         url = fbServerUrl + "betOffering"
        #         betReq = requests.post(url, json=betDict)
        #         print(betReq.json())

        #         betDict = {
        #             "type": "Moneyline",
        #             "odds": int(x.group('mlOdds')),
        #             "subject": x.group('team'),
        #             "objective": "win",
        #             "valid": True,
        #             "game": gameId
        #         }
        #         url = fbServerUrl + "betOffering"
        #         betReq = requests.post(url, json=betDict)
        #         print(betReq.json())

        #         betDict = {
        #             "type": "Spread",
        #             "odds": int(x.group('spreadOdds')),
        #             "subject": x.group('team'),
        #             "objective": x.group('spread'),
        #             "valid": True,
        #             "game": gameId
        #         }
        #         url = fbServerUrl + "betOffering"
        #         betReq = requests.post(url, json=betDict)
        #         print(betReq.json())

        #     else:
        #         print('regex fail')
        #         print(tr.getText())
        #         break
        #         print()
        #     print("______________________-")
        

print("done")
