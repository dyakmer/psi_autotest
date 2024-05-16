from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def analyze_page(url):
    chrome_options = Options()
    driver = webdriver.Chrome()

    try:
        print("Анализируется страница:", url)
        driver.get("https://pagespeed.web.dev/")
        url_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="url"]'))
        )
        url_input.clear()
        url_input.send_keys(url)
        url_input.send_keys(Keys.RETURN)

        result_element = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, '(//*[@class="lh-exp-gauge__percentage"])[1]'))
        )
        result = result_element.text
        print("Результат анализа mobile", url, ":", result)

        tab_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.VfPpkd-YVzG2b[jsname="ksKsZd"]')
        if len(tab_buttons) >= 2:
            tab_button = tab_buttons[1]
            tab_button.click()

        new_result_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '(//*[@class="lh-exp-gauge__percentage"])[2]'))
        )

        new_result = new_result_element.text
        print("Результат анализа desktop", url, ":", new_result)
    finally:
        driver.quit()
