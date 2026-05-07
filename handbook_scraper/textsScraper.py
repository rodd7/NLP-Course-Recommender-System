import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import re
import warnings
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

timetable_url = "https://mytimetablecloud.uts.edu.au/even/timetable/#subjects"

file_path = '2025_UTS_Handbook_Data_subjectTexts_only.xlsx'
data = pd.read_excel(file_path)


for index, row in data.iterrows():
    courseID = str(row['courseID'])
    courseLink = row['courseLink']

    courseReferences = []
    courseOtherResources = []
    courseRecommendedTexts = []

    driver = requests.get(courseLink)
    soup = BeautifulSoup(driver.content, 'html5lib')

    courseRawText = ILLEGAL_CHARACTERS_RE.sub("", str(soup))

    h3Reference = soup.find('h3', string='References')
    if h3Reference:
        for sibling in h3Reference.find_next_siblings():
            if sibling.name == 'h3':  # Stop if another <h3> is found
                break
            courseReferences.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
        courseReferences = ' '.join(courseReferences).strip()
    else:
        courseReferences = 'unknown'

    h3OtherResource = soup.find('h3', string='Other resources')
    if h3OtherResource:
        for sibling in h3OtherResource.find_next_siblings():
            if sibling.name == 'h3':  # Stop if another <h3> is found
                break
            courseOtherResources.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
        courseOtherResources = ' '.join(courseOtherResources).strip()
    else:
        courseOtherResources = 'unknown'

    h3RecommendedTexts = soup.find('h3', string='Recommended texts')
    if h3RecommendedTexts:
        for sibling in h3RecommendedTexts.find_next_siblings():
            if sibling.name == 'h3':  # Stop if another <h3> is found
                break
            courseRecommendedTexts.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
        courseRecommendedTexts = ' '.join(courseRecommendedTexts).strip()
    else:
        courseRecommendedTexts = 'unknown'

    print(courseID)
    print(courseReferences)
    print(courseOtherResources)
    print(courseRecommendedTexts)
    df = pd.read_excel(file_path)

    empty_row_index = df['courseReferences'].isnull().idxmax()
    df.at[empty_row_index, 'courseReferences'] = str(courseReferences)
    df.to_excel(file_path, index=False)

    empty_row_index = df['courseOtherResources'].isnull().idxmax()
    df.at[empty_row_index, 'courseOtherResources'] = str(courseOtherResources)
    df.to_excel(file_path, index=False)

    empty_row_index = df['courseRecommendedTexts'].isnull().idxmax()
    df.at[empty_row_index, 'courseRecommendedTexts'] = str(courseRecommendedTexts)
    df.to_excel(file_path, index=False)
    