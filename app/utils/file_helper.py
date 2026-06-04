import os
import csv
import uuid
import hashlib

from datetime import datetime

# ============================================================
# 🔹 STORAGE PATH
# ============================================================

BASE_DIR = os.getcwd()

SENTINEL_UPLOAD_PATH = os.path.join(
    BASE_DIR,
    "storage",
    "sentinel",
    "uploads",
)


# ============================================================
# 🔹 CREATE DIRECTORY
# ============================================================

os.makedirs(
    SENTINEL_UPLOAD_PATH,
    exist_ok=True,
)


# ============================================================
# 🔹 GENERATE FILE NAME
# ============================================================


def generate_sentinel_file_name(
    department: str,
    original_file_name: str,
):

    extension = original_file_name.split(".")[-1]

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    random_code = uuid.uuid4().hex[:5]

    department = department.lower().replace(" ", "_")

    return f"{timestamp}_{department}_{random_code}.{extension}"


# ============================================================
# 🔹 SHA256 HASH
# ============================================================


def generate_file_hash(file_bytes: bytes):

    sha256 = hashlib.sha256()

    sha256.update(file_bytes)

    return sha256.hexdigest()


# ============================================================
# 🔹 SAVE FILE
# ============================================================


def save_upload_file(
    file_bytes: bytes,
    file_name: str,
):

    file_path = os.path.join(
        SENTINEL_UPLOAD_PATH,
        file_name,
    )

    with open(file_path, "wb") as file:

        file.write(file_bytes)

    return file_path


# ============================================================
# 🔹 VALIDATE CSV
# ============================================================


def validate_csv_file(file_name: str):

    allowed_extensions = ["csv"]

    extension = file_name.split(".")[-1].lower()

    return extension in allowed_extensions
