import string

# ============================================================
# 🔹 BASE36 CHARACTERS
# ============================================================

BASE36_CHARS = string.digits + string.ascii_uppercase


# ============================================================
# 🔹 INT TO BASE36
# ============================================================


def int_to_base36(
    number: int,
):

    if number < 0:
        raise ValueError("number must be positive")

    if number == 0:
        return "0"

    result = ""

    while number:

        number, remainder = divmod(
            number,
            36,
        )

        result = BASE36_CHARS[remainder] + result

    return result


# ============================================================
# 🔹 GENERATE BATCH CODE
# ============================================================


def generate_batch_code(
    batch_id: int,
):

    base36 = int_to_base36(batch_id)

    return base36.zfill(6)
