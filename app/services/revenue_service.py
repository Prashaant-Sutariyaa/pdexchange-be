from sqlalchemy import text
from typing import Optional
import csv
import io
from datetime import datetime

# ============================================================
# 🔹 BUILD COMMON FILTER QUERY
# ============================================================


def build_revenue_filters(
    base_query: str,
    params: dict,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
):

    # ============================================================
    # 🔥 STATUS FILTER
    # ============================================================
    if status and status.lower() != "all":
        base_query += " AND segment_status = :status"
        params["status"] = status

    # ============================================================
    # 🔥 MULTIPLE CLIENT FILTER
    # ============================================================
    if client_id:

        client_ids = [int(c.strip()) for c in client_id.split(",") if c.strip()]

        if client_ids:

            conditions = []

            for i, cid in enumerate(client_ids):

                key = f"client_id_{i}"

                conditions.append(f"client_id = :{key}")

                params[key] = cid

            base_query += " AND (" + " OR ".join(conditions) + ")"

    # ============================================================
    # 🔥 MONTH/YEAR FILTER USING segment_start_date
    # ============================================================
    if from_date and to_date:

        try:

            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
            to_dt = datetime.strptime(to_date, "%Y-%m-%d")

            from_month = from_dt.month
            from_year = from_dt.year

            to_month = to_dt.month
            to_year = to_dt.year

            base_query += """
                AND (
                    DATE_TRUNC('month', segment_start_date)
                    BETWEEN
                    DATE_TRUNC('month', CAST(:from_date AS DATE))
                    AND
                    DATE_TRUNC('month', CAST(:to_date AS DATE))
                )
            """

            params["from_date"] = f"{from_year}-{from_month:02d}-01"
            params["to_date"] = f"{to_year}-{to_month:02d}-01"

        except ValueError:
            pass

    return base_query, params


# ============================================================
# 🔹 GET REVENUE
# ============================================================


def get_revenue(
    db,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
    page: int = 1,
    limit: int = 20,
):

    base_query = """
        FROM revenue_view
        WHERE 1=1
    """

    params = {}

    base_query, params = build_revenue_filters(
        base_query,
        params,
        status,
        client_id,
        from_date,
        to_date,
    )

    offset = (page - 1) * limit

    data_query = f"""
        SELECT *
        {base_query}
        ORDER BY segment_start_date DESC, segment_id DESC
        LIMIT :limit OFFSET :offset
    """

    params["limit"] = limit
    params["offset"] = offset

    result = db.execute(text(data_query), params)
    rows = result.fetchall()

    data = [dict(row._mapping) for row in rows]

    count_query = f"""
        SELECT COUNT(*)
        {base_query}
    """

    total = db.execute(text(count_query), params).scalar()

    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total,
    }


# ============================================================
# 🔹 DOWNLOAD REVENUE CSV
# ============================================================


def download_revenue_csv(
    db,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
):

    base_query = """
        SELECT
            campaign_code,
            segment_code,
            segment_title,
            segment_start_date,
            segment_end_date,
            allocation,
            accepted,
            segment_status,
            allocation_revenue,
            accepted_revenue,
            deficit,
            unrealized,
            deficit_revenue,
            unrealized_revenue
        FROM revenue_view
        WHERE 1=1
    """

    params = {}

    base_query, params = build_revenue_filters(
        base_query,
        params,
        status,
        client_id,
        from_date,
        to_date,
    )

    base_query += """
        ORDER BY segment_start_date DESC, segment_id DESC
    """

    result = db.execute(text(base_query), params)
    rows = result.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    if rows:

        writer.writerow(rows[0]._mapping.keys())

        for row in rows:
            writer.writerow(row._mapping.values())

    output.seek(0)

    return output


# ============================================================
# 🔹 REVENUE SUMMARY
# ============================================================


