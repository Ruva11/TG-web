from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Ідентифікатор таблиці
SPREADSHEET_ID = '16RcTCes8HywiOofiQpEed09o3KQCRORq1_841BCcMws'

# Діапазон, в який будемо записувати дані
RANGE_NAME = 'Sheet1!A1'  # Тут вказується діапазон (наприклад, A1 для першої клітинки)

# Ось твій Client ID та Client Secret
CLIENT_ID = '863136000334-5ofd8nuanh0ftjmqmkk84hbtslqbk0f6.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# Авторизація через OAuth 2.0
def authenticate_google_sheets():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',  # Тобі потрібно завантажити цей файл з Google Console
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    creds = flow.run_local_server(port=0)
    return creds

# Запис даних у таблицю
def update_sheet():
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)

    # Дані для запису
    values = [
        ["Дата", "Параметр 1", "Параметр 2", "Параметр 3"],  # Це заголовки стовпців
        ["2025-03-05", "50", "60", "70"]  # Це приклад даних
    ]
    body = {
        'values': values
    }

    # Оновлюємо таблицю
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as err:
        print(f"An error occurred: {err}")

# Викликаємо функцію
update_sheet()
