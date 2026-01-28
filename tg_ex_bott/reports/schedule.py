import pandas as pd
from collections import defaultdict


def report_schedule(file_path: str) -> str:
    """Считаем пары по группам из расписания (эксель)"""

    # Читаем файл - всё как текст чтобы не глючило
    try:
        df = pd.read_excel(file_path, dtype=str)
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

    # Проверяем есть ли группа
    if "Группа" not in df.columns:
        # Может быть с пробелом в конце или lowercase
        for col in df.columns:
            if "группа" in str(col).lower():
                df = df.rename(columns={col: "Группа"})
                break
        else:
            return f"Не нашел колонку 'Группа'. Колонки: {list(df.columns)}"

    # Собираем статистику
    result = defaultdict(lambda: defaultdict(int))

    for _, row in df.iterrows():
        group = row["Группа"]

        # Пропускаем пустые
        if pd.isna(group) or str(group).strip() == "":
            continue

        group = str(group).strip()

        # Ищем предметы в строке
        for cell in row:
            if pd.isna(cell):
                continue

            cell_str = str(cell)
            # Ищем "Предмет:" в любом регистре
            if "предмет:" in cell_str.lower():
                # Вытаскиваем название
                parts = cell_str.split(":", 1)
                if len(parts) > 1:
                    subject = parts[1].strip()
                    if subject:  # Если не пустое
                        result[group][subject] += 1

    # Если ничего не нашли
    if not result:
        return "Не нашёл предметов в файле. Проверь формат - должно быть 'Предмет: Название'"

    # Формируем отчет
    lines = ["ОТЧЕТ ПО РАСПИСАНИЮ", ""]

    # Сортируем группы по названию
    for group in sorted(result.keys()):
        lines.append(f"Группа: {group}")

        # Предметы сортируем по количеству пар (больше - выше)
        subjects = result[group]
        for subject, count in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  • {subject} — {count} пар")

        lines.append("")  # Пустая строка между группами

    return "\n".join(lines)