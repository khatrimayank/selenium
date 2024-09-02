Car Details Extraction from CarDekho.com
Overview
This script extracts detailed car information from CarDekho.com, focusing on various attributes of car models including engine type, displacement, transmission type, fuel type, mileage, tank capacity, suspension details, and entertainment features. The extracted data is saved to a CSV file for further analysis.

Requirements
Python 3.x
Selenium
ChromeDriver
pandas
Setup
Install Required Packages:

You need to install the required Python packages if you haven’t already. You can install them using pip:

pip install selenium pandas
Download ChromeDriver:

Download the appropriate version of ChromeDriver for your Chrome browser from ChromeDriver Downloads and ensure it is accessible from your system's PATH.

Script Overview
Key Components
Imports:

selenium.webdriver: For browser automation.
time: For adding delays.
pandas: For handling data and exporting to CSV.
webdriver.support.ui and webdriver.support.expected_conditions: For waiting for elements to load.
Setup WebDriver:

Initializes the Chrome WebDriver and opens CarDekho.com.

Data Extraction:

Brand Links Extraction: Finds and collects links to different car brands.
Model Links Extraction: For each brand, extracts links to individual car models.
Car Model Details Extraction: For each car model, extracts specific details from various sections of the page.
Data Parsing:

Uses the row_data_to_dict function to convert table rows into a dictionary format.

Data Storage:

Saves the extracted data into a CSV file named CAR_DETAILS_FROM_CAR_DEKHO.csv.

How to Run
Ensure you have Python 3.x installed on your system.

Install the required packages and download ChromeDriver as mentioned in the setup section.

Save the script to a file, e.g., car_data_extraction.py.

Run the script using:


python car_data_extraction.py
Script Details
Chrome Options
chrome_options.add_argument("--headless"): Optional, runs Chrome in headless mode. Uncomment to enable.
Data Collection Process
Extract Links of All Brands:

The script finds links to brands and opens each in a new tab.

Extract Links of All Models:

For each brand, it collects model links and opens each in a new tab.

Extract Detailed Information for Each Model:

Extracts various details from the model pages, including engine type, displacement, fuel type, etc.

Handle Multiple Tables:

Uses CSS selectors to locate and extract data from tables related to engine specifications, fuel details, suspension, and entertainment features.

Store Data:

Saves the collected data to a CSV file for further analysis.

Troubleshooting
Ensure ChromeDriver is compatible with your version of Chrome.
Check your network connection if the script fails to load pages.
Increase time.sleep duration if elements are not loading properly.
