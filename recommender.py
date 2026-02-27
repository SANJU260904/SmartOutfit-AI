import random
import numpy as np
import joblib
from datetime import datetime, timedelta
from models import ClothingItem
import sqlite3

# ------------------ LOAD ML MODEL ------------------

model = joblib.load("ml_model.pkl")
le_event = joblib.load("event_encoder.pkl")
le_weather = joblib.load("weather_encoder.pkl")

# ------------------ CATEGORY NORMALIZATION ------------------

CATEGORY_MAP = {
    "shirt": "top",
    "t-shirt": "top",
    "blouse": "top",

    "jeans": "pants",
    "trousers": "pants",
    "pants": "pants",

    # IMPORTANT: keep shorts separate
    "shorts": "shorts",

    "frock": "dress",
    "gown": "dress",
    "dress": "dress",

    "chudidhar": "chudidhar",
    "saree": "saree",
    "kurti": "kurti",

    "jacket": "outer",
    "coat": "outer",
    "outer": "outer",
    "sweater": "sweater",

    "top": "top",
    "skirt": "skirt"
}

def normalize(cat):
    return CATEGORY_MAP.get(cat)

# ------------------ LOAD ITEMS ------------------

def _load_items():
    items = ClothingItem.query.all()
    item_map = {}
    for it in items:
        norm = normalize(it.category)
        if norm:
            it._norm = norm
            item_map[it.id] = it
    return item_map

# ------------------ EVENT RULES ------------------

def event_ok(cats, event):
    cats = set(cats)

    # CASUAL
    if event == "casual":
        return (
            ("top" in cats and ("pants" in cats or "shorts" in cats)) or
            ("kurti" in cats and "pants" in cats) or
            (cats == {"dress"})
        )

    # FORMAL (shirt + pants only)
    if event == "formal":
        return (
            ("top" in cats and "pants" in cats)
        )

    # PARTY
    if event == "party":
        return (
            cats == {"dress"} or
            ("top" in cats and "skirt" in cats)
        )

    # DATE
    if event == "date":
        return (
            cats == {"dress"} or
            ("top" in cats and ("pants" in cats or "skirt" in cats))
        )

    # TRADITIONAL (NO shorts allowed)
    if event == "traditional":
        return (
            ("kurti" in cats and "pants" in cats) or
            ("chudidhar" in cats) or
            ("saree" in cats)
        )

    return False

# ------------------ WEATHER LAYERING ------------------

def apply_weather_layers(base, item_map, weather):
    layered = list(base)
    norms = [item_map[i]._norm for i in base]

    if weather == "cold":
        for i, it in item_map.items():
            if it._norm in ["sweater", "outer"] and i not in layered:
                layered.append(i)
                break

    if weather == "rainy":
        for i, it in item_map.items():
            if it._norm == "outer" and i not in layered:
                layered.append(i)
                break

    if weather == "windy" and "skirt" in norms:
        return None

    return layered

# ------------------ GENERATE BASE OUTFITS ------------------

def generate_base_outfits(item_map):
    by_cat = {}
    for i, it in item_map.items():
        by_cat.setdefault(it._norm, []).append(i)

    outfits = []

    for d in by_cat.get("dress", []):
        outfits.append([d])

    for t in by_cat.get("top", []):
        for p in by_cat.get("pants", []):
            outfits.append([t, p])

    for t in by_cat.get("top", []):
        for s in by_cat.get("shorts", []):
            outfits.append([t, s])

    for t in by_cat.get("top", []):
        for s in by_cat.get("skirt", []):
            outfits.append([t, s])

    for k in by_cat.get("kurti", []):
        for p in by_cat.get("pants", []):
            outfits.append([k, p])

    for c in by_cat.get("chudidhar", []):
        outfits.append([c])

    for s in by_cat.get("saree", []):
        outfits.append([s])

    return outfits

# ------------------ NOVELTY CHECK ------------------

def recently_used(item_ids):
    conn = sqlite3.connect("instance/smartoutfit.db")
    cursor = conn.cursor()

    cutoff = datetime.now() - timedelta(days=3)

    cursor.execute("SELECT items_used, created_at FROM outfit_history")
    rows = cursor.fetchall()
    conn.close()

    for items_used, created_at in rows:
        if not created_at:
            continue
        if datetime.fromisoformat(created_at) >= cutoff:
            past_ids = list(map(int, items_used.split(",")))
            if set(past_ids) == set(item_ids):
                return True
    return False

# ------------------ MAIN RECOMMENDER ------------------

def recommend_outfits(event="casual", weather="clear", k=3):
    item_map = _load_items()
    if not item_map:
        return []

    bases = generate_base_outfits(item_map)
    seen = set()
    scored = []

    for base in bases:
        cats = [item_map[i]._norm for i in base]

        if not event_ok(cats, event):
            continue

        final = apply_weather_layers(base, item_map, weather)
        if not final:
            continue

        key = tuple(sorted(final))
        if key in seen:
            continue
        seen.add(key)

        items = [item_map[i] for i in final]

        # -------- Feature Engineering --------
        favorite_count = sum(int(it.favorited) for it in items)
        avg_times_worn = sum(it.times_worn for it in items) / len(items)
        unique_categories = len(set(it._norm for it in items))
        total_items = len(items)

        try:
            event_encoded = le_event.transform([event])[0]
        except:
            event_encoded = 0

        try:
            weather_encoded = le_weather.transform([weather])[0]
        except:
            weather_encoded = 0

        features = np.array([[
            event_encoded,
            weather_encoded,
            favorite_count,
            avg_times_worn,
            unique_categories,
            total_items
        ]])

        score = float(model.predict_proba(features)[0][1])

        # -------- Novelty Penalty --------
        if recently_used(final):
            score -= 0.15

        scored.append((score, final))

    if not scored:
        return []

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:k]

    results = []
    for score, o in top:
        results.append({
            "items": [{
                "id": item_map[i].id,
                "category": item_map[i].category,
                "url": f"/image/{item_map[i].id}",
                "times_worn": item_map[i].times_worn,
                "favorited": bool(item_map[i].favorited)
            } for i in o],
            "justification": f"AI-ranked recommendation (score: {round(score, 2)})"
        })

    return results