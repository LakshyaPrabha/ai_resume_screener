import json
import re
from groq import Groq
from django.conf import settings


def extract_json_from_response(text):
    """Extract JSON from LLM response even if wrapped in markdown."""
    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try to find JSON block
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return None


def screen_resume(resume_text: str, job_description: str, job_title: str) -> dict:
    """
    Send resume + JD to Groq LLaMA3 and get ATS analysis back.
    Returns a dict with score, matched_skills, missing_skills, suggestions, feedback.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume screener and HR specialist.

Analyze the following resume against the job description and return ONLY a valid JSON object with no extra text.

JOB TITLE: {job_title}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY this JSON structure (no markdown, no explanation, just JSON):
{{
  "ats_score": <integer 0-100>,
  "matched_skills": ["skill1", "skill2", "skill3"],
  "missing_skills": ["skill1", "skill2", "skill3"],
  "suggestions": [
    "Suggestion 1 to improve the resume",
    "Suggestion 2 to improve the resume",
    "Suggestion 3 to improve the resume",
    "Suggestion 4 to improve the resume",
    "Suggestion 5 to improve the resume"
  ],
  "overall_feedback": "2-3 sentence overall assessment of the candidate's fit for this role."
}}

Scoring guide:
- 85-100: Excellent match
- 70-84: Good match
- 50-69: Average match
- Below 50: Poor match
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
        )
        raw = response.choices[0].message.content
        data = extract_json_from_response(raw)

        if not data:
            return _fallback_error("Could not parse AI response. Please try again.")

        return {
            "ats_score": int(data.get("ats_score", 0)),
            "matched_skills": data.get("matched_skills", []),
            "missing_skills": data.get("missing_skills", []),
            "suggestions": data.get("suggestions", []),
            "overall_feedback": data.get("overall_feedback", ""),
            "error": None,
        }

    except Exception as e:
        return _fallback_error(str(e))


def _fallback_error(msg):
    return {
        "ats_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "suggestions": [],
        "overall_feedback": "",
        "error": msg,
    }
