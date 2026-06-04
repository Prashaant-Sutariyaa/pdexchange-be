import traceback
from collections import defaultdict
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.sentinel_job import SentinelJob
from app.models.sentinel_activity_log import (
    SentinelActivityLog,
)
from app.models.campaign_segment_batch import (
    CampaignSegmentBatch,
)
from app.services.sentinel.jobs.sentinel_job_service import (
    mark_job_running,
    mark_job_completed,
    mark_job_failed,
)
from app.services.sentinel.jobs.sentinel_csv_service import (
    process_csv_file,
)
from app.services.emails.sentinel_notification_email_service import (
    send_sentinel_job_completed_email,
)
from app.services.sentinel.utils.sentinel_department_router import (
    process_department_row,
)
from app.services.sentinel.validators.validation_cache_builder import (
    ValidationCacheBuilder,
)
from app.services.sentinel.validators.validation_service import (
    ValidationService,
)
import logging
import os
from app.utils.csv_helper import (
    write_invalid_csv,
)

logger = logging.getLogger(__name__)

# ============================================================
# 🔹 PROCESS JOB
# ============================================================


async def process_job(job_id: int):

    db: Session = SessionLocal()
    try:

        # ====================================================
        # 🔹 JOB
        # ====================================================

        job = db.query(SentinelJob).filter(SentinelJob.id == job_id).first()

        if not job:
            return

        mark_job_running(
            db,
            job,
        )

        # ====================================================
        # 🔹 PROCESS CSV
        # ====================================================

        result = process_csv_file(
            file_path=job.file_path,
            department=job.department,
        )
        failed_rows = result["invalid_data"]

        valid_rows = result["valid_data"]

        validation_cache = ValidationCacheBuilder.build(
            db=db,
            department=job.department,
            campaign_code=job.campaign_codes,
        )
        if not valid_rows:

            mark_job_failed(
                db,
                job,
                "No valid rows found in uploaded CSV",
            )

            return

        # ====================================================
        # 🔹 DATAOPS FLOW
        # ====================================================

        if job.department.lower() == "dataops":

            from app.utils.base36 import (
                generate_batch_code,
            )

            temp_batch = CampaignSegmentBatch(
                campaign_code=job.campaign_codes,
                segment_code=job.segment_codes,
                priority="medium",
                status="In Process",
                created_at=datetime.utcnow(),
                created_by=job.created_by,
            )

            db.add(temp_batch)

            db.flush()

            batch_code = generate_batch_code(temp_batch.id)

            temp_batch.batch_code = batch_code

            db.commit()

            db.refresh(temp_batch)

            # ================================================
            # 🔹 ATTACH BATCH CODE TO ALL ROWS
            # ================================================

            for row in valid_rows:

                row["batch_code"] = batch_code

            # ================================================
            # 🔹 PROCESS ROWS
            # ================================================

            valid_count = 0
            invalid_count = 0

            for row in valid_rows:

                try:

                    validation_result = ValidationService.validate_row(
                        db=db,
                        department=job.department,
                        row=row,
                        cache=validation_cache,
                    )

                    if not validation_result.is_valid:

                        row["system_status"] = "Invalid"

                        failed_rows.append(
                            {
                                **row,
                                "failure_reason": validation_result.reason,
                            }
                        )
                        logger.warning(
                            "Sentinel validation failed",
                            extra={
                                "job_id": job.id,
                                "department": job.department,
                                "reason": validation_result.reason,
                                "batch_code": row.get("batch_code"),
                                "email": row.get("email"),
                            },
                        )

                        invalid_count += 1

                        continue

                    row = validation_result.normalized_row

                    process_department_row(
                        db=db,
                        department=job.department,
                        batch_code=batch_code,
                        row=row,
                        user_id=job.created_by,
                    )
                    valid_count += 1

                except Exception as error:

                    db.rollback()

                    # print(
                    #     "UPSERT ERROR:",
                    #     str(error),
                    # )

                    logger.error(
                        "UPSERT ERROR:",
                        str(error),
                    )

                    failed_rows.append(
                        {
                            **row,
                            "failure_reason": str(error),
                        }
                    )

                    invalid_count += 1

            db.commit()

            # ================================================
            # 🔹 UPDATE COUNTERS
            # ================================================

            temp_batch.dataops_total = result["total_rows"]

            temp_batch.dataops_valid = valid_count

            temp_batch.dataops_invalid = invalid_count

            temp_batch.status = "Completed"

            temp_batch.completed_at = datetime.utcnow()

            temp_batch.updated_at = datetime.utcnow()

            temp_batch.updated_by = job.created_by

            # ================================================
            # 🔹 UPDATE JOB
            # ================================================

            job.campaign_codes = temp_batch.campaign_code

            job.segment_codes = temp_batch.segment_code

            job.batch_codes = temp_batch.batch_code

            db.commit()

        # ====================================================
        # 🔹 DOWNSTREAM FLOW
        # ====================================================

        else:

            # ================================================
            # 🔹 GROUP ROWS BY BATCH
            # ================================================

            grouped_rows = defaultdict(list)

            for row in valid_rows:

                batch_code = (row.get("batch_code") or "").strip()

                grouped_rows[batch_code].append(row)

            # ================================================
            # 🔹 PROCESS EACH BATCH
            # ================================================

            total_valid = 0
            total_invalid = 0

            processed_batches = []

            for (
                batch_code,
                batch_rows,
            ) in grouped_rows.items():

                # ============================================
                # 🔹 FETCH BATCH
                # ============================================

                batch = (
                    db.query(CampaignSegmentBatch)
                    .filter(CampaignSegmentBatch.batch_code == batch_code)
                    .first()
                )

                if not batch:

                    print(f"BATCH NOT FOUND: {batch_code}")

                    total_invalid += len(batch_rows)

                    continue

                batch.status = "In Process"

                valid_count = 0
                invalid_count = 0

                # ============================================
                # 🔹 PROCESS BATCH ROWS
                # ============================================

                for row in batch_rows:

                    try:

                        validation_result = ValidationService.validate_row(
                            db=db,
                            department=job.department,
                            row=row,
                            cache=validation_cache,
                        )

                        if not validation_result.is_valid:

                            row["system_status"] = "Invalid"
                            failed_rows.append(
                                {
                                    **row,
                                    "failure_reason": validation_result.reason,
                                }
                            )

                            logger.warning(
                                "Sentinel validation failed",
                                extra={
                                    "job_id": job.id,
                                    "department": job.department,
                                    "reason": validation_result.reason,
                                    "batch_code": row.get("batch_code"),
                                    "email": row.get("email"),
                                },
                            )

                            invalid_count += 1
                            total_invalid += 1

                            continue

                        row = validation_result.normalized_row

                        process_department_row(
                            db=db,
                            department=job.department,
                            batch_code=batch_code,
                            row=row,
                            user_id=job.created_by,
                        )

                        valid_count += 1
                        total_valid += 1

                    except Exception as error:

                        db.rollback()

                        print(
                            "UPSERT ERROR:",
                            str(error),
                        )

                        invalid_count += 1

                        total_invalid += 1

                db.commit()

                # ============================================
                # 🔹 REFRESH BATCH
                # ============================================

                batch = (
                    db.query(CampaignSegmentBatch)
                    .filter(CampaignSegmentBatch.batch_code == batch_code)
                    .first()
                )

                department = job.department.lower()

                # ============================================
                # 🔹 UPDATE COUNTERS
                # ============================================

                if department == "email":

                    batch.email_total = len(batch_rows)

                    batch.email_valid = valid_count

                    batch.email_invalid = invalid_count

                elif department == "quality":

                    batch.quality_total = len(batch_rows)

                    batch.quality_valid = valid_count

                    batch.quality_invalid = invalid_count

                elif department == "dbr":

                    batch.dbr_total = len(batch_rows)

                    batch.dbr_valid = valid_count

                    batch.dbr_invalid = invalid_count

                elif department == "vv" or department == "voice verification":

                    batch.vv_total = len(batch_rows)

                    batch.vv_valid = valid_count

                    batch.vv_invalid = invalid_count

                elif department == "mis":

                    batch.mis_total = len(batch_rows)

                    batch.mis_valid = valid_count

                    batch.mis_invalid = invalid_count

                # ============================================
                # 🔹 COMPLETE BATCH
                # ============================================

                batch.status = "Completed"

                batch.completed_at = datetime.utcnow()

                batch.updated_at = datetime.utcnow()

                batch.updated_by = job.created_by

                processed_batches.append(batch_code)

                db.commit()

            # ================================================
            # 🔹 UPDATE JOB
            # ================================================

            if processed_batches:

                first_batch = (
                    db.query(CampaignSegmentBatch)
                    .filter(CampaignSegmentBatch.batch_code == processed_batches[0])
                    .first()
                )

                if first_batch:

                    job.campaign_codes = first_batch.campaign_code

                    job.segment_codes = first_batch.segment_code

                    job.batch_codes = ",".join(processed_batches)

            db.commit()

        # ====================================================
        # 🔹 FAILED CSV
        # ====================================================

        invalid_file_name = None

        invalid_file_path = None

        if failed_rows:

            os.makedirs(
                "storage/sentinel/failed_upload",
                exist_ok=True,
            )

            invalid_file_name = f"failed_upload_{job.id}.csv"

            invalid_file_path = os.path.join(
                "storage/sentinel/failed_upload",
                invalid_file_name,
            )

            write_invalid_csv(
                failed_rows,
                invalid_file_path,
            )

        # ====================================================
        # 🔹 SEND EMAIL
        # ====================================================

        await send_sentinel_job_completed_email(
            db=db,
            job_id=job.id,
        )

        # ====================================================
        # 🔹 ACTIVITY LOG
        # ====================================================

        activity = SentinelActivityLog(
            user_id=job.created_by,
            user_role=str(job.created_by),
            job_id=job.id,
            department=job.department,
            activity_type="Process_Complete",
            batch_status="Completed",
            campaign_codes=job.campaign_codes,
            segment_codes=job.segment_codes,
            batch_codes=job.batch_codes,
            total_rows=result["total_rows"],
            valid_rows=result["valid_rows"],
            invalid_rows=result["invalid_rows"],
            file_name=job.file_name,
            file_path=job.file_path,
            file_link=job.file_path,
            action_source="API",
            remarks=("Sentinel processing completed"),
            created_at=datetime.utcnow(),
        )

        db.add(activity)

        db.commit()

        # ====================================================
        # 🔹 COMPLETE JOB
        # ====================================================

        mark_job_completed(
            db=db,
            job=job,
            output_file_name=job.file_name,
            output_file_path=job.file_path,
            invalid_file_name=invalid_file_name,
            invalid_file_path=invalid_file_path,
        )

    except Exception as error:

        traceback.print_exc()

        if "job" in locals():

            mark_job_failed(
                db,
                job,
                str(error),
            )

    finally:

        db.close()
