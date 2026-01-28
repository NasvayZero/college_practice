import pandas as pd
from collections import defaultdict


def report_schedule(file_path: str) -> str:
    "подсчёт пар"

    try:
        df = pd.read_excel(file_path, dtype=str)
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

    # Проверка группы
    if "Группа" not in df.columns:
        for col in df.columns:
            if "группа" in str(col).lower():
                df = df.rename(columns={col: "Группа"})
                break
        else:
            return f"Не нашел колонку 'Группа'. Колонки: {list(df.columns)}"

    # статистика
    result = defaultdict(lambda: defaultdict(int))

    for _, row in df.iterrows():
        group = row["Группа"]

        # Пропуск
        if pd.isna(group) or str(group).strip() == "":
            continue

        group = str(group).strip()

        #предметы
        for cell in row:
            if pd.isna(cell):
                continue

            cell_str = str(cell)
            if "предмет:" in cell_str.lower():
                #название
                parts = cell_str.split(":", 1)
                if len(parts) > 1:
                    subject = parts[1].strip()
                    if subject:
                        result[group][subject] += 1

    #ничего не найдено
    if not result:
        return "Не нашёл предметов в файле. Проверь формат - должно быть 'Предмет: Название'"

    #отчет
    lines = ["ОТЧЕТ ПО РАСПИСАНИЮ", ""]

    # сортировка групп по названию
    for group in sorted(result.keys()):
        lines.append(f"Группа: {group}")

        #сортировка по кол-ву пар
        subjects = result[group]
        for subject, count in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  • {subject} — {count} пар")

        lines.append("")

    return "\n".join(lines)