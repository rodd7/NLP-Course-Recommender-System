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

recommended_url = "https://www.handbook.uts.edu.au/directory/courses1.html"

file_path = 'recommendedCourses.xlsx'
    
degreeID = ''
degreeName = ''
courseID = ''
courseYear = ''

driver = webdriver.Chrome()
driver.get(recommended_url)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html5lib')


ie = soup.find('div', class_='ie-images')
if ie:
    links = ie.find_all('a', href=True)
    for link in links:
        title = str(link.next_sibling).strip()
        
        bad_list = {"doctor", "master", "graduate"}

        if all(word not in title.lower() for word in bad_list):
            if "https" in str(link['href']):
                driver.get(str(link['href']))

                

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html5lib')

                strong_elements = soup.find_all('strong')
                for strong in strong_elements:
                    if "year" in strong.get_text().lower():
                        courseYear = strong.get_text()
                        for sibling in strong.find_all_next():
                            if sibling.name == 'strong' or sibling.name == 'h2':
                                break

                            if sibling.name == 'a':
                                degreeName = str(title).strip()
                                degreeID = str(link.get_text().strip())
                                courseID = sibling.text.strip()

                                print(degreeID)
                                print(degreeName)
                                print(courseID)
                                print(courseYear)
                                
                                df = pd.read_excel(file_path)

                                empty_row_index = df.shape[0]
                                df.at[empty_row_index, 'degreeID'] = degreeID
                                df.at[empty_row_index, 'degreeName'] = degreeName
                                df.at[empty_row_index, 'courseID'] = courseID
                                df.at[empty_row_index, 'courseYear'] = courseYear
                                df.to_excel(file_path, index=False)

              

                #search for strong with year in it and loop through every piece of text until another strong year or a h2

                driver.back()

            


        # driver.get(link['href'])
        # driver.back()
        
        # driver.get(url)
        # if title and "doctor" or "master" or "graduate" not in title.lower():
        #     print("h")