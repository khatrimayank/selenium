from selenium import webdriver 
from selenium.webdriver.common.by import By 
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd

# chrome_options = Options()

# chrome_options.add_argument("--headless")

url="https://www.cardekho.com/newcars"

# driver=webdriver.Chrome(options=chrome_options)

driver=webdriver.Chrome()

driver.get(url)

driver.maximize_window()

time.sleep(1)

all_brand_links=[]

all_model_links=[]

MAKE_MODEL=[]
Varients=[]
Engine_Type=[]
Engine_Displacement=[]
Transmission_Type=[]
Fuel_Type=[]
Mileage=[]
Tank_Capacity=[]
Front_Suspension=[]
Rear_Suspension=[]
Entertainment_Details=[]

def row_data_to_dict(rows_data):
    row_dict = {}
    for i in range(0, len(rows_data), 2):
        key = rows_data[i]
        value = rows_data[i+1] if i+1 < len(rows_data) else "N/A"
        row_dict[key] = value
    return row_dict



#extract links of all brands
all_brands=driver.find_elements(By.XPATH,'//div[@data-track-section="Current"]//a')

for brand in all_brands:
    
    #link for current brand
    brand_link = brand.get_attribute('href')
    
    all_brand_links.append(brand_link)

    # Open the link in a new tab
    driver.execute_script("window.open('{}', '_blank');".format(brand_link))
    
    time.sleep(1) # Wait for the new tab to open

     # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(1)

    #extract links of all models
    all_models=driver.find_elements(By.XPATH,'//ul[@class="modelList"]//h3//a')

    for model in all_models:

        try:
            make_model=model.text
            MAKE_MODEL.append(model.text)

        except Exception as e:
            MAKE_MODEL.append("N/A")
            make_model="n/a"
        
        #link of current model
        model_link=model.get_attribute('href')

        all_model_links.append(model_link)
        
        #store the handle of current tab
        current_tab = driver.current_window_handle

        #open cuurent model link in new tab
        driver.execute_script("window.open('{}', '_blank');".format(model_link))

        time.sleep(1) # Wait for the new tab to open

        # handle of newly openend tab
        new_tab_handle = driver.window_handles[-1]

        #switch to new tab
        driver.switch_to.window(new_tab_handle)

        time.sleep(1)

        varient_element=WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'table[data-track-component="varianttable"] tbody tr[data-variant]')))
        
        if not varient_element:
            varient_element=[]

        varients=[]

        try:
            for varient in varient_element:
                if varient and len(varient.text)>0:
                    varients.append((varient.text).split("\n")[0])
                else:
                    continue

            Varients.append(varients)

        except Exception as e:
            Varients.append("N/A")

        
        
        retries = 3

        
        count=0
        for _ in range(retries):
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.BottomLinkViewAll > a')))
    
                element.click()
                break  
            except Exception as e:
                print("hii")
                time.sleep(1)
                count+=1

        if count==3:
            Engine_Type.append("N/A")
            Engine_Displacement.append("N/A")
            Transmission_Type.append("N/A")
            Fuel_Type.append("N/A")
            Mileage.append("N/A")
            Tank_Capacity.append("N/A")
            Front_Suspension.append("N/A")
            Rear_Suspension.append("N/A")
            Entertainment_Details.append("N/A")
            continue



        engine_table=[]
        fuel_table=[]
        suspension_table=[]
        enterntainment_table=[]
        varients_table=[]

        for _ in range(3):                                                                 #(By.XPATH,"//*[@id='scrollDiv']//h3[contains(@id, 'Engine')]/following-sibling::table")

            try:
                engine_table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Engine'] + table")))
                break
            except Exception as e:
                print("for model {} engine table cant extracted".format(make_model))
                time.sleep(1)


        for _ in range(3):
            try:
                fuel_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Fuel'] + table")))
                break
            except Exception as e:
                print("for model {} fuel table cant extracted".format(make_model))
                time.sleep(1)
                

        for _ in range(3):
            try:
                suspension_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Suspension'] + table")))
                break
            except Exception as e:
                print("for model {} Suspension table cant extracted".format(make_model))
                time.sleep(1)

        for _ in range(3):
            try:
                enterntainment_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Entertainment'] + table")))
                break
            except Exception as e:
                print("for model {} enterntainment table cant extracted".format(make_model))
                time.sleep(1)



        data_list=[]

        for table in [engine_table,fuel_table,suspension_table,enterntainment_table]:

            if not table:
                continue
            try:
                table_row_data=table.find_elements(By.XPATH,'.//tr//td')

                for row_data in table_row_data:

                    if row_data.text=="Report Incorrect Specs":

                        continue

                    data_list.append(row_data.text)
            except Exception as e:
                pass
                
        data_dict=row_data_to_dict(data_list)
        

        try:
            Engine_Type.append(data_dict.get("Engine Type", data_dict.get("Battery Type", "N/A")))


        except Exception as e:
            Engine_Type.append("N/A")
        
        try:
            Engine_Displacement.append(data_dict.get("Displacement", data_dict.get("Motor Power", "N/A")))

        except Exception as e:
            Engine_Displacement.appen("N/A")

        try:
            Transmission_Type.append(data_dict.get('Transmission Type','N/A'))

        except Exception as e:
            Transmission_Type.append("N/A")

        try:
            Fuel_Type.append(data_dict.get('Fuel Type','N/A'))
            fuel_type=Fuel_Type[-1]

        except Exception as e:
            Fuel_Type.append("N/A")

        try:
            Mileage.append(data_dict.get(str(fuel_type) + ' Mileage ARAI', 
                                                                         data_dict.get(str(fuel_type) + ' Mileage WLTP' , 
                                                                                                                        data_dict.get("Range", "N/A"))))
        except Exception as e: 
            Mileage.append("N/A")

        try:
            Tank_Capacity.append(data_dict.get(str(fuel_type) + ' Fuel Tank Capacity', data_dict.get("Battery Capacity", "N/A")))

        except Exception as e:
            Tank_Capacity.append("N/A")
        

        try:
            Front_Suspension.append(data_dict.get('Front Suspension','N/A'))

        except Exception as e:
            Front_Suspension.append("N/A")

        try:
            Rear_Suspension.append(data_dict.get('Rear Suspension','N/A'))

        except Exception as e:
            Rear_Suspension.append("N/A")

        try:
            keys_to_get = ['Touch Screen size', 'Connectivity', 'Tweeters' , 'Additional Features']
            
            temp={}

            for key in keys_to_get:

                temp[key]=(data_dict.get(key, 'N/A'))

            Entertainment_Details.append(temp)

        except Exception as e:
            Entertainment_Details.append("N/A")

        
        #close the current model tab
        driver.close()

        #switch window handle to curent tab
        driver.switch_to.window(current_tab)

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

