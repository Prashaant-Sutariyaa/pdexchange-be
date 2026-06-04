import csv
import os


# ============================================================
# 🔹 READ CSV
# ============================================================

def read_csv_file(file_path: str):

    with open(
        file_path,
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


# ============================================================
# 🔹 WRITE INVALID CSV
# ============================================================

def write_invalid_csv(
    rows: list,
    output_path: str,
):

    if not rows:
        return

    headers = list(rows[0].keys())

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    with open(
        output_path,
        mode="w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=headers,
        )

        writer.writeheader()

        writer.writerows(rows)