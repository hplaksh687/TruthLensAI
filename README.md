# TruthLensAI

TruthLensAI is a narrative intelligence system that analyzes claims for misinformation, emotional manipulation, and narrative drift.

## Features

- Evidence strength scoring
- Context completeness analysis
- Emotional manipulation detection
- Narrative drift risk prediction
- Atomic claim extraction
- Missing context identification
- Responsible correction generation

## Tech Stack

- Python
- Flask
- Google Gemini API
- BeautifulSoup (Web scraping)
- HTML / CSS dashboard

## How It Works

1. User submits a claim or article URL.
2. Flask backend processes the input.
3. If URL, the system extracts article text.
4. Gemini AI analyzes the narrative structure.
5. Results are converted into structured JSON.
6. The dashboard visualizes the analysis.

## Run Locally

Clone the repository

```bash
git clone https://github.com/hplaksh687/TruthLensAI.git
cd TruthLensAI
