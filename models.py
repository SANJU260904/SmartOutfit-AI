from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean

db = SQLAlchemy()

class ClothingItem(db.Model):
    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=False)
    embedding_path = Column(String, nullable=False)
    category = Column(String, default="unknown")  # e.g., top, bottom, dress, outer
    color = Column(String, default="unknown")
    times_worn = Column(Integer, default=0)
    favorited = Column(Boolean, default=False)
