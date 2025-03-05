import json
import telegram
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Токен для Telegram бота
bot_token = '7626080007:AAFJzXjTjIkp850hzv7y-jKbptFaCJVPHvk'
bot = Bot(token=bot_token)

# Google Sheets налаштування
SHEET_ID = '16RcTCes8HywiOofiQpEed09o3KQCRORq1_841BCcMws'  # Ваш ID Google Sheets

# Авторизація для доступу до Google Sheets через сервісний акаунт
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Отримуємо доступ до таблиці
sheet = client.open_by_key(SHEET_ID).sheet1

# Функція для запису даних в Google Sheets
def update_google_sheet(data):
    try:
        # Форматування дати
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [date] + data  # Додаємо поточну дату до даних

        # Записуємо в таблицю
        sheet.append_row(row)
        print("Дані успішно додано в таблицю!")
    except HttpError as err:
        print(f"Помилка при оновленні таблиці: {err}")

# Функція для обробки отриманих даних
def process_data(update, context):
    # Отримуємо дані з повідомлення в Telegram
    user_data = json.loads(update.message.text)  # Данні приходять у вигляді JSON

    # Отправка даних до Google Sheets
    update_google_sheet([
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

    # Обробка текстових повідомлень (це будуть наші дані з Telegram Web App)
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, process_data))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запускаємо бота
if __name__ == '__main__':
    start_bot()
