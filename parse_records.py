import json
import os
import re

PHOTOS_DIR = "photos/Astana/astana_photos"
JSON_PATH = "photos/Astana/astana_photos.json"
OUTPUT_PATH = "photos/Astana/photo_records.json"


def extract_text(raw_text):
    if isinstance(raw_text, list):
        return "".join(t if isinstance(t, str) else t.get("text", "") for t in raw_text)
    return raw_text or ""


def parse_field(text, *field_names):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        clean = line.strip().lstrip("\xa0 -").strip()
        for name in field_names:
            pattern = rf"^\*?{re.escape(name)}\*?\s*:\s*(.*)"
            match = re.match(pattern, clean, re.IGNORECASE)
            if match:
                value = match.group(1).strip().strip("*").replace("\xa0", " ").strip()
                # Подхватываем строки-продолжения (не начинаются с -)
                j = i + 1
                while j < len(lines):
                    next_clean = lines[j].strip().lstrip("\xa0 ")
                    if not next_clean or next_clean.startswith("-"):
                        break
                    value += " " + next_clean.strip().replace("\xa0", " ")
                    j += 1
                return re.sub(r"\s+", " ", value).strip()
    return ""


def parse_record(text):
    return {
        "client": parse_field(text, "клиент"),
        "phone": parse_field(text, "телефон"),
        "work_type": parse_field(text, "тип работы"),
        "product_type": parse_field(text, "тип товара"),
        "cartridge_type": parse_field(text, "тип картриджей", "к замене"),
        "address": parse_field(text, "адрес"),
        "maintenance_cost": parse_field(text, "стоимость обслуживания"),
        "product_cost": parse_field(text, "стоимость товара"),
        "delivery_cost": parse_field(text, "стоимость работы | доставки", "стоимость работы"),
        "comment": parse_field(text, "комментарий"),
        "date": parse_field(text, "дата записи"),
        "link_2gis": parse_field(text, "2гис", "2gis"),
    }


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_photos = set(os.listdir(PHOTOS_DIR))

    records = {}
    skipped_no_file = 0
    skipped_no_data = 0

    for msg in data["messages"]:
        if msg.get("type") != "message" or not msg.get("photo"):
            continue

        filename = os.path.basename(msg["photo"])
        if filename not in existing_photos:
            skipped_no_file += 1
            continue

        text = extract_text(msg.get("text", ""))
        if not text.strip():
            skipped_no_data += 1
            continue

        record = parse_record(text)
        record["raw_text"] = text.strip().replace("\xa0", " ")
        records[filename] = record

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Готово. Записей: {len(records)}")
    print(f"Пропущено (нет файла в папке): {skipped_no_file}")
    print(f"Пропущено (нет текста): {skipped_no_data}")
    print(f"Файл сохранён: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()