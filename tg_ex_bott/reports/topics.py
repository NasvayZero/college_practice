import pandas as pd
import re


def report_topics(file_path: str) -> str:
    """
    Чекаем темы уроков на соответствие формату
    Должно быть: 'Урок № _. Тема: _'
    Возвращаем список неправильных
    """

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return f"Не открылся файл: {e}"

    # Ищем колонку с темами - может называться по-разному
    topic_column = None
    for col in df.columns:
        if "тема" in str(col).lower() or "урок" in str(col).lower():
            topic_column = col
            break

    if not topic_column:
        return f"Не нашёл колонку с темами. Есть: {', '.join(df.columns.tolist())}"

    # Регулярка - пробуем разные варианты
    patterns = [
        r"^\s*Урок\s*№\s*\d+\.\s*Тема:\s*.+$",  # строгий
        r"^\s*Урок\s*\d+\s*\.\s*Тема:\s*.+$",  # без №
        r"^\s*Урок\s*№\s*\d+\s*Тема:\s*.+$"  # без точки
    ]

    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

    invalid_topics = []

    for idx, topic in enumerate(df[topic_column], 1):
        # Пропускаем пустые
        if pd.isna(topic):
            invalid_topics.append(f"[строка {idx}] <пусто>")
            continue

        text = str(topic).strip()
        if not text:  # Пустая строка
            invalid_topics.append(f"[строка {idx}] <пустая строка>")
            continue

        # Проверяем по всем паттернам
        is_valid = False
        for pattern in compiled_patterns:
            if pattern.match(text):
                is_valid = True
                break

        if not is_valid:
            invalid_topics.append(f"{text}")

    # Формируем ответ
    if not invalid_topics:
        return "Все темы в правильном формате!"

    lines = [
        "⚠НЕПРАВИЛЬНЫЕ ТЕМЫ:",
        f"Всего ошибок: {len(invalid_topics)}",
        ""
    ]

    for i, topic in enumerate(invalid_topics, 1):
        lines.append(f"{i}. {topic}")


    return "\n".join(lines)