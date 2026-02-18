import os
import numpy as np
from flask import Flask, request, jsonify, send_file, send_from_directory
from datetime import datetime
from models import db, ClothingItem
from recommender import recommend_outfits

from scripts.classify_helper import load_classifier, predict_category

UPLOAD_FOLDER = 'uploads'
EMBED_FOLDER = 'embeddings'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EMBED_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartoutfit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

try:
    load_classifier()
except Exception:
    pass

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ---------- UPLOAD ----------
@app.route('/api/upload', methods=['POST'])
def upload():
    f = request.files.get('image')
    if not f:
        return jsonify({"error": "no image"}), 400

    filename = f"{int(datetime.utcnow().timestamp()*1000)}_{f.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(path)

    embedding = get_embedding(path)
    emb_path = os.path.join(EMBED_FOLDER, filename + ".npy")
    np.save(emb_path, embedding)

    try:
        predicted = predict_category(path)
    except Exception:
        predicted = "unknown"

    item = ClothingItem(
        filename=filename,
        path=path,
        embedding_path=emb_path,
        category=predicted,
        color="unknown",
        times_worn=0,
        favorited=False
    )

    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id})

# ---------- ITEMS ----------
@app.route('/api/items')
def items():
    return jsonify([
        {
            "id": it.id,
            "url": f"/image/{it.id}",
            "category": it.category,
            "times_worn": it.times_worn,
            "favorited": bool(it.favorited)
        }
        for it in ClothingItem.query.all()
    ])

@app.route('/image/<int:item_id>')
def image(item_id):
    item = ClothingItem.query.get_or_404(item_id)
    return send_file(item.path)

# ---------- UPDATE CATEGORY ----------
@app.route('/api/update_category', methods=['POST'])
def update_category():
    body = request.json or {}
    item = ClothingItem.query.get(body.get('item_id'))
    if not item:
        return jsonify({"error": "not found"}), 404

    item.category = body.get('category')
    db.session.commit()
    return jsonify({"ok": True})

# ---------- RECOMMEND ----------
@app.route('/api/recommend', methods=['POST'])
def recommend():
    body = request.json or {}
    event = body.get('event', 'casual')
    weather = body.get('weather', 'clear')

    recs = recommend_outfits(event=event, weather=weather, k=3)

    return jsonify({
        "outfits": recs,
        "message": "ok" if recs else "No suitable outfits found"
    })

# ---------- WORN ----------
@app.route('/api/mark_worn', methods=['POST'])
def mark_worn():
    item = ClothingItem.query.get(request.json.get('item_id'))
    if not item:
        return jsonify({"error": "not found"}), 404

    item.times_worn += 1
    db.session.commit()
    return jsonify({"ok": True})

# ---------- FAVORITE ----------
@app.route('/api/favorite', methods=['POST'])
def favorite():
    item = ClothingItem.query.get(request.json.get('item_id'))
    if not item:
        return jsonify({"error": "not found"}), 404

    item.favorited = not item.favorited
    db.session.commit()
    return jsonify({"ok": True})

# ---------- DELETE ----------
@app.route('/api/delete_item', methods=['POST'])
def delete_item():
    item = ClothingItem.query.get(request.json.get('item_id'))
    if not item:
        return jsonify({"error": "not found"}), 404

    if os.path.exists(item.path):
        os.remove(item.path)
    if item.embedding_path and os.path.exists(item.embedding_path):
        os.remove(item.embedding_path)

    db.session.delete(item)
    db.session.commit()
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True)
