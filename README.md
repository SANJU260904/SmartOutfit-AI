🧥 SmartOutfit – AI-Powered Personalized Outfit Recommendation System
🚀 Overview

SmartOutfit is a hybrid AI-based fashion recommendation web application that generates personalized outfit combinations from a user's real wardrobe.

The system combines:

Rule-based contextual filtering

Supervised Machine Learning ranking

Behavioral feature engineering

Unlike static fashion apps, SmartOutfit dynamically generates outfit combinations and intelligently ranks them based on learned user preferences.

🎯 Problem Statement

Traditional outfit recommendation systems:

Rely purely on fixed rules (no personalization), or

Require large image datasets and deep learning models

SmartOutfit solves this by:

Learning from structured wardrobe usage data

Training a supervised ML model on outfit history

Combining deterministic logic with probabilistic ranking

🧠 AI & Machine Learning Component

SmartOutfit implements a supervised Logistic Regression model using scikit-learn.

🔹 Training Data Source

The training dataset is automatically derived from:

Outfit history table

Clothing usage frequency

Favorite selections

Each previously generated outfit becomes a training sample.

🔹 Feature Engineering

For every outfit, the system extracts:

Encoded event type

Encoded weather type

Number of favorited items

Average times worn

Unique category count

Total number of items

These structured features form a tabular dataset used for training.

🔹 Model Training

Algorithm: Logistic Regression

Learning Type: Supervised Binary Classification

Framework: scikit-learn

Model Persistence: Joblib

The model predicts a probability score representing user preference likelihood.

🏗 System Architecture
🔹 Frontend

HTML

CSS

Vanilla JavaScript

API-driven UI updates

🔹 Backend

Python

Flask

SQLAlchemy ORM

SQLite Database

🔹 Machine Learning

scikit-learn

NumPy

Pandas

Joblib

🔄 Recommendation Pipeline

User selects Event + Weather
↓
Rule engine generates valid outfit combinations
↓
Feature extraction for each combination
↓
Logistic Regression predicts preference probability
↓
Novelty penalty applied to reduce repetition
↓
Top-ranked outfits returned

This ensures:

Context-aware recommendations

Behavioral personalization

Reduced repetition

Balanced exploration

📂 Database Design
clothing_item

id

category

times_worn

favorited

embedding_path (future extensibility)

outfit_history

event

weather

items_used

justification

created_at

The ML training dataset is derived directly from these tables.

💡 Key Highlights

Hybrid rule-based + ML ranking architecture

Behavioral data-driven personalization

Real-time inference integration

Model serialization and deployment

Fully explainable ML model

🛠 How to Run Locally
git clone <your-repo-url>
cd SmartOutfit
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py

Then open:

http://127.0.0.1:5000
🧪 Model Training

To retrain the ML model:

python train_model.py

This regenerates:

ml_model.pkl

event_encoder.pkl

weather_encoder.pkl

📌 Future Improvements

Explicit rating-based feedback learning

Model evaluation metrics

Auto-retraining pipeline

Improved justification explanations

Deep learning image classification extension

👩‍💻 Author

Sanjana Reddy
Integrated MTech(Software Engineering)