from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

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

    # The webpage URL
    URL = "https://www.lenskart.com/eyeglasses.html"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    # print(soup.prettify())
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={"class":"AnchorWrapper--1smmibb dSYMGn"})
    # print(links)
    # # Store the links
    links_list = [link.get('href') for link in links]
    
    

    data = {"title": [],"url":[], "brand": [], "price(in Rupees)": [] , "frame_size": [], "frame_width": [],"model_no":[],"productKeys":[],"warranty":[]}

    # # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.lenskart.com" + link, headers=HEADERS)
        data['url'].append("https://www.lenskart.com" + link)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        data['title'].append(get_title(new_soup))
        data['brand'].append(get_brand(new_soup))
        data['price(in Rupees)'].append(get_price(new_soup))
        data['productKeys'].append(get_prodkeywords(new_soup))
        data['warranty'].append(get_prodwarranty(new_soup))
        # data['productId'].append(get_prodid(new_soup))
        
        # data['product_id'].append(get_prodid(new_soup))
        
        
        # Extract technical information
        tech_info = extract_technical_info(new_soup)
        data['frame_size'].append(tech_info.get('Frame Size', ''))
        data['frame_width'].append(tech_info.get('Frame Width', ''))
        data['model_no'].append(tech_info.get('Model No.', ''))

    # # Create DataFrame from the dictionary
    lenskart_df = pd.DataFrame(data)

    # Remove rows with missing title
    lenskart_df.dropna(subset=['title'], inplace=True)

    # Save DataFrame to CSV
    lenskart_df.to_csv("product_data.csv", header=True, index=False)