def get_revenue_summary(
    db,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
    order: str = "asc",
):

    base_query = """
        FROM revenue_view
        WHERE 1=1
    """

    params = {}

    base_query, params = build_revenue_filters(
        base_query,
        params,
        status,
        client_id,
        from_date,
        to_date,
    )
    order_direction = "ASC"

    if order and order.lower() == "desc":
        order_direction = "DESC"

    query = f"""
        SELECT

            TO_CHAR(segment_start_date, 'FMMonth-YYYY') AS month,

            SUM(allocation) AS booked_leads,

            SUM(accepted) AS accepted_leads,

            SUM(allocation - (accepted + unrealized)) AS deficit_leads,

            SUM(unrealized) AS unrealized,

            SUM(allocation_revenue) AS booked_revenue,

            SUM(accepted_revenue) AS accepted_revenue,

            SUM(deficit_revenue) AS revenue_pending,

            SUM(unrealized_revenue) AS unrealized_revenue

        {base_query}

        GROUP BY
            EXTRACT(YEAR FROM segment_start_date),
            EXTRACT(MONTH FROM segment_start_date),
            month

    ORDER BY
        EXTRACT(YEAR FROM segment_start_date) {order_direction},
        EXTRACT(MONTH FROM segment_start_date) {order_direction}
    """

    result = db.execute(text(query), params)
    rows = result.fetchall()

    summary = []

    for row in rows:

        r = dict(row._mapping)

        allocation = r["booked_leads"] or 0
        accepted = r["accepted_leads"] or 0
        deficit = r["deficit_leads"] or 0
        unrealized = r["unrealized"] or 0

        if allocation > 0:

            accepted_pct = round((accepted / allocation) * 100)

            deficit_pct = round((deficit / allocation) * 100)

            unrealized_pct = round((unrealized / allocation) * 100)

        else:

            accepted_pct = 0
            deficit_pct = 0
            unrealized_pct = 0

        summary.append(
            {
                "month": r["month"],
                "booked_leads": allocation,
                "accepted_leads": {"value": accepted, "percentage": f"{accepted_pct}%"},
                "deficit_leads": {"value": deficit, "percentage": f"{deficit_pct}%"},
                "unrealized": {"value": unrealized, "percentage": f"{unrealized_pct}%"},
                "booked_revenue": float(r["booked_revenue"] or 0),
                "accepted_revenue": float(r["accepted_revenue"] or 0),
                "revenue_pending": float(r["revenue_pending"] or 0),
                "unrealized_revenue": float(r["unrealized_revenue"] or 0),
            }
        )

    return summary


# ============================================================
# 🔹 DOWNLOAD SUMMARY CSV
# ============================================================


def download_revenue_summary_csv(
    db,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
):

    data = get_revenue_summary(
        db,
        status,
        client_id,
        from_date,
        to_date,
    )

    output = io.StringIO()
    writer = csv.writer(output)

    if data:

        writer.writerow(
            [
                "Month",
                "Booked Leads",
                "Accepted Leads",
                "Deficit Leads",
                "Unrealized",
                "Booked Revenue",
                "Accepted Revenue",
                "Revenue Pending",
                "Unrealized Revenue",
            ]
        )

        for row in data:

            writer.writerow(
                [
                    row["month"],
                    row["booked_leads"],
                    f'{row["accepted_leads"]["value"]} ({row["accepted_leads"]["percentage"]})',
                    f'{row["deficit_leads"]["value"]} ({row["deficit_leads"]["percentage"]})',
                    f'{row["unrealized"]["value"]} ({row["unrealized"]["percentage"]})',
                    row["booked_revenue"],
                    row["accepted_revenue"],
                    row["revenue_pending"],
                    row["unrealized_revenue"],
                ]
            )

    output.seek(0)

    return output


# ============================================================
# 🔹 REVENUE STATS
# ============================================================


def get_revenue_stats(
    db,
    status: str = None,
    client_id: Optional[str] = None,
    from_date: str = None,
    to_date: str = None,
):

    base_query = """
        FROM revenue_view
        WHERE 1=1
    """

    params = {}

    base_query, params = build_revenue_filters(
        base_query,
        params,
        status,
        client_id,
        from_date,
        to_date,
    )

    query = f"""
        SELECT

            COALESCE(SUM(allocation), 0) AS booked_leads,

            COALESCE(SUM(accepted), 0) AS accepted_leads,

            COALESCE(SUM(allocation - (accepted+unrealized)), 0) AS deficit_leads,

            COALESCE(SUM(unrealized), 0) AS unrealized,

            COALESCE(SUM(allocation_revenue), 0) AS booked_revenue,

            COALESCE(SUM(accepted_revenue), 0) AS accepted_revenue,

            COALESCE(SUM(deficit_revenue), 0) AS revenue_pending,

            COALESCE(SUM(unrealized_revenue), 0) AS unrealized_revenue

        {base_query}
    """

    result = db.execute(text(query), params)

    row = result.fetchone()

    r = dict(row._mapping)

    allocation = r["booked_leads"] or 0
    accepted = r["accepted_leads"] or 0
    deficit = r["deficit_leads"] or 0
    unrealized = r["unrealized"] or 0

    return {
        "booked_leads": allocation,
        "accepted_leads": accepted,
        "deficit_leads": deficit,
        "unrealized": unrealized,
        "booked_revenue": float(r["booked_revenue"] or 0),
        "accepted_revenue": float(r["accepted_revenue"] or 0),
        "revenue_pending": float(r["revenue_pending"] or 0),
        "unrealized_revenue": float(r["unrealized_revenue"] or 0),
    }
