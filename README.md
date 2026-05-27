# AI Resume Screener
## Built by Lakshya Prabha

A full-stack AI-powered ATS Resume Screener built with Django and Groq (LLaMA 3).

---

## 🚀 Features
- Upload PDF or paste resume text
- AI-powered ATS score (0-100) via Groq LLaMA 3
- Matched & missing skills analysis
- Improvement suggestions
- User login / register / session history
- Full scan history with delete option

---

## 🛠️ Tech Stack
- **Backend:** Python, Django, REST Framework
- **AI:** Groq API (LLaMA 3 70B) — Free
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** HTML, CSS (custom dark theme)
- **PDF Parsing:** PyPDF2
- **Deployment:** AWS EC2 / any server

---

## ⚙️ Setup & Run

### 1. Clone & Install
```bash
git clone <repo>
cd ai_resume_screener
pip install -r requirements.txt
```

### 2. Environment Variables
```bash
cp .env.example .env
# Edit .env and add your keys:
# SECRET_KEY = any random string
# GROQ_API_KEY = get free from https://console.groq.com
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```
Open: http://127.0.0.1:8000

---

## 🔑 Get Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Go to API Keys → Create Key
4. Copy and paste in your `.env` file

---

## 📁 Project Structure
```
ai_resume_screener/
├── config/
│   ├── settings.py
│   └── urls.py
├── screener/
│   ├── models.py       # ResumeScreen model
│   ├── views.py        # All views
│   ├── ai_service.py   # Groq LLM integration
│   ├── utils.py        # PDF extraction
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── screener/
│       ├── dashboard.html
│       ├── screen.html
│       ├── result.html
│       └── history.html
├── manage.py
├── requirements.txt
└── .env.example
```