print(MAKE_MODEL,Engine_Type,Engine_Displacement,Transmission_Type,Front_Suspension,Rear_Suspension,Fuel_Type,Mileage,Tank_Capacity,Entertainment_Details,Varients)

df=pd.DataFrame({"MAKE_MODEL":MAKE_MODEL,"ENGINE_TYPE/BATTERY_TYPE":Engine_Type,"ENGINE_DISPLACEMENT(CC)/MOTOR_POWER(KW)":Engine_Displacement,"TRANSMISSION_TYPE":Transmission_Type,"FUEL_TYPE":Fuel_Type,"MILEAGE/Range":Mileage,"TANK_CAPACITY/BATTERY_CAPACITY":Tank_Capacity,"FRONT_SUSPENSION":Front_Suspension,"REAR_SUSPENSION":Rear_Suspension,"Entertainment_Details":Entertainment_Details,"VARIENTS":Varients})

df.to_csv("All_CAR_DETAILS_FROM_CAR_DEKHO.csv")


'''   both of which are commonly used in web scraping and automated testing frameworks like 
      Selenium to locate elements on a webpage.


XPath: 
(XML Path Language) is a query language used for selecting nodes from an XML document. 
It can also be used with HTML documents, as HTML is an application of XML. 
XPath expressions can traverse the structure of an XML/HTML document and select nodes based on various criteria.

Select all elements: Selects all elements in the document.
//*

Select elements by tag name: Selects all div elements.
//div

Select elements by ID: Selects the element with the ID "example".
//*[@id='example']

Select elements by class name: Selects all elements with the class contain "highlight".
//*[contains(@class, 'highlight')]

Select elements with specific attribute: Selects all elements with a data-type attribute.
//*[@data-type]

Select elements with specific attribute value: Selects all elements with data-type attribute value of "image".
//*[@data-type='image']

Select elements with specific attribute containing a value: Selects all elements with class attribute containing "button".
//*[contains(@class, 'button')]


Select parent element: Selects the parent of the current element.
//element_name/..

Select child elements: Selects all child div elements of the current element.
//element_name/div

Select ancestor elements: Selects all ancestor div elements of the current element.
//element_name/ancestor::div


Certainly! Below are 30 examples covering various XPath syntax elements, along with explanations:

Node Selection:
Select all elements: Selects all elements in the document.

xpath
Copy code
//*
Select elements by tag name: Selects all div elements.

xpath
Copy code
//div
Select elements by ID: Selects the element with the ID "example".

xpath
Copy code
//*[@id='example']
Select elements by class name: Selects all elements with the class "highlight".

xpath
Copy code
//*[contains(@class, 'highlight')]
Predicates:
Select elements with specific attribute: Selects all elements with a data-type attribute.

xpath
Copy code
//*[@data-type]
Select elements with specific attribute value: Selects all elements with data-type attribute value of "image".

xpath
Copy code
//*[@data-type='image']
Select elements with specific attribute containing a value: Selects all elements with class attribute containing "button".

xpath
Copy code
//*[contains(@class, 'button')]
Axes:
Select parent element: Selects the parent of the current element.

xpath
Copy code
//element_name/..
Select child elements: Selects all child div elements of the current element.

xpath
Copy code
//element_name/div
Select ancestor elements: Selects all ancestor div elements of the current element.

xpath
Copy code
//element_name/ancestor::div
Positional:
Select first element: Selects the first div element.

xpath
Copy code
(//div)[1]
Select last element: Selects the last div element.

xpath
Copy code
(//div)[last()]

Text Content:

Select elements with specific text: Selects all elements containing the text "Example".
//*[text()='Example']

Select elements containing specific text: Selects all elements containing the text "Example" anywhere within their text.
//*[contains(text(), 'Example')]



Certainly! Below are 30 examples covering various XPath syntax elements, along with explanations:

Node Selection:
Select all elements: Selects all elements in the document.

xpath
Copy code
//*
Select elements by tag name: Selects all div elements.

xpath
Copy code
//div
Select elements by ID: Selects the element with the ID "example".

xpath
Copy code
//*[@id='example']
Select elements by class name: Selects all elements with the class "highlight".

xpath
Copy code
//*[contains(@class, 'highlight')]
Predicates:
Select elements with specific attribute: Selects all elements with a data-type attribute.

xpath
Copy code
//*[@data-type]
Select elements with specific attribute value: Selects all elements with data-type attribute value of "image".

xpath
Copy code
//*[@data-type='image']
Select elements with specific attribute containing a value: Selects all elements with class attribute containing "button".

xpath
Copy code
//*[contains(@class, 'button')]
Axes:
Select parent element: Selects the parent of the current element.

xpath
Copy code
//element_name/..
Select child elements: Selects all child div elements of the current element.

xpath
Copy code
//element_name/div
Select ancestor elements: Selects all ancestor div elements of the current element.

xpath
Copy code
//element_name/ancestor::div
Positional:
Select first element: Selects the first div element.

xpath
Copy code
(//div)[1]
Select last element: Selects the last div element.

xpath
Copy code
(//div)[last()]
Text Content:
Select elements with specific text: Selects all elements containing the text "Example".

xpath
Copy code
//*[text()='Example']
Select elements containing specific text: Selects all elements containing the text "Example" anywhere within their text.

xpath
Copy code
//*[contains(text(), 'Example')]
Wildcards:
Select elements with any attribute: Selects all elements with any attribute.

xpath
Copy code
//*[@*]
Select elements with any class: Selects all elements with any class attribute.

xpath
Copy code
//*[contains(@class, '')]

Logical Operators:
Select elements matching multiple conditions: Selects all a elements with the class "highlight" and the attribute data-type containing "link".
//a[contains(@class, 'highlight') and contains(@data-type, 'link')]


Select direct child elements: Selects all direct child div elements of the current element.
//element_name/div

Select descendant elements: Selects all descendant span elements of the current element.
//element_name//span


Wildcards:

Select elements with any attribute: Selects all elements with any attribute.
//*[@*]

Select elements with any class: Selects all elements with any class attribute.
//*[contains(@class, '')]

Logical Operators:

Select elements matching multiple conditions: Selects all a elements with the class "highlight" and the attribute data-type containing "link".
//a[contains(@class, 'highlight') and contains(@data-type, 'link')]


Parent/Child Relationships:
Select direct child elements: Selects all direct child div elements of the current element.
//element_name/div

Select descendant elements: Selects all descendant span elements of the current element.
//element_name//span

Attributes:
Select elements with specific attribute: Selects all input elements with the type attribute.
//input[@type]

Select elements with specific attribute value: Selects all input elements with type attribute value of "text".
//input[@type='text']

Select elements with specific attribute containing a value: Selects all div elements with class attribute containing "container".
//div[contains(@class, 'container')]


Text Content:

Select elements with specific text: Selects all elements containing the text "Example".
//*[text()='Example']

Select elements containing specific text: Selects all elements containing the text "Example" anywhere within their text.
//*[contains(text(), 'Example')]


CSS_SELECTOR:
CSS (Cascading Style Sheets) selectors are patterns used to select elements in an HTML 
document based on their element name, attributes, IDs, classes, and relationships with other elements.


Basic Selectors:

Select all elements:
*

Select elements by tag name:
div

Select elements by class name:
.class_name

Select elements by ID:
#element_id

Attribute Selectors:
---------------------
Select elements with a specific attribute:
[data-type]


Select elements with a specific attribute value:
[data-type="image"]


Select elements with a specific attribute containing a value:
[class*="button"]

Descendant Selectors:
---------------------
Select direct child elements:
parent > child

ex:
div > p mean
selects all <p> elements that are direct children of <div> elements.

Adjacent Sibling Selectors:
---------------------------

Select elements immediately preceded by another element:
h2 + p

Select elements immediately preceded by another element of specific type:
h2 + p.warning


Select elements with specific attribute:
input[type]

Select elements with specific attribute value:
input[type="text"]

Select elements with specific attribute containing a value:
[class*="button"]

Select descendants of an element:
div p

Select direct children of an element:
div > p

Select only direct children:
parent > child

Select elements with specific text:
p:contains('Lorem Ipsum')


Select elements starting with specific text:
p:startsWith('Hello')

Select elements ending with specific text:
p:endsWith('World')



XPath Expression: //*[@id='header']
CSS Equivalent: #header

XPath Expression: //*[contains(@class, 'button') and contains(@class, 'primary')]
CSS Equivalent: .button.primary

XPath Expression: //input[@type='text']
CSS Equivalent: input[type='text']

XPath Expression: //div/p
CSS Equivalent: div > p


//p[@class="container"]===p.container

//p[contains(@class,"container")]===p[class*="container"]



'''

