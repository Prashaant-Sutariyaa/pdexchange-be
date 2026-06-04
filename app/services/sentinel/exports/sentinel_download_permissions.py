# ============================================================
# 🔹 DOWNLOAD PERMISSIONS
# ============================================================

DOWNLOAD_PERMISSIONS = {

    "dataops": {

        "dataops.total",
        "dataops.valid",
        "dataops.invalid",

        "email.total",
        "email.pending",
        "email.valid",
        "email.invalid",

        "quality.total",
        "quality.pending",
        "quality.valid",
        "quality.invalid",

        "dbr.total",
        "dbr.pending",
        "dbr.valid",
        "dbr.invalid",

        "vv.total",
        "vv.pending",
        "vv.valid",

        "mis.total",
        "mis.pending",
        "mis.delivered",
        "mis.accepted",
        "mis.client_rejected",
        "mis.rtd",
        "mis.internal_rejected",
    },

    "email": {

        "dataops.valid",

        "email.total",
        "email.pending",
        "email.valid",
        "email.invalid",
    },

    "quality": {

        "email.valid",

        "quality.total",
        "quality.pending",
        "quality.valid",
        "quality.invalid",
    },

    "dbr": {

        "quality.valid",

        "dbr.total",
        "dbr.pending",
        "dbr.valid",
        "dbr.invalid",
    },

    "vv": {

        "quality.valid",

        "dbr.valid",

        "vv.total",
        "vv.pending",
        "vv.valid",
    },

    "mis": {

        "quality.total",
        "quality.pending",
        "quality.valid",
        "quality.invalid",

        "dbr.total",
        "dbr.pending",
        "dbr.valid",
        "dbr.invalid",

        "vv.total",
        "vv.pending",
        "vv.valid",

        "mis.total",
        "mis.pending",
        "mis.delivered",
        "mis.accepted",
        "mis.client_rejected",
        "mis.rtd",
        "mis.internal_rejected",
    },

    "management": {

        "*",
    },
    "technology": {

        "*",
    },
}


# ============================================================
# 🔹 BUILD PERMISSION KEY
# ============================================================

def build_permission_key(
    department: str,
    metric: str,
):

    return (
        f"{department.lower()}."
        f"{metric.lower()}"
    )


# ============================================================
# 🔹 HAS DOWNLOAD PERMISSION
# ============================================================

def has_download_permission(
    user_department: str,
    department: str,
    metric: str,
):

    user_department = (
        user_department
        .strip()
        .lower()
    )

    permissions = DOWNLOAD_PERMISSIONS.get(
        user_department,
        set(),
    )

    # ========================================================
    # 🔹 MANAGEMENT FULL ACCESS
    # ========================================================

    if "*" in permissions:
        return True

    permission_key = build_permission_key(
        department,
        metric,
    )

    return permission_key in permissions