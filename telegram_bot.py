from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT
import requests

# URL нашего API
API_URL = "http://127.0.0.1:5000/analyze"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Отправь мне текст, и я проанализирую его тональность и ключевые слова."
    )

# Обработчик текстовых сообщений
async def analyze_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text  # Текст, который отправил пользователь

    # Отправка запроса на API
    try:
        response = requests.post(
            API_URL,
            json={"text": user_text},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            sentiment = data["sentiment"][0]["label"]
            keywords = ", ".join(data["keywords"])
            # Ответ пользователю
            await update.message.reply_text(
                f"Тональность текста: {sentiment}\nКлючевые слова: {keywords}"
            )
        else:
            await update.message.reply_text("Ошибка анализа текста. Попробуйте снова.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Основная функция
def main() -> None:
    # Замените 'YOUR_TOKEN' на токен вашего Telegram-бота
    TELEGRAM_TOKEN = "7901896521:AAFZWa84z_L80G4ajtKvHoVT8Fiv2iYHR_c"

    # Создание приложения
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(TEXT, analyze_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
