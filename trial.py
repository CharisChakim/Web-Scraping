from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Function to scrape job data
def scrape_job_data():
    # Find all Apply buttons
    apply_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn btn-action btn-lg a-btn']"))
    )

    # Iterate through each Apply button
    for apply_button in apply_buttons:
        # Click the Apply button to open the job page
        apply_button.click()
        
        # Switch to the new window/tab
        driver.switch_to.window(driver.window_handles[1])
        
        # Here you can scrape data from the new page
        # For example, you can find elements by XPath and extract text
        # Example:
        job_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/main/h1"))
        )
        job_location = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/main/ul/li[1]/span/spl-job-location"))
        )
        job_desc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="st-jobDescription"]/div[2]'))
        )
        job_q = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="st-qualifications"]/div[2]'))
        )
       
        job_title = job_title.text
        job_location = job_location.text
        job_desc = job_desc.text
        job_q = job_q.text
        
        print('Job Title: {job_title}\nLocation: {job_location}\nDesc: {job_desc}\nQ: {job_q}'.format(job_title=job_title, job_location=job_location, job_desc=job_desc, job_q=job_q))


        # Close the new window/tab and switch back to the original one
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

# Function to click the arrow button and scrape job data
def click_arrow_and_scrape():
    while True:
        # Find the arrow button
        arrow_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.arrow-icon"))
        )
        
        # Click the arrow button
        arrow_button.click()
        
        # Scrape job data
        scrape_job_data()
        
        # Check if the arrow button is disabled (reached the end)
        arrow_disabled = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.arrow-icon.disabled"))
        )
        if arrow_disabled:
            break

# Start the process
click_arrow_and_scrape()

# Close the browser
driver.quit()
