import json
import csv
from datetime import datetime


class ExportService:

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    # -----------------------
    # JSON EXPORT
    # -----------------------
    def export_json(self, data: dict, name="leads"):
        filename = f"{name}_{self._timestamp()}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filename

    # -----------------------
    # CSV EXPORT (EXCEL FRIENDLY)
    # -----------------------
    def export_csv(self, leads: list, name="leads"):
        filename = f"{name}_{self._timestamp()}.csv"

        if not leads:
            return filename

        keys = leads[0].keys()

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(leads)

        return filename

    # -----------------------
    # FULL EXPORT (STRONG + WEAK)
    # -----------------------
    def export_full(self, strong: list, weak: list, name="leads"):
        strong_file = self.export_csv(strong, name + "_STRONG")
        weak_file = self.export_csv(weak, name + "_WEAK")

        return {
            "strong_file": strong_file,
            "weak_file": weak_file
        }
