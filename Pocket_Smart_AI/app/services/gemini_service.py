import base64
import json
import re
from typing import Any
from google import genai
from google.genai import types
from .recommendation_service import build_fallback
from ..config import settings

class GeminiService:
    def __init__(self):
        self.enabled = bool(settings.gemini_api_key.strip())
        self.client = genai.Client(api_key=settings.gemini_api_key) if self.enabled else None

    def _prompt(self, planner: str, data: dict[str, Any]) -> str:
        return f'''
You are PocketSmart AI, a careful budget recommendation assistant.
Planner: {planner}
User input JSON:
{json.dumps(data, ensure_ascii=False, indent=2)}

Return ONLY valid JSON with this exact top-level structure:
{{
  "planner": "{planner}",
  "title": "short title",
  "summary": "2 sentence summary",
  "budget": number,
  "estimated_total": number,
  "remaining_budget": number,
  "allocations": [
    {{"category":"string","amount":number,"percentage":number}}
  ],
  "recommendations": [
    {{
      "name":"string",
      "category":"string",
      "platform":"Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO|Other",
      "estimated_price": number,
      "quantity": 1,
      "reason":"string",
      "url":"string"
    }}
  ],
  "tips":["string"]
}}
Rules:
- Stay within the supplied budget. estimated_total must not exceed budget.
- Give 4 to 8 recommendations.
- Use Indian rupees.
- Do not invent exact live inventory, ratings, reviews, stock status, or exact product URLs.
- For platform URLs, use search/landing URLs if exact product URLs are not known.
- Make the recommendations actionable and explain trade-offs.
- Never claim that you actually queried Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO.
'''

    def _extract_json(self, text: str) -> dict[str, Any]:
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end < start:
            raise ValueError("Gemini did not return a JSON object")
        return json.loads(text[start:end+1])

    def generate(self, planner: str, data: dict[str, Any], image_bytes: bytes | None = None, mime_type: str | None = None) -> dict[str, Any]:
        fallback = build_fallback(planner, data)
        if not self.enabled:
            return fallback

        contents: list[Any] = [self._prompt(planner, data)]
        if image_bytes and mime_type:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

        try:
            response = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.35,
                    max_output_tokens=5000,
                    response_mime_type="application/json",
                ),
            )
            result = self._extract_json(response.text or "")
            result = self._normalize(result, planner, data, fallback)
            result["source_mode"] = "gemini"
            return result
        except Exception:
            return fallback

    def _normalize(self, result: dict[str, Any], planner: str, data: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
        result["planner"] = planner
        result["budget"] = float(data["budget"])
        recs = result.get("recommendations") or []
        if not isinstance(recs, list):
            return fallback

        clean = []
        for item in recs[:8]:
            try:
                price = max(0, float(item.get("estimated_price", 0)))
                qty = max(1, int(item.get("quantity", 1)))
            except (TypeError, ValueError):
                continue
            item["estimated_price"] = round(price, 2)
            item["quantity"] = qty
            item["name"] = str(item.get("name", "Recommended option"))
            item["category"] = str(item.get("category", "General"))
            item["platform"] = str(item.get("platform", "Other"))
            item["reason"] = str(item.get("reason", "Fits the requested budget and preferences."))
            item["url"] = str(item.get("url", ""))
            clean.append(item)

        if not clean:
            return fallback

        total = round(sum(x["estimated_price"] * x["quantity"] for x in clean), 2)
        if total > float(data["budget"]):
            return fallback

        result["recommendations"] = clean
        result["estimated_total"] = total
        result["remaining_budget"] = round(float(data["budget"]) - total, 2)
        if not result.get("allocations"):
            result["allocations"] = fallback["allocations"]
        if not result.get("tips"):
            result["tips"] = fallback["tips"]
        result["title"] = str(result.get("title", fallback["title"]))
        result["summary"] = str(result.get("summary", fallback["summary"]))
        return result