'''
driver.execute_script("window.open('{}', '_blank');".format(brand_link)) :

 is a Python code snippet using Selenium WebDriver. It switches the WebDriver's focus to a new browser window or tab that was opened previously.

Let's break down the code:

driver.window_handles: This is a property of the Selenium WebDriver object that returns a list of all currently open browser windows or tabs. Each window/tab is represented by a unique identifier called a "window handle."

[-1]: This index -1 accesses the last item in the list of window handles, which corresponds to the most recently opened window or tab. This is because when a new window is opened, Selenium adds its handle to the end of the list.

driver.switch_to.window(): This method of the Selenium WebDriver is used to switch the focus of the WebDriver to a different window or tab identified by its handle.

So, when this line of code is executed, it tells the WebDriver to switch its focus to the most recently opened browser window or tab. This is often used in scenarios where a new window or tab is opened as a result of some action (e.g., clicking a link or button), and you need to interact with elements within that new window or tab.
'''











# from selenium import webdriver 
# from selenium.webdriver.common.by import By 
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import ElementClickInterceptedException
# import pandas as pd

# # chrome_options = Options()

# # chrome_options.add_argument("--headless")

# url="https://www.cardekho.com/newcars"

# # driver=webdriver.Chrome(options=chrome_options)

# driver=webdriver.Chrome()

