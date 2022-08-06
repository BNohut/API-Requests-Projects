from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# --------------- MAKING SOUP
URL = "https://www.zillow.com/san-francisco-ca/rent-houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56825534228516%2C%22east%22%3A-122.29840365771484%2C%22south%22%3A37.69668892292082%2C%22north%22%3A37.85381150365382%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}
response = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# --------------- CREATE LISTS
addresses = soup.find_all(name="address", class_="list-card-addr")
address_list = [address.getText() for address in addresses]

prices = soup.find_all(name="div", class_="list-card-price")
prices_list = [price.getText().split("/")[0] for price in prices]

links = soup.find_all(name="a", class_="list-card-img")
links_list = [link["href"] for link in links]

# ---------------- ADD SHEETS TO GOOGLE USING BY SELENIUM

chrome_path = "C:/Users/bugra/PycharmProjects/chromedriver.exe"
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(executable_path=chrome_path))

driver.get(url="https://docs.google.com/forms/d/e/1FAIpQLSciCJ-x9C0oPOziVPbu_9rdbKbtmkm52O9pmN_WroLxbDyYGw/viewform?usp=sf_link")
sleep(5)
first = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
first.send_keys(f"{address_list[0]}")
