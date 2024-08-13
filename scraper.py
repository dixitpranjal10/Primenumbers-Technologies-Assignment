from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# Go to the target URL
driver.get('https://hprera.nic.in/PublicDashboard')

# Wait for the page to fully load
time.sleep(5)  # Adjust the sleep time if necessary

# Find the "Registered Projects" section by locating the RERA numbers (these are links)
project_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'ProjectDetail')]")

# Collect the first 6 project links
first_six_links = project_links[:6]

project_data = []

for link in first_six_links:
    link.click()  # Click on the link to open project details
    time.sleep(2)  # Wait for the page to load

    # Scrape the required fields
    gstin = driver.find_element(By.XPATH, "//*[contains(text(), 'GSTIN No')]").find_element(By.XPATH, "./following-sibling::td").text
    pan = driver.find_element(By.XPATH, "//*[contains(text(), 'PAN No')]").find_element(By.XPATH, "./following-sibling::td").text
    name = driver.find_element(By.XPATH, "//*[contains(text(), 'Name')]").find_element(By.XPATH, "./following-sibling::td").text
    permanent_address = driver.find_element(By.XPATH, "//*[contains(text(), 'Permanent Address')]").find_element(By.XPATH, "./following-sibling::td").text

    # Store the scraped data
    project_data.append({
        'GSTIN No': gstin,
        'PAN No': pan,
        'Name': name,
        'Permanent Address': permanent_address
    })

    driver.back()  # Go back to the previous page
    time.sleep(2)  # Wait for the page to load again

# Close the browser
driver.quit()

# Convert the collected data into a DataFrame
df = pd.DataFrame(project_data)

# Save the data to a CSV file
df.to_csv('outputs/registered_projects.csv', index=False)

# Optionally, display the DataFrame
print(df)
