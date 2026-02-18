import random
from models import ClothingItem

# ------------------ CATEGORY NORMALIZATION ------------------

CATEGORY_MAP = {
    "shirt": "top",
    "t-shirt": "top",
    "blouse": "top",

    "jeans": "pants",
    "trousers": "pants",
    "shorts": "pants",

    "frock": "dress",
    "gown": "dress",
    "chudidhar": "chudidhar",
    "saree": "saree",

    "kurti": "kurti",

    "jacket": "outer",
    "coat": "outer",
    "sweater": "sweater",

    "top": "top",
    "pants": "pants",
    "skirt": "skirt",
    "dress": "dress"
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

    if event == "casual":
        return (
            ("top" in cats and "pants" in cats) or
            ("kurti" in cats and "pants" in cats) or
            (cats == {"dress"} and "skirt" not in cats)
        )

    if event == "party":
        return (
            cats == {"dress"} or
            ("top" in cats and "skirt" in cats)
        )

    if event == "date":
        return (
            cats == {"dress"} or
            ("top" in cats and ("pants" in cats or "skirt" in cats))
        )

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
            if it._norm == "sweater" and i not in layered:
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

# ------------------ JUSTIFICATION ------------------

def build_justification(cats, event, weather):
    parts = []

    if "dress" in cats:
        parts.append("a clean one-piece look")
    if "kurti" in cats:
        parts.append("a traditional Indian silhouette")
    if "top" in cats and "pants" in cats:
        parts.append("a comfortable everyday pairing")
    if "top" in cats and "skirt" in cats:
        parts.append("a stylish modern combination")

    if weather == "cold":
        parts.append("layered with a sweater for warmth")
    if weather == "rainy":
        parts.append("paired with a raincoat for weather protection")

    parts.append(f"appropriate for a {event} setting")

    return "Chosen because it offers " + ", ".join(parts) + "."

# ------------------ MAIN RECOMMENDER ------------------

def recommend_outfits(event="casual", weather="clear", k=3):
    item_map = _load_items()
    if not item_map:
        return []

    bases = generate_base_outfits(item_map)
    seen = set()
    valid = []

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
        valid.append(final)

    random.shuffle(valid)
    valid = valid[:k]

    results = []
    for o in valid:
        cats = {item_map[i]._norm for i in o}
        results.append({
            "items": [{
                "id": item_map[i].id,
                "category": item_map[i].category,
                "url": f"/image/{item_map[i].id}",
                "times_worn": item_map[i].times_worn,
                "favorited": bool(item_map[i].favorited)
            } for i in o],
            "justification": build_justification(cats, event, weather)
        })

    return results
