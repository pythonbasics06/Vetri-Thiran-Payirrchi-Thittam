import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User, RecommendationHistory

router = APIRouter(tags=["history"])

@router.get("/history")
def get_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(RecommendationHistory)
        .filter_by(user_id=user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": r.id,
            "planner": r.planner,
            "created_at": r.created_at.isoformat(),
            "request": json.loads(r.request_json),
            "response": json.loads(r.response_json),
        }
        for r in rows
    ]
