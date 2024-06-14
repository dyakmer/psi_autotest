from google.oauth2 import service_account
from googleapiclient.discovery import build

# Загрузка JSON ключа
json_keyfile_path = 'service-account-file.json'

# Определение области видимости
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Авторизация
credentials = service_account.Credentials.from_service_account_file(
    json_keyfile_path, scopes=SCOPES)

# Идентификатор таблицы
spreadsheet_id = '14ufsg3FoN7tA30PEj5dq4pIx1v1TEClx-3NygAMVrFo'

# Создание сервиса для работы с API
service = build('sheets', 'v4', credentials=credentials)


# Функция получения следующей свободной строки в столбце B
def get_next_free_row(sheet_name):
    # Чтение данных из столбца B
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!B:B'
    ).execute()
    values = result.get('values', [])

    # Возвращаем следующую свободную строку
    return len(values) + 1


# Функция обновления данных в таблице
def update_google_sheet(mobile_result, desktop_result, url, analysis_time, description):
    # Получение следующей свободной строки
    sheet_name = 'Лист1'
    next_row = get_next_free_row(sheet_name)

    # Определение диапазона для столбцов B, C, D, E и F
    range_ = f'{sheet_name}!B{next_row}:F{next_row}'  # Лист и диапазон

    # Значения для обновления
    values = [
        [mobile_result, desktop_result, url, analysis_time, description]
    ]
    body = {
        'values': values
    }

    # Обновление данных
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f'{result.get("updatedCells")} cells updated.')
