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
def scrape_jobs(soup):
    jobs_by_department = {}

    # Find all the div elements with class 'page-job-list-wrapper'
    job_wrappers = soup.find_all('div', {'class': 'page-job-list-wrapper'})

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
        job_link_element = job_wrapper.find('a', {'class': 'btn btn-action btn-lg a-btn'})

        job_link = job_link_element['href']

        # Check if the link opens in a new window/tab
        if 'target' in job_link_element.attrs and job_link_element['target'] == '_blank':
            # Open job link in a new tab
            driver.execute_script("window.open('" + job_link + "', '_blank');")
        else:
            # Open job link in the current tab
            job_link_element.click()

        # Wait for the new tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Switch to the newly opened tab
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        time.sleep(2)

        # Get job details from the new tab
        source2 = driver.page_source
        soup2 = bs(source2, 'html.parser')
        detail = soup2.find('div', {'class': 'job-sections'})
        job_desc = [desc.text.strip() for desc in detail.find_all('div', {'class': 'wysiwyg', 'itemprop':"responsibilities"})]
        qualifications = [q.text.strip() for q in detail.find_all('div', {'class': 'wysiwyg', 'itemprop': 'qualifications'})]

        # Build job data structure
        job_data = {
            "title": job_title,
            "location": job_location,
            "description": job_desc,
            "qualification": qualifications,
            "job_type": job_type
        }

        # Group jobs by department
        if job_department not in jobs_by_department:
            jobs_by_department[job_department] = []

        jobs_by_department[job_department].append(job_data)

        # Close the new tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(window_handles[0])

    return jobs_by_department

jobs_by_department = {}

page_count = 1
print('On Progress . . .')
# Start scraping
driver.get(url2)
while page_count <= max_page:
    source = driver.page_source
    soup = bs(source, 'html.parser')

    jobs_data = scrape_jobs(soup)

    for department, jobs_list in jobs_data.items():
        if department not in jobs_by_department:
            jobs_by_department[department] = []
        jobs_by_department[department].extend(jobs_list)

    # driver.get(url2)
    # for _ in range(page_count):
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

# Save data in JSON format
with open('job_list.json', 'w') as json_file:
    json.dump(jobs_by_department, json_file, indent=4)

print('Scraping Done . . .')
driver.quit()
