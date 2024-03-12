from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd

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
soup = bs(source,'html.parser')

# Find all the div elements with class 'page-job-list-wrapper'
job_wrappers = soup.find_all('div', {'class': 'page-job-list-wrapper'})

job_list =[]

# Iterate through each job wrapper
for job_wrapper in job_wrappers:
    # Find the strong element with class 'text-color-blue' (job title)
    job_title = job_wrapper.find('strong', {'class': 'text-color-blue'}).text

    # Find the p element with class 'text-color-base-light' (job type)
    job_type = job_wrapper.find('p', {'class': 'text-color-base-light'}).text

    # Find the p element with string 'Engineering' (job department)
    job_department = job_wrapper.find('p', {'class': 'job-detail margin-0 margin-right-20 sm'}).text

    # Find the div element with class 'jobs-location-wrapper' (job location)
    job_location= job_wrapper.find('div', {'class': 'jobs-location-wrapper'})
    # print(job_location_wrapper)

    # Find the a element with class 'btn btn-action btn-lg a-btn' (job application link)
    job_link = job_wrapper.find('a', {'class': 'btn btn-action btn-lg a-btn'})['href']
    
    source2 = job_link
    
    soup2= bs(source2,'html.parser')
    
    detail = soup2.find('div',{'class': 'job-sections'})
    job_desc= detail.find('div',{'class': 'wysiwyg'}).text
    q = detail.find('div', attrs={'class': 'wysiwyg', 'itemprop': 'qualifications'}).text
    

    job_list.append([job_title,job_type,job_department,job_location,job_desc,q])
    
df = pd.DataFrame(job_list,columns=['Job Title','Job Type','Job Department','Job Location','Job Desc','Qualification'])
df.to_csv('results/result.csv')
print('done')
driver.quit()
