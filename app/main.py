from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import validation_exception_handler

from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_data
from app.api.v1.endpoints import (
    auth,
    campaign,
    campaign_segment,
    user,
    role,
    vendor,
)
from app.api.v1.endpoints import module_permission
from app.api.v1.endpoints import role_permission
from app.api.v1.endpoints import user_permission
from app.api.v1.endpoints import app_settings
from app.api.v1.endpoints import client
from app.api.v1.endpoints import user_access
from app.api.v1.endpoints import currency_rate
from app.api.v1.endpoints import revenue
from app.api.v1.endpoints.sync import router as sync_router

app = FastAPI(title="CRM Backend", root_path="/api")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔥 STARTUP
# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)  # ✅ create tables
#     seed_data()  # ✅ seed default data


# 🔗 ROUTES
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(user_access.router)
app.include_router(role.router)
app.include_router(module_permission.router)
app.include_router(role_permission.router)
app.include_router(user_permission.router)
app.include_router(app_settings.router)
app.include_router(client.router)
app.include_router(vendor.router)
app.include_router(campaign.router)
app.include_router(campaign_segment.router)
app.include_router(currency_rate.router)
app.include_router(revenue.router)
app.include_router(sync_router)
