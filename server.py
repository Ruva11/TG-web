import subprocess
import sys

# Перевірка наявності необхідних бібліотек та їх встановлення
required_libraries = ['Flask', 'gspread', 'oauth2client', 'google-api-python-client', 'telegram']

for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(f"Бібліотека {library} не знайдена, встановлюється...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Тепер можна додавати основний код, використовуючи ці бібліотеки

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import telegram
from telegram import Bot
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify

# Ваші налаштування
SPREADSHEET_ID = '16RcTCes8HywiOofiQpEed09o3KQCRORq1_841BCcMws'
RANGE_NAME = 'Sheet1!A1'
bot_token = '7626080007:AAFJzXjTjIkp850hzv7y-jKbptFaCJVPHvk'

# Створення Flask додатку
app = Flask(__name__)

# Авторизація для Google Sheets через OAuth
def authenticate_google_sheets():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',  # Файл credentials.json потрібно завантажити з Google Console
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    creds = flow.run_local_server(port=0)
    return creds

# Функція для запису в Google Sheets
def update_google_sheet(data):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    
    values = [
        ["Дата", "Час засинання", "Час підйому", "Кроки", "Результативність", "Настрій зранку", "Настрій ввечері", "Загальний настрій"],
        [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), *data]  # додамо поточну дату та час
    ]
    body = {
        'values': values
    }

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as err:
        print(f"Помилка при оновленні таблиці: {err}")

# Створення Telegram бота
bot = Bot(token=bot_token)

# Функція для обробки отриманих даних з Telegram
def process_data(update, context):
    user_data = json.loads(update.message.text)  # Перетворюємо текст на JSON

    # Записуємо дані в Google Sheets
    update_google_sheet([
        user_data.get('bedtime', ''),
        user_data.get('wakeuptime', ''),
        user_data.get('steps', ''),
        user_data.get('taskperformance', ''),
        user_data.get('morningmood', ''),
        user_data.get('eveningmood', ''),
        user_data.get('overallmood', '')
    ])

    # Відправляємо повідомлення назад користувачу
    update.message.reply_text("Дані успішно записано в таблицю.")

# Функція для запуску бота
def start_bot():
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Вітаємо!")))

    # Обробка текстових повідомлень
    dp.add_handler(MessageHandler(Filters.text, process_data))

    updater.start_polling()
    updater.idle()

# Стартуємо бота
if __name__ == '__main__':
    start_bot()

# Flask API для отримання даних
@app.route('/update-google-sheet', methods=['POST'])
def update_data():
    data = request.json  # Отримуємо JSON з запиту
    # Тут додавати код для обробки даних і запису в Google Sheets
    update_google_sheet([data.get('bedtime', ''), data.get('wakeuptime', ''), data.get('steps', ''),
                         data.get('taskperformance', ''), data.get('morningmood', ''),
                         data.get('eveningmood', ''), data.get('overallmood', '')])

    return jsonify({"status": "success", "message": "Дані успішно записано."}), 200

# Запуск Flask серверу
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
