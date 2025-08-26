from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Open browser and load category page
s = Service('C:/webdriver/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get("https://www.limeroad.com/men-clothing/top-wear/casual-shirts?classification%5B%5D=.0.11201585.11201684.11201586.11202215.11201587&stock%5B%5D=1&color%5B%5D=navy%20blue&color%5B%5D=multi")
time.sleep(180)  # Wait for page to load

product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.prdC.bgF.br4.fs12.fg2t.dIb.vT.pR.taC.bs.bd2E.m6')
product_urls = []
product_titles = []
product_brand = []
product_discount = []
product_original = []
product_rating = []
Category = "Men's Casual Shirts"


for card in product_cards[:310]:          
    link = card.find_element(By.TAG_NAME, "a")
    href = link.get_attribute("href")
    product_urls.append(href)

print(len(product_urls))

for url in product_urls:
    driver.get(url)
    time.sleep(5)  # Wait for product page to load
    try:
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        title = ""
    product_titles.append(title)
    
    try:
        brand = driver.find_element(By.CSS_SELECTOR, "a.fs13.c6.eli.pt0.taL.tdN.ttC.hcP").text.strip().replace("Brand","").replace(":","")
    except:
        brand = ""
    product_brand.append(brand)

    try:
        discounted_price = driver.find_element(By.CSS_SELECTOR, "span.sell").text.strip()
    except:
        discounted_price = ""
    product_discount.append(discounted_price)

    try:
        original_price = driver.find_element(By.CSS_SELECTOR, "span.mrp").text.strip().replace("₹","")
    except:
        original_price = ""
    product_original.append(original_price)

    try:
        rating = driver.find_element(By.CSS_SELECTOR, "div.dTc.vM.fs20.c0").text.strip()
    except:
        rating = ""
    product_rating.append(rating)
    

print("Product title:", len(product_titles))
print("Brand:", len(product_brand))
print("Discounted price:", len(product_discount))
print("Original price:", len(product_original))
print("Rating:", len(product_rating))
print("Product URLs:", len(product_urls))
# Close the browser
driver.quit()

# Create a DataFrame and save to CSV
df = pd.DataFrame ({
    'Product Name': product_titles,
    'Brand': product_brand,
    'Category': Category,
    'MRP': product_original,
    'Discounted Price': product_discount,
    'Rating': product_rating,
    'Product URL': product_urls})
print(df)

df.to_csv('limeroad_casualshirts.csv', index=True)

# DATA CLEANING

import pandas as pd
import numpy as np

data = pd.read_csv('limeroad_casualshirts.csv')
print(data.head())
pd.set_option('display.max_columns', None)
data["Brand"] = data["Brand"].str.title() # Capitalize brand names
data.drop('Unnamed: 0',inplace=True,axis=1)

print(data["MRP"].dtype)
print(data["Discounted Price"].dtype)
print(data.tail())

 # filling null values in MRP column with Discounted Price values because mrp and discounted price are same for some products
data["MRP"] = data["MRP"].fillna(data["Discounted Price"])
data["MRP"] = data["MRP"].astype("int64")

# Count total duplicate rows
print(data[data.duplicated()])
# Save to a new CSV file
data.to_csv("limeroad_men_casualshirts.csv", index=False)



