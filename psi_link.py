from psi_windown import analyze_page
from google_sheets import update_google_sheet

# Запуск скрипта
if __name__ == '__main__':
    urls = [
        "https://haieronline.ru/", #Главная
        "https://haieronline.ru/offers/super-discount/", #Супер акция
        "https://haieronline.ru/catalog/appliances/fridges/", #Каталог холодильников
        "https://haieronline.ru/catalog/appliances/fridges/kholodilnik-haier-cef535awd/" #Деталка холодильника
    ]

    descriptions = [
        "Главная",
        "Супер акция",
        "Каталог холодильников",
        "Деталка холодильника"
    ]

    for url, description in zip(urls, descriptions):
        mobile_result, desktop_result = analyze_page(url, description)
