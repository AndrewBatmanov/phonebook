import csv
import re
import requests

from io import StringIO
from pprint import pprint
from collections import defaultdict

url = "https://data.nalog.ru/opendata/7707329152-regoffice/data-03012016-structure-11192014.csv"

response = requests.get(url)
response.raise_for_status()

file_like_object = StringIO(response.text)
# Обратите внимание на разделитель ';'
csv_reader = csv.reader(file_like_object, delimiter=';')

all_rows = list(csv_reader)


def format_phone(phone):
    if not phone:
        return ""

    digits = re.sub(r'\D', '', phone)

    if len(digits) == 11:
        formatted = re.sub(
            r'^(\d)(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', digits)
    elif len(digits) > 11:
        main_part = digits[:11]
        extension = digits[11:]
        formatted_main = re.sub(
            r'^(\d)(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', main_part)
        formatted = f"{formatted_main} доб.{extension}"
    else:
        formatted = phone

    return formatted


processed_rows = []
for row in all_rows:
    if len(row) < 7:
        continue

    processed_row = row.copy()

    # ЗАДАЧА 1: Обработка ФИО
    fio_str = " ".join(processed_row[:3])
    fio_parts = fio_str.split()

    if len(fio_parts) >= 1:
        processed_row[0] = fio_parts[0]
    if len(fio_parts) >= 2:
        processed_row[1] = fio_parts[1]
    if len(fio_parts) >= 3:
        processed_row[2] = " ".join(fio_parts[2:])

    # ЗАДАЧА 2: Форматирование телефона
    if len(processed_row) > 5:
        processed_row[5] = format_phone(processed_row[5])

    processed_rows.append(processed_row)

# ЗАДАЧА 3: Объединение дублирующихся людей
grouped_records = defaultdict(list)

for record in processed_rows:
    key = (record[0], record[1])
    grouped_records[key].append(record)

final_records = []
for key, records in grouped_records.items():
    if len(records) == 1:
        final_records.append(records[0])
    else:
        merged_record = records[0].copy()

        for other_record in records[1:]:
            for i in range(len(merged_record)):
                if not merged_record[i] and other_record[i]:
                    merged_record[i] = other_record[i]

        final_records.append(merged_record)

print("\nПервые 10 записей:")
for i, record in enumerate(final_records[1:11]):
    pprint(f"{i + 1}. {record}")

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=';')
    datawriter.writerows(final_records)