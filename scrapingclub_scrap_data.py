from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
import time 
 
chrome_options = Options()

chrome_options.add_argument("--headless")

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=chrome_options)
 
# load target website 
url = 'https://scrapingclub.com/exercise/list_infinite_scroll/' 
 
# get website content 
driver.get(url) 
 
# instantiate items 
items = [] 
 
# instantiate height of webpage 
last_height = driver.execute_script('return document.body.scrollHeight') 
 
# set target count 
itemTargetCount = 10
 
# scroll to bottom of webpage 
while itemTargetCount > len(items): 
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
 
    # wait for content to load 
    time.sleep(1) 
 
    new_height = driver.execute_script('return document.body.scrollHeight') 
 
    if new_height == last_height: 
        break 
 
    last_height = new_height 
 
    # select elements by XPath 
    elements = driver.find_elements(By.XPATH, "//div/h4/a") 
    h4_texts = [element.text for element in elements] 
 
    items.extend(h4_texts) 
 
    # print title 
    print(h4_texts)