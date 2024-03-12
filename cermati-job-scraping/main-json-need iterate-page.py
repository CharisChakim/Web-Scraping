from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

# Mendapatkan konten HTML dari halaman web
url = "https://www.cermati.com/karir"
driver = webdriver.Chrome()

# Open web
driver.get(url)

# Klik tombol "View All Jobs"
view_all_jobs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View All Jobs')]"))
)
view_all_jobs_button.click()

source = driver.page_source
soup = bs(source, 'html.parser')

# Find all the div elements with class 'page-job-list-wrapper'
job_wrappers = soup.find_all('div', {'class': 'page-job-list-wrapper'})

jobs_by_department = {}

# Iterate through each job wrapper
for job_wrapper in job_wrappers:
    # Find the strong element with class 'text-color-blue' (job title)
    job_title = job_wrapper.find('strong', {'class': 'text-color-blue'}).text

    # Find the p element with class 'text-color-base-light' (job type)
    job_type = job_wrapper.find('p', {'class': 'text-color-base-light'}).text

    # Find the p element with string 'Engineering' (job department)
    job_department = job_wrapper.find('p', {'class': 'job-detail margin-0 margin-right-20 sm'}).text.strip()

    # Find the div element with class 'jobs-location-wrapper' (job location)
    job_location = job_wrapper.find('div', {'class': 'jobs-location-wrapper'}).text.strip()

    # Find the a element with class 'btn btn-action btn-lg a-btn' (job application link)
    job_link = job_wrapper.find('a', {'class': 'btn btn-action btn-lg a-btn'})['href']
    
    driver.get(job_link)
    source2 = driver.page_source
    soup2 = bs(source2, 'html.parser')
    
    detail = soup2.find('div', {'class': 'job-sections'})
    job_desc = [desc.text.strip() for desc in detail.find_all('div', {'class': 'wysiwyg'})]
    qualifications = [q.text.strip() for q in detail.find_all('div', {'class': 'wysiwyg', 'itemprop': 'qualifications'})]

    job_data = {
        "title": job_title,
        "location": job_location,
        "description": job_desc,
        "qualification": qualifications,
        "job_type": job_type
    }
    
    if job_department not in jobs_by_department:
        jobs_by_department[job_department] = []
    
    jobs_by_department[job_department].append(job_data)

# Simpan data ke dalam format JSON
with open('results/result.json', 'w') as json_file:
    json.dump(jobs_by_department, json_file, indent=4)

print('done')
driver.quit()
