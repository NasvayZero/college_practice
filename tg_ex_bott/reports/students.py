import pandas as pd

def report_students(file_path: str) -> str:
    df = pd.read_excel(file_path)

    # Проверяем нужные столбцы
    required_cols = ["FIO", "Homework", "Classroom"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        return f"В файле не найдены столбцы: {', '.join(missing)}"

    # Фильтруем
    filtered = df[
        (df["Homework"] == 1) |
        (df["Classroom"] < 3)
    ]

    if filtered.empty:
        return "Нет студентов, соответствующих критериям"

    lines = ["Отчет по студентам с низкими оценками:"]
    for _, row in filtered.iterrows():
        lines.append(f"- {row['FIO']}: ДЗ ср.={row['Homework']}, Классная={row['Classroom']}")

    return "\n".join(lines)