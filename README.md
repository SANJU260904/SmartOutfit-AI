SmartOutfit-AI
AI-Powered Outfit Recommendation System

SmartOutfit is a full-stack AI-based outfit recommendation system that generates personalized outfit combinations based on event type, weather conditions, and user wardrobe inventory.

The system combines a deterministic rule-based filtering engine with intelligent scoring logic to produce coherent, explainable, and context-aware outfit suggestions.

🚀 Key Features

Wardrobe item upload and storage

Automatic clothing category tagging

Event-aware outfit filtering (casual, formal, party, etc.)

Weather-based outfit constraints

Multi-item outfit generation (top, bottom, footwear, outerwear)

Human-readable AI-generated outfit explanations

REST-based Flask backend

Clean responsive frontend (HTML, CSS, JS)

SQLite-based persistent storage

Docker support for containerized deployment

🧠 System Architecture

The recommendation pipeline follows a hybrid architecture:

1️⃣ User Input

Event type

Weather condition

2️⃣ Rule-Based Filtering

Filters wardrobe items based on event compatibility

Applies weather constraints (e.g., sweaters for cold weather)

Ensures category completeness (top + bottom + footwear)

3️⃣ Outfit Construction

Combines filtered items into valid outfit sets

Applies ranking logic

Selects top-K recommendations

4️⃣ Explainability Layer

Generates human-readable justifications.

Example:

“This outfit works well for a formal evening event as the structured outerwear adds elegance while neutral tones maintain a polished look.”

🛠 Tech Stack
Backend

Python

Flask

SQLAlchemy

SQLite

AI / Logic Layer

Custom rule-based recommendation engine

Lightweight embedding placeholder (extensible)

Modular classifier integration (optional)

Frontend

HTML

CSS

JavaScript (Vanilla JS)

DevOps

Git

Docker

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

Windows

python -m venv venv
venv\Scripts\activate


Mac/Linux

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
python app.py


Visit:

http://127.0.0.1:5000

🐳 Docker Setup (Optional)
Build Image
docker build -t smartoutfit-ai .

Run Container
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

Hybrid rule-based logic ensures deterministic outfit validity

Modular architecture allows ML extension without breaking core system

Separation of backend, recommendation engine, and UI

Persistent database design for scalable wardrobe management

📈 Future Enhancements

Personalized user preference learning

Visual deep learning-based classification

User authentication & multi-user support

Cloud deployment (AWS / GCP)

Mobile-optimized UI

👩‍💻 Author

Golla Sanjana Reddy
Integrated M.Tech – Software Engineering

📌 Project Purpose

This project was built to demonstrate:

Full-stack system architecture

REST API design

Database modeling

Explainable recommendation logic

Containerization fundamentals