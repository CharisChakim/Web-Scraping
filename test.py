from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import json
import time

# Mendapatkan konten HTML dari halaman web
url = "https://www.cermati.com/karir"
driver = webdriver.Chrome()

# Open web
driver.get(url)
time.sleep(2) # timer untuk load web
print('Scaping Start . . . ')

# Klik tombol "View All Jobs"
view_all_jobs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View All Jobs')]"))
)
view_all_jobs_button.click()

# Simpan URL saat ini
url2 = driver.current_url

# Klik tombol "Last Page" untuk mengakses halaman terakhir dan mengetahui max page
last_page_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[11]/div/button[10]'))
)
last_page_button.click()

page = bs(driver.page_source, 'html.parser') # Parsing konten HTML yang baru

active_page_button = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[11]/div/button[8]').text

max_page = int(active_page_button)

# Fungsi untuk mengekstrak data dari halaman pekerjaan dan menyimpannya dalam struktur data
def scrape_job(job_wrapper):
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
    time.sleep(2)
    source2 = driver.page_source
    soup2 = bs(source2, 'html.parser')

    detail = soup2.find('div', {'class': 'job-sections'})
    job_desc = [desc.text.strip() for desc in detail.find_all('div', {'class': 'wysiwyg'})]
    qualifications = [q.text.strip() for q in detail.find_all('div', {'class': 'wysiwyg', 'itemprop': 'qualifications'})]

    # Build Structure Data
    job_data = {
        "title": job_title,
        "location": job_location,
        "description": job_desc,
        "qualification": qualifications,
        "job_type": job_type,
        "department": job_department
    }

    return job_data

jobs_by_department = {}

page_count = 0
print('On Progres . . .')
# start scrapping
while page_count <= max_page:
    source = driver.page_source
    soup = bs(source, 'html.parser')

    # Find all the div elements with class 'page-job-list-wrapper'
    job_wrappers = soup.find_all('div', {'class': 'page-job-list-wrapper'})

    # Create a ThreadPoolExecutor with a maximum of 4 workers
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Use executor.map to apply scrape_job function to each job wrapper in parallel
        job_datas = list(executor.map(scrape_job, job_wrappers))

    # Group job data by department
    for job_data in job_datas:
        job_department = job_data['department']
        if job_department not in jobs_by_department:
            jobs_by_department[job_department] = []
        jobs_by_department[job_department].append(job_data)

    driver.get(url2)
    for _ in range(page_count):
        try:
            next_button_xpath = '//*[@id="career-jobs"]/div/div[6]/div/div[11]/div/button[9]'
            next_button = driver.find_element(By.XPATH, next_button_xpath)
            next_button.click()
            time.sleep(2)
        except NoSuchElementException:
            next_button = None
            break

    page_count += 1
    time.sleep(2)

# Save as format JSON
with open('job_list.json', 'w') as json_file:
    json.dump(jobs_by_department, json_file, indent=4)

print('Scraping Done . . .')
driver.quit()
