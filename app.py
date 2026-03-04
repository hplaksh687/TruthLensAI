import json
import os
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import google.generativeai as genai


# ==============================
# CONFIGURE GEMINI
# ==============================
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

model_flash = genai.GenerativeModel("models/gemini-2.5-flash")
model_pro   = genai.GenerativeModel("models/gemini-2.5-pro")

app = Flask(__name__)


# ==============================
# SAFE DEFAULT RESULT STRUCTURE
# ==============================
def empty_result():
    return {
        "scores": {
            "evidence": 0,
            "context": 0,
            "emotion": 0,
            "manipulation": 0,
            "confidence": 0,
            "bias_score": 0.0,
            "political_bias": "Unknown",
            "drift_risk": "Unknown"
        },
        "atomic_claims": [],
        "evidence_assessment": "",
        "missing_context": [],
        "emotional_analysis": "",
        "narrative_drift_analysis": "",
        "responsible_correction": "",
        "summary": ""
    }


# ==============================
# URL CONTENT EXTRACTOR
# ==============================
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=8, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs).strip()
        return text[:5000] if text else None
    except Exception:
        return None


# ==============================
# CLEAN GEMINI JSON OUTPUT
# ==============================
def parse_json_response(raw_text):
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    return json.loads(cleaned)


# ==============================
# BUILD INTELLIGENCE PROMPT
# ==============================
def build_prompt(content):
    return f"""
You are TruthLensAI — a Narrative Intelligence system.

Perform a structured misinformation and narrative analysis.

Content:
\"\"\"{content}\"\"\"

Return STRICT JSON only.

Structure:

{{
  "scores": {{
    "evidence": 0-100,
    "context": 0-100,
    "emotion": 0-100,
    "manipulation": 0-100,
    "confidence": 0-100,
    "bias_score": -1.0 to 1.0,
    "political_bias": "Far Left/Left/Center-Left/Center/Center-Right/Right/Far Right",
    "drift_risk": "Low/Moderate/High"
  }},
  "atomic_claims": [],
  "evidence_assessment": "Detailed evidence reliability explanation.",
  "missing_context": [],
  "emotional_analysis": "Explanation of emotional framing or manipulation.",
  "narrative_drift_analysis": "Explanation of how the narrative may evolve or escalate.",
  "responsible_correction": "Rewrite the claim responsibly with uncertainty framing.",
  "summary": "Executive intelligence summary."
}}

Return valid JSON only.
"""


# ==============================
# MAIN ROUTE
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    agreement_score = None
    error_message = None

    if request.method == "POST":

        user_input = request.form.get("claim", "").strip()

        if not user_input:
            error_message = "Please enter a claim or URL."
            return render_template("index.html",
                                   result=None,
                                   agreement=None,
                                   error=error_message)

        if len(user_input) < 15:
            error_message = "Input too short. Please provide more detail."
            return render_template("index.html",
                                   result=None,
                                   agreement=None,
                                   error=error_message)

        # URL Handling
        if user_input.startswith("http://") or user_input.startswith("https://"):
            extracted = extract_text_from_url(user_input)
            if not extracted:
                error_message = "Could not fetch URL content. Try pasting the text."
                return render_template("index.html",
                                       result=None,
                                       agreement=None,
                                       error=error_message)
            content = extracted
        else:
            content = user_input

        prompt = build_prompt(content)

        data_flash = None
        data_pro = None

        # FLASH MODEL
        try:
            response_flash = model_flash.generate_content(prompt)
            data_flash = parse_json_response(response_flash.text)
        except Exception as e:
            app.logger.warning(f"Flash error: {e}")

        # PRO MODEL
        try:
            response_pro = model_pro.generate_content(prompt)
            data_pro = parse_json_response(response_pro.text)
        except Exception as e:
            app.logger.warning(f"Pro error: {e}")

        # MERGE LOGIC
        if data_flash and data_pro:

            diff = abs(
                data_flash["scores"]["confidence"] -
                data_pro["scores"]["confidence"]
            )

            agreement_score = 100 - diff

            avg_confidence = (
                data_flash["scores"]["confidence"] +
                data_pro["scores"]["confidence"]
            ) // 2

            result = data_flash
            result["scores"]["confidence"] = avg_confidence

        elif data_flash:
            result = data_flash

        elif data_pro:
            result = data_pro

        else:
            error_message = "Both models failed. API quota may be exceeded."
            result = empty_result()

        # SAFETY STRUCTURE CHECK
        if not result or "scores" not in result:
            result = empty_result()

    return render_template(
        "index.html",
        result=result,
        agreement=agreement_score,
        error=error_message
    )


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)