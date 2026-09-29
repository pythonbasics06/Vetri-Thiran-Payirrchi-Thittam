from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class HomeItem(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    quantity: int = Field(ge=1, le=100)
    notes: str = Field(default="", max_length=300)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1, max_length=10)
    style: str = Field(default="modern", max_length=80)
    location: str = Field(default="India", max_length=100)
    items: list[HomeItem] = Field(min_length=1, max_length=30)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(ge=1, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="home", max_length=120)
    city: str = Field(default="Chennai", max_length=100)
    preferences: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="elegant", max_length=100)
    outfit_color: str = Field(default="", max_length=100)
    material: str = Field(default="any", max_length=100)
    notes: str = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: float
    reason: str
    url: str
    quantity: int = 1

class Allocation(BaseModel):
    category: str
    amount: float
    percentage: float

class RecommendationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    planner: Literal["home", "party", "jewelry"]
    title: str
    summary: str
    budget: float
    estimated_total: float
    remaining_budget: float
    allocations: list[Allocation]
    recommendations: list[RecommendationItem]
    tips: list[str]
    source_mode: str = "fallback"