# driver.get(url)

# driver.maximize_window()

# time.sleep(1)

# all_brand_links=[]

# all_model_links=[]

# MAKE_MODEL=[]
# Varients=[]
# Engine_Type=[]
# Engine_Displacement=[]
# Transmission_Type=[]
# Fuel_Type=[]
# Mileage=[]
# Tank_Capacity=[]
# Front_Suspension=[]
# Rear_Suspension=[]
# Entertainment_Details=[]

# def row_data_to_dict(rows_data):
#     row_dict = {}
#     for i in range(0, len(rows_data), 2):
#         key = rows_data[i]
#         value = rows_data[i+1] if i+1 < len(rows_data) else "N/A"
#         row_dict[key] = value
#     return row_dict



# #extract links of all brands
# all_brands=driver.find_elements(By.XPATH,'//div[@data-track-section="Current"]//a')

# for brand in all_brands:
    
#     #link for current brand
#     brand_link = brand.get_attribute('href')
    
#     all_brand_links.append(brand_link)

#     # Open the link in a new tab
#     driver.execute_script("window.open('{}', '_blank');".format(brand_link))
    
#     time.sleep(1) # Wait for the new tab to open

#      # Switch to the newly opened tab
#     driver.switch_to.window(driver.window_handles[-1])

#     time.sleep(1)

