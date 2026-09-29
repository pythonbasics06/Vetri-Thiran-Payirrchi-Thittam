import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, RecommendationHistory
from ..dependencies import optional_user
from ..schemas import HomeRequest, PartyRequest, JewelryRequest
from ..services.gemini_service import GeminiService
from ..config import settings

router = APIRouter(tags=["planners"])
gemini = GeminiService()

def save_history(db: Session, user: User | None, planner: str, request_data: dict, response_data: dict):
    if not user:
        return
    record = RecommendationHistory(
        user_id=user.id,
        planner=planner,
        request_json=json.dumps(request_data, ensure_ascii=False),
        response_json=json.dumps(response_data, ensure_ascii=False),
    )
    db.add(record)
    db.commit()

@router.post("/generate-home")
def generate_home(payload: HomeRequest, db: Session = Depends(get_db), user: User | None = Depends(optional_user)):
    result = gemini.generate("home", payload.model_dump())
    save_history(db, user, "home", payload.model_dump(), result)
    return result

@router.post("/generate-party")
def generate_party(payload: PartyRequest, db: Session = Depends(get_db), user: User | None = Depends(optional_user)):
    result = gemini.generate("party", payload.model_dump())
    save_history(db, user, "party", payload.model_dump(), result)
    return result

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    outfit_color: str = Form(""),
    material: str = Form("any"),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User | None = Depends(optional_user),
):
    if budget <= 0 or budget > 10_000_000:
        raise HTTPException(422, "Budget must be between 0 and 10,000,000")
    data = {
        "budget": budget, "occasion": occasion.strip(), "style": style.strip(),
        "outfit_color": outfit_color.strip(), "material": material.strip(),
        "notes": notes.strip(),
    }
    image_bytes = None
    mime = None
    if outfit_image and outfit_image.filename:
        mime = outfit_image.content_type or ""
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(400, "Only JPG, PNG, and WEBP images are allowed")
        image_bytes = await outfit_image.read()
        if len(image_bytes) > settings.max_upload_bytes:
            raise HTTPException(413, f"Image must be <= {settings.max_upload_mb} MB")
    result = gemini.generate("jewelry", data, image_bytes, mime)
    save_history(db, user, "jewelry", data, result)
    return result

@router.get("/recommendations-details")
def recommendations_details():
    return {
        "message": "Planner responses are returned directly by /generate-home, /generate-party and /generate-jewelry.",
        "supported_planners": ["home", "party", "jewelry"]
    }
