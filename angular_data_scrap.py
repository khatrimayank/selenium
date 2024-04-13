from selenium import webdriver 
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options
 
# instantiate options 
chrome_options = Options()

chrome_options.add_argument("--headless")

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=chrome_options)
 
# load website 
url = 'https://angular.io/' 
 
# get the entire website content 
driver.get(url) 
 
# select elements by class name 
elements = driver.find_elements(By.CLASS_NAME, 'text-container') 

for title in elements: 
    # select H2s, within element, by tag name 
    heading = title.find_element(By.TAG_NAME, 'h2').text 
    # print H2s 
    print(heading)