import json
import os

MAPPINGS_FILE = "mappings.json"


def load_mappings():

    if not os.path.exists(MAPPINGS_FILE):
        return {"mappings": []}

    with open(MAPPINGS_FILE, "r") as f:
        return json.load(f)


# ============================================================
# 🔹 SAVE JSON
# ============================================================
def save_mappings(data):

    with open(MAPPINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
