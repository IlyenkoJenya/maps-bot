import json
import os
import random


class DataManager:
    def __init__(self, records_path: str, photos_dir: str):
        self.records_path = records_path
        self.photos_dir = photos_dir

    def _load(self) -> dict:
        with open(self.records_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, records: dict) -> None:
        with open(self.records_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def get_random_record(self) -> tuple[str, dict] | tuple[None, None]:
        records = self._load()
        usable = {
            filename: data
            for filename, data in records.items()
            if os.path.exists(os.path.join(self.photos_dir, filename))
            and (data.get("work_type") or data.get("product_type") or data.get("address"))
        }
        if not usable:
            return None, None

        filename = random.choice(list(usable.keys()))
        return filename, usable[filename]

    def delete_record(self, filename: str) -> None:
        photo_path = os.path.join(self.photos_dir, filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)

        records = self._load()
        records.pop(filename, None)
        self._save(records)

    def remaining_count(self) -> int:
        records = self._load()
        return sum(
            1 for filename, data in records.items()
            if os.path.exists(os.path.join(self.photos_dir, filename))
            and (data.get("work_type") or data.get("product_type") or data.get("address"))
        )