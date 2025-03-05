import json
import datetime
import telegram
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Токен для Telegram бота
bot_token = '7626080007:AAFJzXjTjIkp850hzv7y-jKbptFaCJVPHvk'
bot = Bot(token=bot_token)

# Google Sheets налаштування
SHEET_ID = '16RcTCes8HywiOofiQpEed09o3KQCRORq1_841BCcMws'  # Ваш ID Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Авторизація через сервісний акаунт
def authenticate_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

# Запис даних в Google Sheets
def update_google_sheet(sheet, data):
    try:
        # Форматування дати
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [date] + data  # Додаємо поточну дату до даних
        sheet.append_row(row)  # Записуємо в таблицю
        print("Дані успішно додано в таблицю!")
    except HttpError as err:
        print(f"Помилка при оновленні таблиці: {err}")

# Обробка отриманих даних
def process_data(update, context):
    # Отримуємо дані з повідомлення в Telegram
    user_data = json.loads(update.message.text)  # Дані приходять у вигляді JSON
    sheet = authenticate_google_sheets()  # Отримуємо доступ до таблиці

    # Відправка даних до Google Sheets
    update_google_sheet(sheet, [
        user_data.get('sleep_time', ''),
        user_data.get('wake_up_time', ''),
        user_data.get('steps', ''),
        user_data.get('task_performance', ''),
        user_data.get('mood_morning', ''),
        user_data.get('mood_evening', ''),
        user_data.get('mood_day', '')
    ])

    # Відправляємо підтвердження користувачеві
    update.message.reply_text("Дані успішно записано в таблицю.")

# Основна функція для запуску бота
def start_bot():
    updater = telegram.ext.Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Обробка команди /start
    dp.add_handler(telegram.ext.CommandHandler("start", lambda update, context: update.message.reply_text("Вітаємо!")))

    # Обробка текстових повідомлень
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, process_data))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запускаємо бота
if __name__ == '__main__':
    start_bot()
