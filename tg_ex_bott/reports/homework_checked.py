import pandas as pd


def report_homework_checked(file_path: str) -> str:

    try:
        df = pd.read_excel(file_path, skiprows=1)
    except Exception as e:
        try:
            df = pd.read_excel(file_path)
            print("Читаю без skiprows=1")  # Для отладки
        except Exception as e2:
            return f"Не могу прочитать файл: {e2}"

    # пустой файл
    if df.empty:
        return "Файл пустой или не содержит данных"

    if len(df.columns) > 1:
        name_col = df.columns[1]
        df = df.dropna(subset=[name_col])
    else:
        return f"Мало колонок в файле: {len(df.columns)}"

    mask = ~df[name_col].astype(str).str.contains("итого|всего|итог|total|sum", case=False, na=False)
    df = df[mask]

    lines = ["ПРОВЕРКА ДОМАШНИХ ЗАДАНИЙ (<70%)"]
    lines.append("=" * 40)
    found = False

    # статистикав
    total_teachers = len(df)
    problem_teachers = 0

    for idx, row in df.iterrows():
        name = str(row[name_col]).strip()
        if not name or name == "nan":
            continue

        # Месяц
        month_received = 0
        month_checked = 0

        if len(df.columns) > 5:
            try:
                month_received_val = row[df.columns[4]]
                month_checked_val = row[df.columns[5]]

                month_received = pd.to_numeric(month_received_val, errors='coerce') or 0
                month_checked = pd.to_numeric(month_checked_val, errors='coerce') or 0
            except:
                pass

        # Неделя
        week_received = 0
        week_checked = 0

        if len(df.columns) > 10:
            try:
                week_received_val = row[df.columns[9]]
                week_checked_val = row[df.columns[10]]

                week_received = pd.to_numeric(week_received_val, errors='coerce') or 0
                week_checked = pd.to_numeric(week_checked_val, errors='coerce') or 0
            except:
                pass

        problems = []

        if month_received > 0:
            month_percent = (month_checked / month_received) * 100
            if month_percent < 70:
                problems.append(f"Месяц: {month_percent:.0f}% ({month_checked}/{month_received})")

        if week_received > 0:
            week_percent = (week_checked / week_received) * 100
            if week_percent < 70:
                problems.append(f"Неделя: {week_percent:.0f}% ({week_checked}/{week_received})")

        if problems:
            found = True
            problem_teachers += 1

            lines.append("")
            lines.append(f"{name}")
            for problem in problems:
                lines.append(f"{problem}")

    # отчёт
    if not found:
        return f"Все преподаватели ({total_teachers} чел.) проверяют ≥70% ДЗ"

    lines.append("")
    lines.append("=" * 40)
    lines.append(f"ИТОГО: {problem_teachers} из {total_teachers} преподавателей")
    lines.append(f"Порог проверки: <70%")

    return "\n".join(lines)