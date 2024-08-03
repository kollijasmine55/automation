from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # Navigate to the FitPeo homepage
    driver.get("https://www.fitpeo.com/")
    time.sleep(3)  # Wait for the page to load

    # Navigate to the Revenue Calculator
    revenue_calculator_link = driver.find_element(By.LINK_TEXT, "Revenue Calculator")
    revenue_calculator_link.click()
    time.sleep(3)  # Wait for the page to load
    
  
    # Step 4: Adjust the Slider
    slider = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='range']")))
    driver.execute_script("arguments[0].scrollIntoView();", slider)
    slider_value = 820
    driver.execute_script(f"arguments[0].value = {slider_value}; arguments[0].dispatchEvent(new Event('input'));", slider)
    
    # Step 5: Update the Text Field
    text_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='revenue-text-field']")))
    text_field.clear()
    text_field.send_keys('560')
    
    # Validate Slider Value
    # Wait for slider to update
    time.sleep(2)
    updated_slider_value = slider.get_attribute('value')
    assert updated_slider_value == '560', f"Slider value mismatch: Expected 560, got {updated_slider_value}"
    
    # Step 6: Select CPT Codes
    cpt_codes = [
        'CPT-99091', 
        'CPT-99453', 
        'CPT-99454', 
        'CPT-99474'
    ]
    
    for code in cpt_codes:
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{code}']/preceding-sibling::input")))
        if not checkbox.is_selected():
            checkbox.click()
    
    # Step 7: Validate Total Recurring Reimbursement
    reimbursement_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@id='total-reimbursement']")))
    assert reimbursement_header.text == "$110700", f"Total Recurring Reimbursement mismatch: Expected $110700, got {reimbursement_header.text}"
    
finally:
    # Cleanup
    time.sleep(5)  # Just to observe the final state, remove this in production
    driver.quit()
