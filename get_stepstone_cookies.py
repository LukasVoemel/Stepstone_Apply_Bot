from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

import time 

driver = webdriver.Chrome()
driver.get("https://www.stepstone.de")


driver.implicitly_wait(2)

cookies1 = driver.find_element(By.CSS_SELECTOR, "#ccmgt_explicit_preferences")
cookies1.click()

driver.implicitly_wait(2)

cookies2 = driver.find_element(By.CSS_SELECTOR, "#ccmgt_preferences_reject")
cookies2.click()


login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='sub-menu-item' and @aria-label='Login']"))
)
login_button.click()

login_button2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='sign-in']"))
)
login_button2.click()

driver.find_element(By.CSS_SELECTOR, "input[data-testid='email-input']").send_keys('Your Username')
driver.find_element(By.CSS_SELECTOR, "input[data-testid='password-input']").send_keys('Your Password')


login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-submit-btn']")
login_button.click()

time.sleep(5)

cookies = driver.get_cookies()
print(cookies)

pickle.dump(cookies, open("cookies.pkl", 'wb'))




