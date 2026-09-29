from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest
from ..auth import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

router = APIRouter(prefix="", tags=["authentication"])

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "An account with this email already exists")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    return {"message": "Registration successful", "access_token": token, "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    token = create_access_token(user.id)
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return {"message": "Login successful", "access_token": token, "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"logged_in": True, "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.get("/session-data")
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from ..models import RecommendationHistory
    count = db.query(RecommendationHistory).filter_by(user_id=user.id).count()
    return {"user_id": user.id, "recommendation_count": count}
