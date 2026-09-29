from urllib.parse import quote_plus
from typing import Any

def money(value: float) -> float:
    return round(float(value), 2)

def search_url(platform: str, query: str) -> str:
    q = quote_plus(query)
    urls = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/search?query={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return urls.get(platform, f"https://www.google.com/search?q={q}")

def build_fallback(planner: str, data: dict[str, Any]) -> dict[str, Any]:
    budget = float(data["budget"])
    items = []
    allocations = []

    if planner == "home":
        cats = [("Furniture", .35), ("Lighting", .15), ("Decor", .20), ("Storage", .15), ("Contingency", .15)]
        for name, pct in cats:
            allocations.append({"category": name, "amount": money(budget*pct), "percentage": pct*100})
        base = [
            ("Compact study/storage unit", "Storage", "IKEA", .12),
            ("LED ceiling light", "Lighting", "Amazon", .07),
            ("Decorative wall art", "Decor", "Amazon", .06),
            ("Side table", "Furniture", "Flipkart", .10),
            ("Cushion set", "Decor", "IKEA", .04),
        ]
        for name, cat, platform, pct in base:
            items.append({
                "name": name, "category": cat, "platform": platform,
                "estimated_price": money(budget*pct), "quantity": 1,
                "reason": f"Selected as a practical {data.get('style','modern')} option while keeping the overall plan inside the budget.",
                "url": search_url(platform, name),
            })
        tips = [
            "Measure rooms and doorways before purchasing large furniture.",
            "Keep the contingency allocation for installation, delivery, or price changes.",
            "Compare the final cart total with your allocated category amount before checkout.",
        ]
        title = "Home interior plan"
        summary = f"A balanced {data.get('style','modern')} plan for {', '.join(data.get('rooms', []))}."

    elif planner == "party":
        cats = [("Food & catering", .45), ("Decoration", .15), ("Venue", .20), ("Entertainment", .10), ("Contingency", .10)]
        for name, pct in cats:
            allocations.append({"category": name, "amount": money(budget*pct), "percentage": pct*100})
        base = [
            ("Catering package", "Food & catering", "Swiggy", .38),
            ("Birthday/event decoration", "Decoration", "Amazon", .10),
            ("Local venue search", "Venue", "Zomato", .15),
            ("Guest accommodation", "Venue", "OYO", .05),
            ("Party games and props", "Entertainment", "Flipkart", .07),
        ]
        for name, cat, platform, pct in base:
            items.append({
                "name": name, "category": cat, "platform": platform,
                "estimated_price": money(budget*pct), "quantity": 1,
                "reason": f"Fits a {data.get('event_type','event')} for approximately {data.get('guests',1)} guests.",
                "url": search_url(platform, name),
            })
        tips = [
            f"Confirm per-person catering cost for all {data.get('guests',1)} guests.",
            "Reserve the venue and accommodation before committing to decor vendors.",
            "Keep contingency money untouched until the major bookings are confirmed.",
        ]
        title = "Party budget plan"
        summary = f"A practical {data.get('event_type','event')} plan for about {data.get('guests',1)} guests."

    else:
        cats = [("Necklace", .40), ("Earrings", .20), ("Bracelet/Bangles", .15), ("Optional accessory", .10), ("Contingency", .15)]
        for name, pct in cats:
            allocations.append({"category": name, "amount": money(budget*pct), "percentage": pct*100})
        base = [
            ("Statement necklace", "Necklace", "Amazon", .32),
            ("Matching earrings", "Earrings", "Flipkart", .16),
            ("Minimal bracelet/bangles", "Bracelet/Bangles", "Amazon", .11),
            ("Hair/occasion accessory", "Optional accessory", "Flipkart", .07),
        ]
        for name, cat, platform, pct in base:
            items.append({
                "name": name, "category": cat, "platform": platform,
                "estimated_price": money(budget*pct), "quantity": 1,
                "reason": f"Suggested for a {data.get('occasion','special')} occasion with a {data.get('style','elegant')} style.",
                "url": search_url(platform, name),
            })
        tips = [
            "Use the uploaded outfit image and actual outfit color as the final visual reference.",
            "For a coordinated look, avoid using too many statement pieces at once.",
            "Verify material, dimensions, seller ratings, and return policy before buying.",
        ]
        title = "Jewelry style plan"
        summary = f"A {data.get('style','elegant')} jewelry plan for a {data.get('occasion','special')} occasion."

    estimated_total = money(sum(x["estimated_price"] * x.get("quantity", 1) for x in items))
    return {
        "planner": planner,
        "title": title,
        "summary": summary,
        "budget": money(budget),
        "estimated_total": estimated_total,
        "remaining_budget": money(budget-estimated_total),
        "allocations": allocations,
        "recommendations": items,
        "tips": tips,
        "source_mode": "fallback",
    }
