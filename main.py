import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Якщо змінити доступ, потрібно видалити файл token.pickle
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Авторизація через OAuth 2.0
def authenticate():
    creds = None
    # Файл token.pickle зберігає доступ до токенів користувача
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Якщо немає валідних облікових даних, користувач має пройти процес авторизації
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Зберігаємо облікові дані для подальших запитів
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

# Функція для запису даних в таблицю Google Sheets
def append_to_sheet(spreadsheet_id, range_name, values):
    service = authenticate()

    # Формат даних для додавання до таблиці
    body = {
        'values': values
    }

    # Додаємо нові рядки в таблицю
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

# Приклад виклику функції
spreadsheet_id = '16RcTCes8HywiOofiQpEed09o3KQCRORq1_841BCcMws'  # ID твоєї таблиці
range_name = 'Лист1!A2:C2'  # Вибір діапазону, куди будуть записані дані
values = [
    ['2025-03-05', 'Параметр 1', 'Параметр 2']
]

append_to_sheet(spreadsheet_id, range_name, values)
