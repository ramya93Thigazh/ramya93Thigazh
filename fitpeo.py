import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.order(1)
def test_fit(driver):
    try:
        # Navigate to FitPeo Homepage
        driver.get('https://fitpeo.com')  # Update to the actual FitPeo homepage URL
        ActionChains(driver)
        # Wait for the page to load and navigate to the Revenue Calculator Page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Revenue Calculator'))).click()

        scrol = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,':r')][contains(@class,'MuiInputBase')]")))
        driver.execute_script("arguments[0].scrollIntoView();", scrol)
        time.sleep(3)


        #adjust slider
        slider = driver.find_element(By.XPATH, "//input[@type='range']")
        driver.execute_script("arguments[0].scrollIntoView();", slider)
        time.sleep(3)

        # Verify  slider value
        slider = driver.find_element(By.XPATH, "//input[@type='range']")
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'))",slider, 820)
        time.sleep(3)
        # Verify the text field value
        text_field = driver.find_element(By.XPATH, "//input[contains(@id,':r')][contains(@class,'MuiInputBase')]")

        text_field.clear()
        time.sleep(3)
        text_field=driver.find_element(By.XPATH, "//input[contains(@id,':r')][contains(@class,'MuiInputBase')]")
        text_field.send_keys("820")

        assert text_field.get_attribute("value") == "2000"
        # Update the text field to 560

        text_field.clear()
        text_field.send_keys("560")
        text_field.send_keys(Keys.RETURN)

        # Wait for the slider to update


        # Verify the slider position
        assert slider.get_attribute("value") == "2000"

        # Select CPT Codes
        cpt_codes = ["(//input[contains(@class,'PrivateSwitchBase-input')])[1]", "(//input[contains(@class,'PrivateSwitchBase-input')])[2]", "(//input[contains(@class,'PrivateSwitchBase-input')])[3]", "(//input[contains(@class,'PrivateSwitchBase-input')])[8]"]
        for code in cpt_codes:
            checkbox = driver.find_element(By.XPATH, code)
            if not checkbox.is_selected():
                checkbox.click()

        # Validate Total Recurring Reimbursement:
        total_reimbursement = driver.find_element(By.ID, "totalReimbursement").text
        assert total_reimbursement == "$110700"

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred:{e}")
