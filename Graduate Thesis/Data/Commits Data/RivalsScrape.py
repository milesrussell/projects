import json
import pandas as pd

from bs4 import BeautifulSoup

import requests

def retrieve_and_convert_data(school, year):
    r  = requests.get("https://{}.rivals.com/commitments/football/{}".format(school, year))

    soup = BeautifulSoup(r.text)

    json_data = json.loads(soup.find_all('rv-commitments')[0]['prospects'])

    converted_data = pd.DataFrame.from_dict(json_data, orient='columns')
    converted_data['team'] = school
    return converted_data


# no recruiting data for Air Force, Akron, Ball State, Bowling Green, Buffalo, Eastern Michigan, Georgia Southern,
# Georgia State, Hawaii, Idaho, Louisiana-Lafayette, Louisiana-Monroe, Massachusetts, Miami (OH), Navy, NIU, Ohio,
# Old Dominion, San Jose State, South Alabama, Utah State

#pwi is Penn State, uga is Georgia, tamu is Texas A&M, wku is Western Kentucky
teams = ['alabama','appalachianstate','arizona','arizonastate','arkansas','arkansasstate','army','auburn','baylor',
         'boisestate','bostoncollege','byu','cal','centralmichigan','cincinnati','clemson','colorado','coloradostate',
         'connecticut','duke','eastcarolina','florida','fau','fiu','floridastate','fresnostate','uga','georgiatech',
         'houston','illinois','indiana','iowa','iowastate','kansas','kansasstate','kentstate','kentucky','lsu','latech',
         'louisville','marshall','maryland','memphis','miami','michigan','michiganstate','middletennessee','minnesota',
         'olemiss','mississippistate','missouri','nebraska','nevada','unlv','newmexico','newmexicostate','northcarolina',
         'ncstate','northtexas','northwestern','notredame','ohiostate','oklahoma','oklahomastate','oregon','oregonstate',
         'bwi','pittsburgh','purdue','rice','rutgers','sandiegostate','southcarolina','usf','usc','ucla','ucf','smu',
         'southernmiss','stanford','syracuse','temple','tennessee','texas','tamu','tcu','texasstate','texastech',
         'utep','utsa','toledo','troy','tulane','tulsa','utah','vanderbilt','virginia','virginiatech','wakeforest',
         'washington','washingtonstate','westvirginia','wku','westernmichigan','wisconsin','wyoming']

years = ['2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']

data_final = []
FinalData = pd.DataFrame()

for i in teams:
    for j in years:
        data = retrieve_and_convert_data(i,j)
        data_final.append(data)

FinalData = pd.concat(data_final)

FinalData.to_csv('commits.csv')