#     #extract links of all models
#     all_models=driver.find_elements(By.XPATH,'//ul[@class="modelList"]//h3//a')

#     for model in all_models:

#         try:
#             make_model=model.text
#             MAKE_MODEL.append(model.text)

#         except Exception as e:
#             MAKE_MODEL.append("N/A")
#             make_model="n/a"
        
#         #link of current model
#         model_link=model.get_attribute('href')

#         all_model_links.append(model_link)
        
#         #store the handle of current tab
#         current_tab = driver.current_window_handle

#         #open cuurent model link in new tab
#         driver.execute_script("window.open('{}', '_blank');".format(model_link))

#         time.sleep(1) # Wait for the new tab to open

#         # handle of newly openend tab
#         new_tab_handle = driver.window_handles[-1]

#         #switch to new tab
#         driver.switch_to.window(new_tab_handle)

#         time.sleep(1)

#         varient_element=WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'table[data-track-component="varianttable"] tbody tr[data-variant]')))
        
#         if not varient_element:
#             varient_element=[]

#         varients=[]

#         try:
#             for varient in varient_element:
#                 if varient and len(varient.text)>0:
#                     varients.append((varient.text).split("\n")[0])
#                 else:
#                     continue

#             Varients.append(varients)

#         except Exception as e:
#             Varients.append("N/A")

        
        
