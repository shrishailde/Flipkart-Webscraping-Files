# main program to create headphones dataset by
# scraping the flipkart.com website.

# import the necessary libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import sqlalchemy

# Create the empty lists to store the extracted attributes
title_list = []
color_list = []
type_list = []
rating_list = []
num_of_ratings_list = []
curr_price_list = []
mrp_list = []

# Set number of pages to be scraped
num_of_pages = 55

# For each page the website url must be updated so for that matter we will save
# base url in one variable and create custom url for each page using logic
base_url = "https://www.flipkart.com/search?q=headphones&sid=0pm%2Cfcn&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=headphones%7CHeadphones&requestId=4f0a773b-0c3f-4d39-a229-90a1b66546bc&as-searchtext=headpho&page="
for i in range(1, num_of_pages+1):
    print("***************************************")
    print("Processing Page No-{}".format(i))
    print("***************************************")
    web_url = base_url+str(i)
    # Make a http request to above website variable using requests package
    response = requests.get(web_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # title
    a_tags = soup.find_all("a", {"class": "s1Q9rs"})
    # color and type
    ct_tags = soup.find_all("div", {'class': '_3Djpdu'})
    # rating
    rating_tags = soup.find_all("div", {'class': '_3LWZlK'})
    rating_tags = rating_tags[:40]
    # Number of ratings
    nrating_tags = soup.find_all("span", {'class': '_2_R_DZ'})
    nrating_tags = nrating_tags[:40]
    # Current price
    cp_tags = soup.find_all('div', {'class': '_30jeq3'})
    cp_tags = cp_tags[:40]
    # MRP tags
    mrp_tags = soup.find_all('div', {'class': '_3I9_wc'})

    # extract each item value for above attributes and store them
    # in respective lists
    for j in range(40):
        try:
            # title
            title_list.append(a_tags[j].get_text())
        except:
            title_list.append('NA')
        # color and type
        try:
            color_list.append(ct_tags[j].get_text().split(',')[0])
        except:
            color_list.append('NA')
        try:
            type_list.append(ct_tags[j].get_text().split(',')[1])
        except:
            type_list.append('NA')
        try:
            # rating
            rating_list.append(float(rating_tags[j].get_text()))
        except:
            rating_list.append(0)
        try:
            # Number of ratings
            num_of_ratings_list.append(
                int(nrating_tags[j].get_text()[1:-1].replace(',', '')))
        except:
            num_of_ratings_list.append(0)
        try:
            # Current Selling price
            curr_price_list.append(
                float(cp_tags[j].get_text()[1:].replace(',', '')))
        except:
            curr_price_list.append(0)
        try:
            # MRP
            mrp_list.append(float(mrp_tags[j].get_text()[1:].replace(',', '')))
        except:
            mrp_list.append(0)

df = pd.DataFrame(list(zip(title_list, color_list, type_list, rating_list, num_of_ratings_list, curr_price_list, mrp_list)),
                  columns=['title', 'color', 'type', 'avg_rating', 'num_of_ratings', 'curr_price', 'MRP'])
print(df.head())
df.to_excel('fk_headphones.xlsx', index=False)

# Store the dataframe into PostgreSQL
engine = sqlalchemy.create_engine(
    'postgresql://postgres:shri5@localhost:5432/misc')
df.to_sql('fk_headphones', engine, index=False)
