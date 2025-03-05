import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Налаштування для Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Your Google Sheets Name").sheet1

# Функція для обробки даних
def process_data(data):
    try:
        # Парсимо отримані дані
        data = json.loads(data)
        # Отримуємо поточний час
        current_time = data.get("datetime")
        bedtime = data.get("bedtime")
        wakeuptime = data.get("wakeuptime")
        steps = data.get("steps")
        taskperformance = data.get("taskperformance")
        morningmood = data.get("morningmood")
        eveningmood = data.get("eveningmood")
        overallmood = data.get("overallmood")

        # Записуємо дані в таблицю
        sheet.append_row([current_time, bedtime, wakeuptime, steps, taskperformance, morningmood, eveningmood, overallmood])
    except Exception as e:
        logging.error(f"Error processing data: {e}")

# Функція для обробки команди /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Введіть ваші дані через веб-додаток.")

# Основна функція для запуску бота
def main():
    updater = Updater("YOUR TELEGRAM BOT TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # Реєструємо команду /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обробляємо отримані дані
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_data))

    # Запускаємо бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
