from pprint import pprint
import csv
import re
from collections import defaultdict

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

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
for row in contacts_list:
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

pprint(final_records)

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_records)