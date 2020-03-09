import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
response = requests.get("https://www.zomato.com/bangalore/south-bangalore-restaurants",headers=headers)

content = response.content
soup = BeautifulSoup(content,"html.parser")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page_no = 1
list_restaurants =[]
c=0;

for page in range(0,6):
    print(page_no)
    
    response = requests.get("https://www.zomato.com/bangalore/south-bangalore-restaurants?page={0}".format(page_no), headers=headers)
    content = response.content
    sp = BeautifulSoup(content, "html.parser")
    search_list = sp.find_all("div", {'id': 'orig-search-list'})
    list_ = search_list[0].find_all("div", {'class': 'content'})
    for i in range(0,15):
            c=c + 1
            rest_N = list_[i].find("a", {'data-result-type': 'ResCard_Name'})
            rest_N=rest_N.string.strip()
            area = list_[i].find("b")
            area = area.string.strip()
        
            rating = list_[i].find("div", {'data-variation': 'mini inverted'})
            rating = rating.string.split()[0]
            if rating is None:
                continue
            votes = list_[i].find("span", {'class': re.compile(r'rating-votes-div*')})
            
            if votes is None:
                continue
            rest_T=list_[i].find_all("div", {'class': 'col-s-12'})
            tpe = []
            for x in rest_T:
                tpe=x.find("a", {'class': 'zdark ttupper fontsize6'})
                if tpe is None:
                    continue
                tpe=tpe.string.split()
            
            
            dataframe=[]
            dfObject={
                "restaurant_id": c,
                "name": rest_N,
                "area": area,
                "restaurant_type": tpe,
                "rating": rating,
                "votes": votes.string.split()[0],
            }
            list_restaurants.append(dfObject)
            if c == 80:
                break
        
    page_no+=1
df = pd.DataFrame(list_restaurants)
df.to_csv("zomato_south_banglore.csv", index= False, header=True)

with open('zomato_south_banglore.json','w') as outfile:
    json.dump(list_restaurants, outfile, indent=4)