#         retries = 3

        
#         count=0
#         for _ in range(retries):
#             try:
#                 element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.BottomLinkViewAll > a')))
    
#                 element.click()
#                 break  
#             except Exception as e:
#                 print("hii")
#                 time.sleep(1)
#                 count+=1

#         if count==3:
#             Engine_Type.append("N/A")
#             Engine_Displacement.append("N/A")
#             Transmission_Type.append("N/A")
#             Fuel_Type.append("N/A")
#             Mileage.append("N/A")
#             Tank_Capacity.append("N/A")
#             Front_Suspension.append("N/A")
#             Rear_Suspension.append("N/A")
#             Entertainment_Details.append("N/A")
#             continue



#         engine_table=[]
#         fuel_table=[]
#         suspension_table=[]
#         enterntainment_table=[]
#         varients_table=[]

#         for _ in range(3):
#             try:
#                 engine_table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Engine'] + table")))
#                 break
#             except Exception as e:
#                 print("for model {} engine table cant extracted".format(make_model))
#                 time.sleep(1)


#         for _ in range(3):
#             try:
#                 fuel_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Fuel'] + table")))
#                 break
#             except Exception as e:
#                 print("for model {} fuel table cant extracted".format(make_model))
#                 time.sleep(1)
                

#         for _ in range(3):
#             try:
#                 suspension_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Suspension'] + table")))
#                 break
#             except Exception as e:
#                 print("for model {} Suspension table cant extracted".format(make_model))
#                 time.sleep(1)

#         for _ in range(3):
#             try:
#                 enterntainment_table=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#scrollDiv > h3[id*='Entertainment'] + table")))
#                 break
#             except Exception as e:
#                 print("for model {} enterntainment table cant extracted".format(make_model))
#                 time.sleep(1)



#         data_list=[]

#         for table in [engine_table,fuel_table,suspension_table,enterntainment_table]:

#             if not table:
#                 continue
#             try:
#                 table_row_data=table.find_elements(By.XPATH,'.//tr//td')

#                 for row_data in table_row_data:

#                     if row_data.text=="Report Incorrect Specs":

#                         continue

#                     data_list.append(row_data.text)
#             except Exception as e:
#                 pass
                
#         data_dict=row_data_to_dict(data_list)
        

#         try:
#             Engine_Type.append(data_dict.get("Engine Type", data_dict.get("Battery Type", "N/A")))


#         except Exception as e:
#             Engine_Type.append("N/A")
        
#         try:
#             Engine_Displacement.append(data_dict.get("Displacement", data_dict.get("Motor Power", "N/A")))

#         except Exception as e:
#             Engine_Displacement.appen("N/A")

#         try:
#             Transmission_Type.append(data_dict.get('Transmission Type','N/A'))

#         except Exception as e:
#             Transmission_Type.append("N/A")

#         try:
#             Fuel_Type.append(data_dict.get('Fuel Type','N/A'))
#             fuel_type=Fuel_Type[-1]

#         except Exception as e:
#             Fuel_Type.append("N/A")

#         try:
#             Mileage.append(data_dict.get(str(fuel_type) + ' Mileage ARAI', data_dict.get("Range", "N/A")))

#         except Exception as e: 
#             Mileage.append("N/A")

#         try:
#             Tank_Capacity.append(data_dict.get(str(fuel_type) + ' Fuel Tank Capacity', data_dict.get("Battery Capacity", "N/A")))

#         except Exception as e:
#             Tank_Capacity.append("N/A")
        

#         try:
#             Front_Suspension.append(data_dict.get('Front Suspension','N/A'))

#         except Exception as e:
#             Front_Suspension.append("N/A")

