import os
import numpy as np
from app import app
from models import db, ClothingItem
from recommender import get_embedding

DATA_DIR = 'dataset_sample'  # place sample images here

with app.app_context():
    files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    count = 0
    for fname in files:
        path = os.path.join(DATA_DIR, fname)
        try:
            emb = get_embedding(path)
            emb_path = os.path.join('embeddings', fname + '.npy')
            np.save(emb_path, emb)
            # store in DB
            item = ClothingItem(
                filename=fname,
                path=path,
                embedding_path=emb_path,
                category='unknown',
                color='unknown',
                times_worn=0,
                favorited=False
            )
            db.session.add(item)
            count += 1
        except Exception as e:
            print(f"Failed for {fname}: {e}")
    db.session.commit()
    print(f"Preprocess complete. Added {count} items.")
