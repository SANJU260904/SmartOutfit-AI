SmartOutfit-AI
AI-Powered Outfit Recommendation System

SmartOutfit is a full-stack AI-based outfit recommendation system that generates personalized outfit combinations based on event type, weather conditions, and wardrobe inventory.

The system combines a deterministic rule-based filtering engine with embedding-based similarity matching to produce coherent, explainable, and context-aware outfit suggestions.

🚀 Key Features

Wardrobe item upload and storage

Automatic clothing category tagging

Event-aware outfit filtering (casual, formal, party, etc.)

Weather-based outfit constraints

Multi-item outfit generation (top, bottom, footwear, outerwear)

Embedding-based style similarity using SentenceTransformers

Human-readable AI-generated outfit explanations

REST-based Flask backend

Clean responsive frontend (HTML, CSS, JS)

Docker support for containerized deployment

🧠 System Architecture

The recommendation pipeline follows a hybrid architecture:

User Input

Event type

Weather condition

Rule-Based Filtering

Filters wardrobe items based on event compatibility

Applies weather constraints (e.g., jackets for cold weather)

Ensures category completeness (top + bottom + footwear)

Embedding-Based Similarity

Uses SentenceTransformers to encode style descriptions

Computes similarity to maintain outfit coherence

Optional FAISS/Vector search optimization

Outfit Construction

Combines filtered items into valid outfit sets

Applies ranking logic

Explainability Layer

Generates human-readable justifications

Example:

"This outfit works well for a formal evening event as the blazer adds structure while the neutral tones maintain elegance."

🛠 Tech Stack
Backend

Python

Flask

SQLAlchemy

SQLite / PostgreSQL

AI & ML

SentenceTransformers

FAISS / Vector Search

Custom Rule Engine

Embedding Similarity Matching

Frontend

HTML

CSS

JavaScript

DevOps

Docker

Git

📂 Project Structure
SmartOutfit-AI/
│
├── app.py
├── models.py
├── recommender.py
├── requirements.txt
├── Dockerfile
│
├── scripts/
│   ├── preprocess.py
│   ├── train_classifier.py
│   └── classify_helper.py
│
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/SmartOutfit-AI.git
cd SmartOutfit-AI

2️⃣ Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate


Mac/Linux:

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
python app.py


Visit:

http://127.0.0.1:5000

🐳 Docker Setup (Optional)

Build image:

docker build -t smartoutfit-ai .


Run container:

docker run -p 5000:5000 smartoutfit-ai

🎯 Example Use Case

Input

Event: Formal Dinner

Weather: Cold

Output

Blazer

Formal Shirt

Trousers

Leather Shoes

With generated explanation describing style compatibility.

🔬 Design Decisions

Hybrid rule + embedding approach ensures both logical correctness and style coherence.

Deterministic filtering prevents invalid outfit combinations.

Embedding similarity improves personalization potential.

Modular architecture allows future extension into deep learning pipelines.

📈 Future Enhancements

Personalized user preference learning

Deep learning-based visual style classification

User authentication & saved wardrobes

Cloud deployment (AWS / GCP)

Mobile-responsive UI upgrade

👩‍💻 Author

Golla Sanjana Reddy
Integrated M.Tech – Software Engineering

✅ After Pasting This

Save README.md

Run:

git add README.md
git commit -m "Updated README - professional documentation"
git push