#         try:
#             Rear_Suspension.append(data_dict.get('Rear Suspension','N/A'))

#         except Exception as e:
#             Rear_Suspension.append("N/A")

#         try:
#             keys_to_get = ['Touch Screen size', 'Connectivity', 'Tweeters' , 'Additional Features']
            
#             temp={}

#             for key in keys_to_get:

#                 temp[key]=(data_dict.get(key, 'N/A'))

#             Entertainment_Details.append(temp)

#         except Exception as e:
#             Entertainment_Details.append("N/A")

        
           


#         #close the current model tab
#         driver.close()

#         #switch window handle to curent tab
#         driver.switch_to.window(current_tab)

#     driver.close()

#     driver.switch_to.window(driver.window_handles[0])

# print(MAKE_MODEL,Engine_Type,Engine_Displacement,Transmission_Type,Front_Suspension,Rear_Suspension,Fuel_Type,Mileage,Tank_Capacity,Entertainment_Details,Varients)

# df=pd.DataFrame({"MAKE_MODEL":MAKE_MODEL,"ENGINE_TYPE/BATTERY_TYPE":Engine_Type,"ENGINE_DISPLACEMENT(CC)/MOTOR_POWER(KW)":Engine_Displacement,"TRANSMISSION_TYPE":Transmission_Type,"FUEL_TYPE":Fuel_Type,"MILEAGE/Range":Mileage,"TANK_CAPACITY/BATTERY_CAPACITY":Tank_Capacity,"FRONT_SUSPENSION":Front_Suspension,"REAR_SUSPENSION":Rear_Suspension,"Entertainment_Details":Entertainment_Details,"VARIENTS":Varients})

# df.to_csv("All_CAR_DETAILS_FROM_CAR_DEKHO.csv")








# '''
# The line driver.execute_script("window.open('{}', '_blank');".format(brand_link)) is a Python code snippet using Selenium WebDriver. It executes a JavaScript command to open a new browser window with a specified URL.

# Let's break down the code:

# driver.execute_script(): This method of the Selenium WebDriver allows you to execute JavaScript code within the context of the current page. You can use it to perform various actions that are not directly supported by Selenium's WebDriver API.

# "window.open('{}', '_blank');": This is the JavaScript code that will be executed. It calls the window.open() function, which is a built-in JavaScript function used to open a new browser window. The first parameter '{}' is a placeholder for the URL you want to open, and '_blank' is the target attribute specifying that the URL should open in a new window or tab. The placeholder {} will be replaced with the URL provided in the format() method.

# .format(brand_link): This Python string method replaces the {} placeholder in the JavaScript code with the URL stored in the brand_link variable. The brand_link variable presumably contains the URL of the webpage you want to open in the new window.

# So, when this line of code is executed, it essentially tells the browser to open a new window/tab with the URL stored in the brand_link variable. This can be useful when you need to interact with multiple webpages simultaneously during your automation script execution.
# '''

# '''
# The line driver.switch_to.window(driver.window_handles[-1]) is a Python code snippet using Selenium WebDriver. It switches the WebDriver's focus to a new browser window or tab that was opened previously.

# Let's break down the code:

# driver.window_handles: This is a property of the Selenium WebDriver object that returns a list of all currently open browser windows or tabs. Each window/tab is represented by a unique identifier called a "window handle."

# [-1]: This index -1 accesses the last item in the list of window handles, which corresponds to the most recently opened window or tab. This is because when a new window is opened, Selenium adds its handle to the end of the list.

# driver.switch_to.window(): This method of the Selenium WebDriver is used to switch the focus of the WebDriver to a different window or tab identified by its handle.

# So, when this line of code is executed, it tells the WebDriver to switch its focus to the most recently opened browser window or tab. This is often used in scenarios where a new window or tab is opened as a result of some action (e.g., clicking a link or button), and you need to interact with elements within that new window or tab.
# '''


