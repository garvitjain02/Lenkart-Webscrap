import pandas as pd
import re
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import staleness_of
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--disable-geolocation")


driver = Chrome(options=chrome_options)

URL = "https://www.lenskart.com/stores/location/rajasthan/kota"
driver.get(URL) 

# all data points list
city = "Kota"
store_names = []
store_addresses = []
store_abouts = []
contacts = []
stars = []
reviews = []
img_urls = []
store_urls = []

timings = []
services = []
products = []
about = []


webpage = requests.get(URL)
mainSoup = BeautifulSoup(webpage.content,'html.parser')

links = mainSoup.find_all("div", attrs={'class': 'StoreCard_imgContainer__P6NMN'})

for link in links:
    # Extract store name
    store_name_element = link.find("a", class_="StoreCard_name__mrTXJ")
    store_name = store_name_element.text.strip()
    store_names.append(store_name)

    # Extract store address
    store_address_element = link.find("a", class_="StoreCard_storeAddress__PfC_v")
    store_address = store_address_element.text.strip()
    store_addresses.append(store_address)

    # Extract store contact
    contacts_element = link.find("div", class_="StoreCard_wrapper__xhJ0A")
    contact = contacts_element.text.strip()
    contacts.append(contact)

    img_tag = link.find('div', class_='StoreCard_imgBox__jTzRs').find('noscript').find('img')
    img_src = img_tag['src']
    img_url = "https://www.lenskart.com" + img_src
    img_urls.append(img_url)

anchors = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.StoreCard_name__mrTXJ"))
)

for anchor in anchors:
    try:
        href = anchor.get_attribute("href")

        store_urls.append(href)
        
        driver.get(href)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Home_activeNav__SJWJq"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract store about
        store_about = soup.find("p", class_="Home_otherInfo__QYiBD").text.strip()
        store_abouts.append(store_about)

        
        try:   
            star = soup.find("div", class_="Home_rating__BaBug").text.strip()
            stars.append(star)
        except:
            stars.append("Not rated")

        try:
            review = soup.find("div", class_="Home_count__Y0nOJ").text.strip()
            no = review[1:-1]
            reviews.append(no)
        except:
            reviews.append("Not reviewed")

        try:
            product_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Home_activeNav__SJWJq"))
                
            )
            product_text = product_element.text.strip()
            if "(" in product_text:
                no_of_product = product_text.split("(", 1)[-1].split(")", 1)[0]
                products.append(no_of_product)
            else:
                products.append("0")
        except :
            print("Timeout occurred while waiting for product information to appear.")
            products.append("0")

        hours_span = soup.find_all("div", class_="Home_infoBox__PV5Wz")[0]
        span = hours_span.find_all("span")[3]
        hours_text = span.get_text(strip=True)
        timings.append(hours_text)

        services_div = soup.find_all("div", class_="Home_infoBox__PV5Wz")[1]
        service_text = services_div.find_all("span")[1]
        service = service_text.get_text(strip=True)
        services.append(service)
        
        driver.back()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Error occurred while extracting information from:", href)

driver.quit()

store_df = pd.DataFrame({"Store Name": store_names, "Address": store_addresses,"Timings":timings,"Services":services,"Image URL":img_urls,"No of Reviews":reviews,"Ratings":stars,"About":store_abouts,"Store URL":store_urls,"No of Products":products,"Store City":city,"Contact":contacts})
csv_file = city + ".csv"
store_df.to_csv(csv_file, index=False)

print("Store details saved for:", city)
