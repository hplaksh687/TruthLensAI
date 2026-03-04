# TruthLensAI

TruthLensAI is a narrative intelligence system that analyzes claims for misinformation, emotional manipulation, and narrative drift.

Instead of simple fact-checking, TruthLensAI evaluates how narratives are constructed and how they influence public perception.

---

## Features

- Evidence strength scoring
- Context completeness analysis
- Emotional manipulation detection
- Narrative drift risk prediction
- Atomic claim extraction
- Missing context identification
- Responsible correction generation
- Structured intelligence summary

---

## Tech Stack

- Python
- Flask
- Google Gemini API
- BeautifulSoup (Web scraping)
- HTML / CSS dashboard

---

## How It Works

1. User submits a claim or article URL
2. Flask backend processes the request
3. If URL is provided, article text is extracted
4. Gemini AI analyzes the narrative structure
5. The response is converted into structured JSON
6. The dashboard visualizes the results

---

## Architecture

User Input  
↓  
Flask Backend  
↓  
Content Extraction  
↓  
Gemini AI Analysis  
↓  
Structured JSON Output  
↓  
Dashboard Visualization  

---

## Business Model

TruthLensAI can scale as a Narrative Intelligence Platform.

Potential applications:

- SaaS dashboard for journalists and researchers
- API service for media monitoring platforms
- Browser extension for misinformation detection
- Enterprise intelligence tool for policy analysis

---

## Future Work

- Real-time social media narrative monitoring
- Bias heatmap visualization
- Browser extension
- AI-powered misinformation alerts
- Narrative trend clustering

---

## Run Locally

Clone the repository

```bash
git clone https://github.com/hplaksh687/TruthLensAI.git
cd TruthLensAI
```

Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install flask requests beautifulsoup4 google-generativeai
```

Set API key

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Run the application

```bash
python app.py
```

Open browser

```
http://127.0.0.1:5000
```

---

## Author

Laksh H P
