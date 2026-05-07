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

file_path = '2025_UTS_Handbook_Data.xlsx'
data = pd.read_excel(file_path)

start_scraping = False # temporary fix to adjust for crash, remove this and references if needed

for index, row in data.iterrows():
    courseID = str(row['courseID'])

    if courseID == "10024":
        start_scraping = True

    if start_scraping:

        # course interface
        courseID = None
        courseTitle = None
        courseCreditPoints = 0
        courseOrganisationalName = 'unknown'
        courseLevel = "Undergraduate" # courses usually say its postgraduate, otherwise assumed it's always UG
        courseAvailability = 'unknown'
        courseRequisite = 'unknown'
        courseResultType = 'unknown'
        courseRecommendedYear = 0
        courseDescription = []
        courseSLO = []
        courseCILO = []
        courseStrategy = []
        courseContent = []
        courseAssessment = []
        courseMinRequirements = []
        courseRequiredTexts = []
        courseReferences = []
        courseOtherResources = []
        courseRawText = 'unknown'

        courseLink = row['courseLink']  # Change 'Link' to your actual column name
        print(courseLink)

        driver = webdriver.Chrome()
        driver.get(courseLink)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html5lib')

        courseRawText = ILLEGAL_CHARACTERS_RE.sub("", str(soup))

        # h1_title = soup.h1.get_text(strip=True).split(' ', 1) # got these already
        # courseID = h1_title[0]
        # courseTitle = h1_title[1]

        courseOrganisationalName = soup.find('em', string=lambda text: "UTS:" in text)
        if courseOrganisationalName:
            courseOrganisationalName = courseOrganisationalName.get_text()
        else:
            courseOrganisationalName = 'unknown'

        cp = soup.find(string=lambda text: text and "cp" in text)
        if cp:
            courseCreditPoints = re.search(r'\d+', str(cp)).group()
        else:
            courseCreditPoints = 0

        level = soup.find(string=lambda text: text and "Postgraduate" in text)
        if level:
            courseLevel = "Postgraduate"
        else:
            courseLevel = 'Undergraduate'

        result = soup.find('em', string=lambda text: text is not None and "Result type" in text)
        if result:
            courseResultType = re.sub(r':', '', result.next_sibling.get_text()).strip()
        else:
            courseResultType = "unknown"

        # courseRequisite = soup.find_all('em')
        # for em in courseRequisite:
        #     if 'requisite(s)' in em.get_text().lower():
        #         courseRequisite = em.get_text()

        h3Description = soup.find('h3', string='Description')
        if h3Description:
            for sibling in h3Description.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseDescription.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseDescription = ' '.join(courseDescription).strip()
        else:
            courseDescription = 'unknown'

        h3SLO = soup.find('h3', string='Subject learning objectives (SLOs)')
        if h3SLO:
            for sibling in h3SLO.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseSLO.append(sibling.get_text(strip=True))
            courseSLO = ' '.join(courseSLO).strip()
        else:
            courseSLO = 'unknown'

        h3CILO = soup.find('h3', string='Course intended learning outcomes (CILOs)')
        if h3CILO:
            for sibling in h3CILO.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseCILO.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseCILO = ' '.join(courseCILO).strip()
        else:
            courseCILO = 'unknown'

        h3Strategy = soup.find('h3', string='Teaching and learning strategies')
        if h3Strategy:
            for sibling in h3Strategy.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseStrategy.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseStrategy = ' '.join(courseStrategy).strip()
        else:
            courseStrategy = 'unknown'

        h3Content = soup.find('h3', string='Content (topics)')
        if h3Content:
            for sibling in h3Content.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseContent.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseContent = ' '.join(courseContent).strip()
        else:
            courseContent = 'unknown'

        h3Assessment = soup.find('h3', string='Assessment')
        if h3Assessment:
            for sibling in h3Assessment.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseAssessment.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseAssessment = ' '.join(courseAssessment).strip()
        else:
            courseAssessment = 'unknown'

        h3MinRequirement = soup.find('h3', string='Minimum requirements')
        if h3MinRequirement:
            for sibling in h3MinRequirement.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseMinRequirements.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseMinRequirements = ' '.join(courseMinRequirements).strip()
        else:
            courseMinRequirements = 'unknown'

        h3RequiredText = soup.find('h3', string='Required texts')
        if h3RequiredText:
            for sibling in h3RequiredText.find_next_siblings():
                if sibling.name == 'h3':  # Stop if another <h3> is found
                    break
                courseRequiredTexts.append(ILLEGAL_CHARACTERS_RE.sub("", sibling.get_text(strip=True)))
            courseRequiredTexts = ' '.join(courseRequiredTexts).strip()
        else:
            courseRequiredTexts = 'unknown'

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


        # print("courseID", row['courseID'])   
        # print("courseTitle", row['courseTitle'])
        # print("courseCreditPoints", courseCreditPoints)
        # print("courseOrganisationalName", courseOrganisationalName)
        # print("courseLevel", courseLevel)
        # print("courseResultType", courseResultType)
        # print("courseRequisite", courseRequisite)
        # print("courseDescription", courseDescription)
        # print("courseSLO", courseSLO)
        # print("courseCILO", courseCILO)
        # print("courseStrategy", courseStrategy)
        # print("courseContent", courseContent)
        # print("courseAssessment", courseAssessment)
        # print("courseMinRequirements", courseMinRequirements)
        # print("courseRequiredTexts", courseRequiredTexts)
        # print("courseReferences", courseReferences)
        # print("courseOtherResources", courseOtherResources)

        df = pd.read_excel(file_path)

        empty_row_index = df['courseCreditPoints'].isnull().idxmax()
        df.at[empty_row_index, 'courseCreditPoints'] = courseCreditPoints
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseOrganisationalName'].isnull().idxmax()
        df.at[empty_row_index, 'courseOrganisationalName'] = courseOrganisationalName
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseLevel'].isnull().idxmax()
        df.at[empty_row_index, 'courseLevel'] = courseLevel
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseResultType'].isnull().idxmax()
        df.at[empty_row_index, 'courseResultType'] = courseResultType
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseDescription'].isnull().idxmax()
        df.at[empty_row_index, 'courseDescription'] = courseDescription
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseSLO'].isnull().idxmax()
        df.at[empty_row_index, 'courseSLO'] = courseSLO
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseCILO'].isnull().idxmax()
        df.at[empty_row_index, 'courseCILO'] = courseCILO
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseStrategy'].isnull().idxmax()
        df.at[empty_row_index, 'courseStrategy'] = courseStrategy
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseContent'].isnull().idxmax()
        df.at[empty_row_index, 'courseContent'] = courseContent
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseAssessment'].isnull().idxmax()
        df.at[empty_row_index, 'courseAssessment'] = courseAssessment
        df.to_excel(file_path, index=False)
        
        empty_row_index = df['courseMinRequirements'].isnull().idxmax()
        df.at[empty_row_index, 'courseMinRequirements'] = courseMinRequirements
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseRequiredTexts'].isnull().idxmax()
        df.at[empty_row_index, 'courseRequiredTexts'] = courseRequiredTexts
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseReferences'].isnull().idxmax()
        df.at[empty_row_index, 'courseReferences'] = courseReferences
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseOtherResources'].isnull().idxmax()
        df.at[empty_row_index, 'courseOtherResources'] = courseOtherResources
        df.to_excel(file_path, index=False)

        empty_row_index = df['courseRawText'].isnull().idxmax()
        df.at[empty_row_index, 'courseRawText'] = courseRawText
        df.to_excel(file_path, index=False)


        # print(courseRawText)


def get_all_links(url):
    driver = webdriver.Chrome()
    driver.get(url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html5lib')

    ie = soup.find('div', class_='ie-images')
    
    with open('2025_UTS_Handbook_Data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['courseID', 'courseTitle', 'courseLink'])

        if ie:
            links = ie.find_all('a', href=True)
            for link in links:
                title = link.next_sibling
                print(title)

                csv_writer.writerow([link.text, title, link['href']])

    driver.quit()








# h3_tag = soup.find('h3', string=lambda text: "Description" in text if text else False)
# # print(h3_tag)


# get_all_links("https://www.handbook.uts.edu.au/subjects/numerical.html")


