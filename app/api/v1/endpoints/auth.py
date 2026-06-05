from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.auth import create_access_token

from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🚀 REGISTER (PUBLIC)
@router.post("/register")
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    user = create_user(db, data, user_id=None)

    if user == "exists":
        raise HTTPException(status_code=409, detail="User already exists")

    if user == "deleted":
        raise HTTPException(
            status_code=409,
            detail="User deleted. Restore instead."
        )

    return user


# 🔐 LOGIN (PUBLIC)
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }