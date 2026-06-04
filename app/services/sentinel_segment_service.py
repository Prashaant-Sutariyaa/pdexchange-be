from sqlalchemy import text
from sqlalchemy.orm import Session


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_sentinel_segment_batches(
    db: Session,
    page: int = 1,
    limit: int = 20,
    search: str = None,
    campaign_search: str = None,
):

    offset = (page - 1) * limit

    params = {
        "limit": limit,
        "offset": offset,
    }

    # ============================================================
    # 🔥 MODULE 2
    # 🔥 CAMPAIGN LEVEL
    # ============================================================
    if campaign_search:

        where_clause = """
            WHERE (
                campaign_code ILIKE :campaign_search
                OR title ILIKE :campaign_search
            )
        """

        params["campaign_search"] = f"%{campaign_search}%"

        # ============================================================
        # 🔹 TOTAL
        # ============================================================
        total_query = text(f"""
            SELECT COUNT(*)
            FROM (
                SELECT
                    campaign_code,
                    MAX(title) AS title

                FROM vw_batch_dashboard_summary

                {where_clause}

                GROUP BY
                    campaign_code

            ) grouped_data
        """)

        total = db.execute(
            total_query,
            params,
        ).scalar()

        # ============================================================
        # 🔹 DATA
        # ============================================================
        query = text(f"""
            SELECT
                campaign_code,

                MAX(title) AS title,

                SUM(total_leads) AS total_leads,

                SUM(dataops_total) AS dataops_total,
                SUM(dataops_valid) AS dataops_valid,
                SUM(dataops_invalid) AS dataops_invalid,

                SUM(email_total) AS email_total,
                SUM(email_pending) AS email_pending,
                SUM(email_valid) AS email_valid,
                SUM(email_invalid) AS email_invalid,

                SUM(quality_total) AS quality_total,
                SUM(quality_pending) AS quality_pending,
                SUM(quality_valid) AS quality_valid,
                SUM(quality_invalid) AS quality_invalid,

                SUM(dbr_total) AS dbr_total,
                SUM(dbr_pending) AS dbr_pending,
                SUM(dbr_valid) AS dbr_valid,
                SUM(dbr_invalid) AS dbr_invalid,

                SUM(vv_total) AS vv_total,
                SUM(vv_pending) AS vv_pending,
                SUM(vv_valid) AS vv_valid,
                SUM(vv_invalid) AS vv_invalid,

                SUM(mis_total) AS mis_total,
                SUM(mis_pending) AS mis_pending,
                SUM(mis_delivered) AS mis_delivered,
                SUM(mis_accepted) AS mis_accepted,
                SUM(mis_client_rejected) AS mis_client_rejected,
                SUM(mis_rtd) AS mis_rtd,
                SUM(mis_internal_rejected) AS mis_internal_rejected

            FROM vw_batch_dashboard_summary

            {where_clause}

            GROUP BY
                campaign_code

            ORDER BY campaign_code DESC

            LIMIT :limit OFFSET :offset
        """)

        result = db.execute(
            query,
            params,
        )

        rows = result.mappings().all()

        return {
            "data": [dict(row) for row in rows],
            "page": page,
            "limit": limit,
            "total": total,
        }

    # ============================================================
    # 🔥 MODULE 1
    # 🔥 EXISTING LOGIC
    # ============================================================

    where_clause = ""

    # ============================================================
    # 🔹 SEARCH
    # ============================================================
    if search:

        where_clause = """
            WHERE (
                campaign_code ILIKE :search
                OR segment_code ILIKE :search
            )
        """

        params["search"] = f"%{search}%"

    # ============================================================
    # 🔹 TOTAL
    # ============================================================
    total_query = text(f"""
        SELECT COUNT(*)
        FROM (
            SELECT
                campaign_code,
                segment_code,
                title

            FROM vw_batch_dashboard_summary

            {where_clause}

            GROUP BY
                campaign_code,
                segment_code,
                title

        ) grouped_data
    """)

    total = db.execute(
        total_query,
        params,
    ).scalar()

    # ============================================================
    # 🔹 DATA
    # ============================================================
    query = text(f"""
        SELECT
            campaign_code,
            segment_code,
            title,

            SUM(total_leads) AS total_leads,

            SUM(dataops_total) AS dataops_total,
            SUM(dataops_valid) AS dataops_valid,
            SUM(dataops_invalid) AS dataops_invalid,

            SUM(email_total) AS email_total,
            SUM(email_pending) AS email_pending,
            SUM(email_valid) AS email_valid,
            SUM(email_invalid) AS email_invalid,

            SUM(quality_total) AS quality_total,
            SUM(quality_pending) AS quality_pending,
            SUM(quality_valid) AS quality_valid,
            SUM(quality_invalid) AS quality_invalid,

            SUM(dbr_total) AS dbr_total,
            SUM(dbr_pending) AS dbr_pending,
            SUM(dbr_valid) AS dbr_valid,
            SUM(dbr_invalid) AS dbr_invalid,

            SUM(vv_total) AS vv_total,
            SUM(vv_pending) AS vv_pending,
            SUM(vv_valid) AS vv_valid,
            SUM(vv_invalid) AS vv_invalid,

            SUM(mis_total) AS mis_total,
            SUM(mis_pending) AS mis_pending,
            SUM(mis_delivered) AS mis_delivered,
            SUM(mis_accepted) AS mis_accepted,
            SUM(mis_client_rejected) AS mis_client_rejected,
            SUM(mis_rtd) AS mis_rtd,
            SUM(mis_internal_rejected) AS mis_internal_rejected

        FROM vw_batch_dashboard_summary

        {where_clause}

        GROUP BY
            campaign_code,
            segment_code,
            title

        ORDER BY segment_code DESC

        LIMIT :limit OFFSET :offset
    """)

    result = db.execute(
        query,
        params,
    )

    rows = result.mappings().all()

    return {
        "data": [dict(row) for row in rows],
        "page": page,
        "limit": limit,
        "total": total,
    }


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_sentinel_batch(
    db: Session,
    batch_code: str,
):

    query = text("""
        SELECT *
        FROM vw_batch_dashboard_summary
        WHERE batch_code = :batch_code
        LIMIT 1
    """)

    result = db.execute(
        query,
        {
            "batch_code": batch_code,
        },
    )

    row = result.mappings().first()

    if not row:
        return None

    return dict(row)


# ============================================================
# 🔹 GET BY SEGMENT CODE
# ============================================================
def get_sentinel_batches_by_segment_code(
    db: Session,
    segment_code: str,
    page: int = 1,
    limit: int = 20,
):

    offset = (page - 1) * limit

    params = {
        "segment_code": segment_code,
        "limit": limit,
        "offset": offset,
    }

    # ============================================================
    # 🔹 TOTAL
    # ============================================================
    total_query = text("""
        SELECT COUNT(*)
        FROM vw_batch_dashboard_summary
        WHERE segment_code = :segment_code
    """)

    total = db.execute(
        total_query,
        params,
    ).scalar()

    # ============================================================
    # 🔹 DATA
    # ============================================================
    query = text("""
        SELECT *
        FROM vw_batch_dashboard_summary
        WHERE segment_code = :segment_code
        ORDER BY batch_code DESC
        LIMIT :limit OFFSET :offset
    """)

    result = db.execute(
        query,
        params,
    )

    rows = result.mappings().all()

    return {
        "data": [dict(row) for row in rows],
        "page": page,
        "limit": limit,
        "total": total,
    }
