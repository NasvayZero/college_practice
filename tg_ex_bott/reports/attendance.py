import pandas as pd


def report_attendance(file_path: str) -> str:
    """Отчет по преподом с низкой посещаемостью (<40%)"""

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return f"Файл не читается: {e}"

    # Ищем нужные колонки
    teacher_col = None
    attendance_col = None

    for col in df.columns:
        col_str = str(col).lower()

        if not teacher_col and any(word in col_str for word in ["фио", "преподаватель", "учитель", "teacher"]):
            teacher_col = col

        if not attendance_col and any(word in col_str for word in ["посещаем", "attendance", "средн"]):
            attendance_col = col

    # Если не нашли стандартные названия
    if not teacher_col or not attendance_col:
        # Попробуем взять первую колонку как ФИО, вторую как %
        if len(df.columns) >= 2:
            teacher_col = df.columns[0]
            attendance_col = df.columns[1]
        else:
            return f"Не понял колонки. Есть: {', '.join(df.columns.astype(str))}"

    # Чистим данные по посещаемости
    attendance_clean = []

    for val in df[attendance_col]:
        if pd.isna(val):
            attendance_clean.append(0)
            continue

        val_str = str(val)

        # Убираем %, пробелы, запятые вместо точек
        val_str = val_str.replace("%", "").replace(",", ".").strip()

        try:
            num = float(val_str)
            attendance_clean.append(num)
        except:
            attendance_clean.append(0)  # Если совсем кривое - ставим 0

    df["_attendance_clean"] = attendance_clean

    # Фильтруем (<40%)
    mask = df["_attendance_clean"] < 40
    filtered = df[mask]

    # Если все нормально
    if filtered.empty:
        return "Все преподаватели имеют посещаемость ≥40%"

    # Формируем отчет
    lines = [
        "НИЗКАЯ ПОСЕЩАЕМОСТЬ (<40%):",
        f"Найдено преподавателей: {len(filtered)}",
        ""
    ]

    # Сортируем от худшей посещаемости
    filtered = filtered.sort_values("_attendance_clean")

    for _, row in filtered.iterrows():
        teacher = row[teacher_col]
        # Берем оригинальное значение или очищенное
        original_val = row[attendance_col]
        clean_val = row["_attendance_clean"]

        # Показываем как было в файле, если не совсем сломано
        if pd.isna(original_val):
            display_val = f"{clean_val:.1f}%"
        else:
            display_val = str(original_val).strip()
            if not display_val.endswith("%"):
                display_val = f"{display_val}%"

        lines.append(f"• {teacher}: {display_val}")

    # Добавляем статистику
    lines.append("")
    if len(filtered) > 1:
        worst = filtered.iloc[0]["_attendance_clean"]
        lines.append(f"Самая низкая посещаемость: {worst:.1f}%")

    return "\n".join(lines)