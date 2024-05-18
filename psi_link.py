from psi_windown import analyze_page

# Запуск скрипта
if __name__ == '__main__':
    urls = [
        "https://haieronline.ru/",
        "https://haieronline.ru/offers/super-discount/",
        "https://haieronline.ru/catalog/appliances/fridges/",
        "https://haieronline.ru/catalog/appliances/fridges/kholodilnik-haier-cef535awd/"
    ]

    for url in urls:
        analyze_page(url)
