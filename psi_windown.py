import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Инициализация Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Режим без графического интерфейса
driver = webdriver.Chrome()

# Функция для анализа страницы
def analyze_page(url):
    print("Анализируется страница:", url)
    driver.get("https://pagespeed.web.dev/")
    # Ожидание появления поля для ввода URL
    url_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="url"]'))
    )
    # Вставка ссылки в поле для ввода URL
    url_input.clear()  # Очистка поля, если там уже есть текст
    url_input.send_keys(url)
    url_input.send_keys(Keys.RETURN)  # Нажатие Enter для отправки формы
    try:
        # Ждем появления результата
        result_element = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'g.lh-exp-gauge__inner text.lh-exp-gauge__percentage'))
        )
        result = result_element.text
        print("Результат для mobile", url, ":", result)

        # Нажатие на таб
        tab_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.VfPpkd-YVzG2b[jsname="ksKsZd"]')
        if len(tab_buttons) >= 2:  # Есть два элемента
            tab_button = tab_buttons[1]  # Выбор второго элемента по индексу
            tab_button.click()  # Выполнение действия с выбранным элементом

        # Получение данных по новому CSS селектору
        new_result_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.lh-exp-gauge__inner .lh-exp-gauge__percentage'))
        )

        new_result = new_result_element.text
        print("Результат для desktop", url, ":", new_result)
    finally:
        # Независимо от результата, закрываем браузер
        driver.quit()

# Анализируем страницу https://pagespeed.web.dev/
analyze_page("https://haieronline.ru/")