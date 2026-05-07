import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import pandas as pd
import re
import time
from openpyxl import load_workbook

timetable_url = "https://mytimetablecloud.uts.edu.au/even/timetable/#subjects"

file_path = '2025_UTS_Handbook_Data.xlsx' # temp fie name
data = pd.read_excel(file_path)



start_scraping = False # temporary fix to adjust for crash, remove this and references if needed

for index, row in data.iterrows():
    courseID = str(row['courseID'])

    if courseID == "42001":
        start_scraping = True
    
    if start_scraping:
        driver = webdriver.Chrome()
        driver.get(timetable_url)

        

        input_field = driver.find_element("id", 'search_box')
        input_field.send_keys(courseID)

        submit_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.desktop-only')
        submit_button.click()

        time.sleep(1)

        try:
            driver.find_element(By.XPATH, "//strong[text()='No subject found']")

            df = pd.read_excel(file_path)
            column_title = 'courseAvailability'

            courseAvailability = ['N/A']
            empty_row_index = df[column_title].isnull().idxmax()
            data_as_string = '\n'.join(['; '.join(inner_array) for inner_array in courseAvailability])
            df.at[empty_row_index, column_title] = data_as_string
            df.to_excel(file_path, index=False)

        except:
            time.sleep(1)
            select_all_button = driver.find_element(By.ID, 'select-all')
            select_all_button.click()
            show_timetable_button = driver.find_element(By.ID, 'toggle-right-col-btn')
            show_timetable_button.click()

            show_as_list_button = driver.find_element(By.CLASS_NAME, 'flat-btn')
            driver.execute_script("arguments[0].click();", show_as_list_button) #JavaScript Executor will click - works


            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html5lib')

            table = driver.find_element(By.CLASS_NAME, "aplus-table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # tableSubjectCode = []
            # tableGroup = []
            # tableActivity = []
            # tableDay = []
            # tableTime = []
            # tableCampus = []
            # tableLocation = []
            # tableDuration = []
            # tableDates = []

            courseAvailability = []

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    courseClass = []
                    for cell in cells:
                        courseClass.append(cell.text)
                    
                    courseAvailability.append(courseClass)

            df = pd.read_excel(file_path)
            column_title = 'courseAvailability'

            empty_row_index = df[column_title].isnull().idxmax()

            data_as_string = '\n'.join(['; '.join(inner_array) for inner_array in courseAvailability])
            df.at[empty_row_index, column_title] = data_as_string
            df.to_excel(file_path, index=False)

        print(courseID)
        print(courseAvailability)

        # open file_path using pd
        #find the title "courseAvailability"
        #find the current column index under the row which its empty
        #write the array TEXT as string type into that empty column index
        #save

        

        driver.quit()