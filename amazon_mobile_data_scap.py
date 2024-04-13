#https://www.youtube.com/watch?v=FXVjDTimQAg&t=479s

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


'''webdriver - software component or library that is used to automate interactions with web browsers.

selenium.webdriver.common.by - provides a set of locator strategies to find and interact with web elements on a web page.

sleep - used to introduce a delay or pause in the execution of a program or script. '''

browser = webdriver.Chrome()

'''Chrome() is a constructor for creating a WebDriver instance that controls the Google Chrome browser. When you call webdriver.Chrome(), it initializes a new Chrome browser window or tab that can be controlled programmatically using Selenium.'''

browser.get('https://www.amazon.in')

browser.maximize_window()

input_search = browser.find_element(By.ID, 'twotabsearchtextbox')
search_button = browser.find_element(By.XPATH, "(//input[@type='submit'])[1]")

input_search.send_keys("Smartphones under 10000")
sleep(1)
search_button.click()


products = []
for i in range(10):
    print('Scraping page', i+1)
    product = browser.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    for p in product:
        products.append(p.text)
    next_button = browser.find_element(By.XPATH, "//a[text()='Next']")
    next_button.click()
    sleep(2)

print(len(products))

print(products[:5])

