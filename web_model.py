'''
Use Python Selenium to scrape data from the EPFO website. Make sure to use the Chrome driver.
Make sure to verify your requirements.txt file before submitting your code. You can use Python 3.11>= for this coding challenge.

Fill out the sections where TODO is written.
Ideally your code should work simply by running the web_library.py file.

This is a sample file to get you started. Feel free to add any other functions, classes, etc. as you see fit.
This coding challenge is designed to test your ability to write python code and your familiarity with the Selenium library.
This coding challenge is designed to take 2-4 hours and is representative of the kind of work you will be doing at the company daily.
'''

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
import re
import pandas as pd
from io import BytesIO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image


import cv2

DOWNLOAD_DIR = "/home/t2b/Desktop/Repository/python_dev_coding_challenge/data"

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"


def get_captcha_text(driver):
    captcha_element = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div[2]/form/div[4]/div/div/img")

    # Get the location and size of the captcha image element
    location = captcha_element.location
    size = captcha_element.size

    # Take a screenshot of the captcha image
    captcha_screenshot = driver.get_screenshot_as_png()
    # Crop the screenshot to get only the captcha image
    captcha_image = Image.open(BytesIO(captcha_screenshot)).crop(
        (location['x'], location['y'], location['x'] + size['width'],
         location['y'] + size['height'])
    )

    # Save the captcha image to a file (optional)
    captcha_image.save("captcha.png")

    # Instantiate the processor
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')

    # Instantiate the model
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')

    # Switch model to evaluation mode
    model.eval()

    img = captcha_image.convert('RGB')  # Convert to RGB
    pixel_values = processor(images=img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    captcha_text = re.sub(r'\s', '', generated_text)
    return captcha_text

def scrape_data(company_name: str):
    '''
    Scrape data from the EPFO website
    '''

    # Create Selenium driver
    options = Options()
    # TODO: Add whatever options you might think are helpful
    prefs = {"download.default_directory": os.path.join(os.getcwd(),
                                                        DOWNLOAD_DIR)}  # Set the download directory to the data folder
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    # Open the EPFO website
    driver.get('https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome')

    # Use time library to visualize the browser else tab will close
    time.sleep(5)

    # TODO: Fill out the code for the following steps
    # Step 1
    # Enter the company name in the search box
    try:
        search_box = driver.find_element(By.ID, "estName")
        search_box.send_keys(company_name)
    except NoSuchElementException as e:
        print(f"Error finding search box: {e}")
    time.sleep(2)

    captcha_value = get_captcha_text(driver)
    print("captcha text:", captcha_value)

    # Enter the captcha in the captcha box
    captcha_input = driver.find_element(By.ID, 'captcha')
    captcha_input.send_keys(captcha_value)

    # Click on the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchEmployer"))
    )
    search_button.click()

    # Wait for the search results to load
    time.sleep(2)

    # Step 2
    # Click on the "View Details" button
    view_details_button = driver.find_element(By.LINK_TEXT, "View Details")
    view_details_button.click()

    # Wait for the page to load
    time.sleep(2)

    # Click on the "View Payment Details" button in the new tab
    view_payment_details_button = driver.find_element(By.LINK_TEXT, "View Payment Details")
    view_payment_details_button.click()

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Step 3
    # Click on the "Excel" button to download the Excel file
    excel_button = driver.find_element(By.LINK_TEXT, "Excel")
    excel_button.click()

    # Wait for the download to complete
    time.sleep(5)

    # Close the browser
    driver.quit()

    print("Driver closed successfully...!!!")


def test_scrape_data():
    '''
    Test the scraped data
    '''
    # Convert xlsx file to csv due to some issues with pandas
    from xlsx2csv import Xlsx2csv
    Xlsx2csv("/home/t2b/Desktop/Repository/python_dev_coding_challenge/data/Payment Details.xlsx",
             outputencoding="utf-8").convert("payment_details.csv")

    df = pd.read_csv("payment_details.csv")

    assert set(df.columns) == set(['TRRN', 'Date Of Credit', 'Amount', 'Wage Month', 'No. of Employee', 'ECR'])
    assert df['TRRN'].loc[0] == 3171702000767
    assert df['Date Of Credit'].loc[0] == '03-FEB-2017 14:35:15'
    assert df['Amount'].loc[0] == 334901
    assert df['Wage Month'].loc[0] == 'DEC-16'
    assert df['No. of Employee'].loc[0] == 83
    assert df['ECR'].loc[0] == 'YES'
    print("All tests passed!")


def main():
    print("Hello World!")

    # Uncomment the following line when you are ready to test the scraping function
    scrape_data("MGH LOGISTICS PVT LTD")

    # Uncomment the following tests whenever scraping is completed.
    test_scrape_data()
    # TODO: Feel free to add any edge cases which you might think are helpful


if __name__ == "__main__":
    main()





















