from reports.students import report_students
from reports.attendance import report_attendance
from reports.homework_checked import report_homework_checked
from reports.topics import report_topics
from reports.schedule import report_schedule
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
import os

UPLOAD_DIR = "uploads"
MAX_MSG_LENGTH = 4000


async def start(update, context):
    await update.message.reply_text(
        "Привет! \n"
        "Отправь Excel-файл (.xls или .xlsx), и я его обработаю."
        "\n\nP.S. Файлы пока сохраняю во временную папку"
    )


async def send_long_message(update, text, chunk_size=MAX_MSG_LENGTH):
    "для длинных отчеты "
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if i + chunk_size < len(text) and chunk[-1] != '\n':
            chunk += "..."
        await update.message.reply_text(chunk)
        #пауза


async def handle_document(update, context):
    "обработчик файлов"
    document = update.message.document
    file_name = document.file_name.lower()

    # Проверка расширения
    if not (file_name.endswith(".xls") or file_name.endswith(".xlsx")):
        await update.message.reply_text("Пожалуйста, отправь Excel-файл (.xls или .xlsx)")
        return

    # Создание папки если нет
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")  # В продакшене логгер
        await update.message.reply_text("Ошибка при сохранении файла")
        return

    # Скачка файла
    try:
        file = await document.get_file()
        file_path = os.path.join(UPLOAD_DIR, document.file_name)
        await file.download_to_drive(file_path)
    except Exception as e:
        print(f"Не скачался файл: {e}")
        await update.message.reply_text("Не удалось скачать файл")
        return

    # тип отчета по имени файла
    report = None

    if "расписание" in file_name:
        report = report_schedule(file_path)
        # Расписание обычно короткое
        await update.message.reply_text(report)
        return

    elif "тем" in file_name:
        report = report_topics(file_path)

    elif "студент" in file_name:
        report = report_students(file_path)

    elif "посещаемост" in file_name:  #посещаемость
        report = report_attendance(file_path)

    elif "отчет по домашним" in file_name or "домашн" in file_name:
        # ДЗ
        report = report_homework_checked(file_path)

    else:
        # Файл не понят
        await update.message.reply_text(
            f"Файл '{document.file_name}' получен, но я не понял, что с ним делать.\n"
            f"Поддерживаемые отчеты:\n"
            f"- Студенты\n- Посещаемость\n- Темы\n- Расписание\n- Домашние задания\n\n"
            f"Добавь соответствующее слово в название файла"
        )
        return

    # Отправляем длинный отчет
    if report:
        await send_long_message(update, report)
    else:
        await update.message.reply_text("Что-то пошло не так - отчет не сформирован")



def main():
    "запуск"
    try:
        app = Application.builder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        # Бот отвечает только на документы
        app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        # TODO: добавить команду /help

        print("Бот запускается...")
        print(f"Папка для загрузок: {os.path.abspath(UPLOAD_DIR)}")

        app.run_polling()

    except Exception as e:
        print(f"Ошибка запуска: {e}")


if __name__ == "__main__":
    # Проверка на наличие токена
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TOKEN_HERE":
        print("ОШИБКА: Не задан токен бота в config.py")
        exit(1)

    main()