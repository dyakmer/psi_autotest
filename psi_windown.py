from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time

MAX_RETRIES = 3
WAIT_TIME_BETWEEN_RETRIES = 2

def create_driver():
    chrome_options = Options()
    return webdriver.Chrome(options=chrome_options)

def load_url_with_retries(driver, url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except WebDriverException as e:
            print(f"Ошибка при загрузке страницы (попытка {attempt + 1}/{retries}): {e}")
            time.sleep(WAIT_TIME_BETWEEN_RETRIES)
    return False

def find_element_with_retries(driver, by, value, retries=MAX_RETRIES, timeout=10):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Не удалось найти элемент (попытка {attempt + 1}/{retries}): {e}")
            time.sleep(WAIT_TIME_BETWEEN_RETRIES)
    return None

def analyze_page(url):
    for attempt in range(MAX_RETRIES):
        driver = create_driver()
        try:
            print(f"Анализируется страница (попытка {attempt + 1}/{MAX_RETRIES}):", url)

            if not load_url_with_retries(driver, "https://pagespeed.web.dev/"):
                print("Не удалось загрузить страницу https://pagespeed.web.dev/ после нескольких попыток.")
                continue

            url_input = find_element_with_retries(driver, By.CSS_SELECTOR, 'input[name="url"]')
            if url_input is None:
                print("Не удалось найти поле ввода URL на странице.")
                continue

            url_input.clear()
            url_input.send_keys(url)
            url_input.send_keys(Keys.RETURN)

            result_element = find_element_with_retries(driver, By.XPATH, '(//*[@class="lh-exp-gauge__percentage"])[1]', timeout=120)
            if result_element is None:
                print(f"Не удалось получить результат анализа мобильной версии для {url}.")
                continue

            mobile_result = result_element.text
            print("Результат анализа mobile", url, ":", mobile_result)

            tab_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.VfPpkd-YVzG2b[jsname="ksKsZd"]')
            if not tab_buttons or len(tab_buttons) < 2:
                print("Не найдены кнопки переключения вкладок анализа.")
                continue

            tab_button = tab_buttons[1]
            tab_button.click()

            new_result_element = find_element_with_retries(driver, By.XPATH, '(//*[@class="lh-exp-gauge__percentage"])[2]', timeout=30)
            if new_result_element is None:
                print(f"Не удалось получить результат анализа десктопной версии для {url}.")
                continue

            desktop_result = new_result_element.text
            print("Результат анализа desktop", url, ":", desktop_result)

            return mobile_result, desktop_result

        except WebDriverException as e:
            print(f"Произошла ошибка при работе с WebDriver: {e}")
        finally:
            driver.quit()

    print(f"Не удалось получить результаты анализа для {url} после нескольких попыток.")
    return None, None
