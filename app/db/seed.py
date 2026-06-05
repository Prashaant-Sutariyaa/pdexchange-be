from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from sqlalchemy import func

from app.models.role import Role
from app.models.app_settings import AppSetting  # ✅ ADD


def seed_data():
    db: Session = SessionLocal()

    try:
        # 🔹 Roles
        if db.query(Role).count() == 0:
            roles = ["Executive", "Team Lead", "Head"]

            for name in roles:
                db.add(Role(name=name, is_active=True, created_by=1, updated_by=1))

            print("✅ Roles seeded")

        # 🔹 App Settings (🔥 ADD HERE)
        if db.query(AppSetting).count() == 0:
            settings = [
                {
                    "key": "app_name",
                    "value": "ProspectVine CRM",
                    "description": "Main application name",
                },
                {
                    "key": "footer_text",
                    "value": "ProspectVine CRM",
                    "description": "Footer short text",
                },
                {
                    "key": "developed_by_text",
                    "value": "Designed & Developed by ProspectVine",
                    "description": "Developer credit",
                },
                {
                    "key": "copyright_text",
                    "value": "Copyright © 2026 ProspectVine Pvt. Ltd. — ProspectVine CRM. All rights reserved.",
                    "description": "Legal text",
                },
                {"key": "app_version", "value": "v1.0.0", "description": "Version"},
                {
                    "key": "support_email",
                    "value": "support@prospectvine.com",
                    "description": "Support email",
                },
            ]

            for setting in settings:
                db.add(
                    AppSetting(
                        key=setting["key"].lower(),
                        value=setting["value"],
                        description=setting["description"],
                        is_active=True,
                        created_by=1,
                        updated_by=1,
                    )
                )

            print("✅ App settings seeded")

        db.commit()

    finally:
        db.close()
