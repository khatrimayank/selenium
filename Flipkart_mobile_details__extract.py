import requests

from bs4 import BeautifulSoup

import pandas as pd

Names=[]

Prices=[]

Reviews=[]

Descriptions=[]


for i in range(1,12):

    url="https://www.flipkart.com/search?q=mobile+under+50000&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_19_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_19_na_na_na&as-pos=3&as-type=RECENT&suggestionId=mobile+under+50000&requestId=4c4dd914-309e-4d51-875e-cea121e60e14&as-searchtext=mobile+under+50000&page="+str(i)
    
    response=requests.get(url)

    raw_html=response.content

    soup=BeautifulSoup(raw_html,'html.parser')

    box=soup.find('div',class_="_1YokD2 _3Mn1Gg")

    #base_link="https://www.flipkart.com/"

    #next_page_link=base_link + soup.find('a',class_="ge-49M _2Kfbh8").get("href")

    #print(next_page_link)

    names=box.find_all('div',class_="_4rR01T")

    for name in names:

        Names.append(name.text)



    prices=box.find_all('div' , class_="_30jeq3 _1_WHN1")

    for price in prices:
        Prices.append(price.text)



    descriptions=box.find_all('ul',class_="_1xgFaf")

    for des in descriptions:

        Descriptions.append(des.text)



    reviews=box.find_all('div' , class_="_3LWZlK")

    for review in reviews:
        Reviews.append(review.text)


#print(Names),print(len(Names))

# print(Prices),print(len(Prices))

# print(Descriptions),print(len(Descriptions))

# print(Reviews),print(len(Reviews))

df=pd.DataFrame({"Names" : Names , "Prices ": Prices , "Descriptions": Descriptions , "Reviews:": Reviews})

print(df)

df.to_csv("Flipkart Mobiles Under 50k.csv")

































"""
#string
#stripped_string
#children
#childrens
#parent
#parents
#next_sibling
#previous_sibling

import requests

from bs4 import BeautifulSoup

url="https://codewithharry.com"

r=requests.get(url)

html_content=r.content #raw html content

#print(r.status_code)

soup=BeautifulSoup(html_content,'html.parser')

#print(soup.prettify)

title=soup.title

#print(title)
#print(title.text)

# find all paras
all_paras=soup.find_all('p')

#find first para
first_para=soup.find('p')

print(first_para)

#print(first_para['class'])

#print(first_para.get_text())

#print(soup.get_text())

all_anchors=soup.find_all('a')

for link in all_anchors:

    if link.get('href')!="#":

        link_text= "https://codewithharry.com" + link.get("href")

        #print(link_text)


print(soup.p)
"""