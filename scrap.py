from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from csv import DictWriter


# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("h1", attrs={"class":'Title--1mf9vro hPTYyn'})
        title_value = title.text.strip()
        return title_value
    except AttributeError:
        return ""
    

#Function to get product keywords 
def get_prodkeywords(soup):
    keywords = ""
    try:
        tech = soup.find_all("a", attrs={"class":"AnchorTag--u22q95 hcBJcI"})
        for line in tech:
            keywords = keywords + ","+line.text
        return keywords
    except AttributeError:
        return ""
    

# Function to extract Product warranty
def get_prodwarranty(soup):
    keywords = ""
    try:
        warranty = soup.find("small", attrs={"class":"SecondaryText--wwg5ji jNlGsQ"})
        # print(warranty)
        return processString(warranty.text).strip()
    except AttributeError:
        return ""
    
    
# Function to extract Process string
def processString(str):
    pr_str = ""
    for c in str:
        if(c!='(' and c!=')'):
            pr_str += c

        
    return pr_str


# Function to extract Product Brand
def get_brand(soup):
    try:
        brand = soup.find("h2", attrs={"class":'Brand--qscqp4 OOcjB'})
        brand_value = brand.text.strip()
        return brand_value
    except AttributeError:
        return ""
    

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'SpecialPriceSpan--1olt47v eowfNn'}).find_all("span")[1]
        act_price = price.text
        return act_price
    except AttributeError:
        return ""

# Function to extract Technical Information
def extract_technical_info(soup):
    technical_info = {}
    try:
        technical_section = soup.find("div", id="technicalID")
        tech_lines = technical_section.find_all("div", class_="TechInfoLine--o1c6fd iayXKH")
        for line in tech_lines:
            key_element = line.find("span", class_="TechInfoKey--d2dhxn cbKQsk")
            value_element = line.find("span", class_="TechInfoVal--1wwve45 dGIuxy")
            key = key_element.text.strip()
            value = value_element.text.strip()
            # print(key," : ",value)
            technical_info[key] = value
    except AttributeError:
        pass
    return technical_info

if __name__ == '__main__':
    # add your user agent 
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}

    # arr = ["eyeglasses","sunglasses","eyeglasses/promotions/all-kids-eyeglasses","eyeglasses/collections/all-computer-glasses"]
    driver = webdriver.Chrome()
    arr = ["eyeglasses","sunglasses"]

    for str in arr :

        # The webpage URL
        URL = "https://www.lenskart.com/" +str+ ".html"

        # HTTP Request
        driver.get(URL)
        # webpage = requests.get(URL, headers=HEADERS)

        # Loading all products
        prev_height = -1
        max_scrolls = 1000
        scroll_count = 0

        while scroll_count < max_scrolls:
            x = 1000+500*(scroll_count)
            driver.execute_script(f"window.scrollTo(0, {x});")
            time.sleep(3)  # give some time for new results to load
            new_height = driver.execute_script(f"return {x}")
            if new_height == prev_height:
                break
            prev_height = new_height
            scroll_count += 1


        # Soup Object containing all data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # print(soup.prettify())
        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={"class":"AnchorWrapper--1smmibb iioefz"})
        # print(links)
        # # Store the links
        links_list = [link.get('href') for link in links]
        
        
        if (len(links_list)) :
            driver.get("https://www.lenskart.com" + links_list[0])

        # Loop for extracting product details from each link 
        for index, link in enumerate(links_list):
            
            data = {"id": '', "title": '',"url": '', "brand": '', "price(in Rupees)": '', "frame_size": '', "frame_width": '',"model_no":'',"productKeys":'',"warranty":''}
            # new_webpage = requests.get("https://www.lenskart.com" + link, headers=HEADERS)
            data['url'] = ("https://www.lenskart.com" + link)
            new_soup = BeautifulSoup(driver.page_source, "html.parser")
            if (index < (len(links_list)-1)) :
                driver.get("https://www.lenskart.com" + links_list[index+1])

            
            # Function calls to display all necessary product information
            data['id'] = (get_id(new_soup))
            data['title'] = (get_title(new_soup))
            data['brand'] = (get_brand(new_soup))
            data['price(in Rupees)'] = (get_price(new_soup))
            data['productKeys'] = (get_prodkeywords(new_soup))
            data['warranty'] = (get_prodwarranty(new_soup))
            
            
            # Extract technical information
            tech_info = extract_technical_info(new_soup)
            data['id'] = (tech_info.get('Product id', ''))
            data['frame_size'] = (tech_info.get('Frame Size', ''))
            data['frame_width'] = (tech_info.get('Frame Width', ''))
            data['model_no'] = (tech_info.get('Model No.', ''))


            field_names = ["id", "title","url", "brand", "price(in Rupees)" , "frame_size", "frame_width", "model_no", "productKeys", "warranty"]
            with open('products.csv', 'a') as f_object:
 
                # Passing the file object and a list
                dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            
                # Passing the dictionary as an argument to the Writerow()
                dictwriter_object.writerow(data)
            
                # Close the file object
                f_object.close()

    # Close the browser window
    driver.quit()
