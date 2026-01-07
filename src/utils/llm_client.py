import os
import logging
import json
import random

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        HAS_GEMINI_LIB = True
    else:
        HAS_GEMINI_LIB = False
except ImportError:
    HAS_GEMINI_LIB = False
    logger.warning("google-generativeai not installed. Using mock data.")

MOCK_TASKS = {
    "Engineering": [
        "Refactor authentication middleware", "Fix race condition in payment API",
        "Optimize database queries", "Upgrade React to v18",
        "Write integration tests", "Setup CI/CD for staging"
    ],
    "Marketing": [
        "Draft social copy", "Design assets for Q3 campaign",
        "Review Google Ads", "Coordinate webinar",
        "Update landing page SEO", "Analyze competitor pricing"
    ],
    "General": [
        "Weekly team sync notes", "Onboard new hire", "Renew software licenses",
        "Quarterly budget review", "Update internal docs"
    ]
}

def generate_task_content(dept, section_name, count=3):
    if HAS_GEMINI_LIB and os.environ.get("GEMINI_API_KEY"):
        try:
            return _generate_llm_content(dept, section_name, count)
        except Exception as e:
            logger.warning(f"Gemini API Error (Switching to Mock): {e}")
            return _generate_mock_content(dept, section_name, count)
    else:
        return _generate_mock_content(dept, section_name, count)

def _generate_llm_content(dept, section_name, count):
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        f"Generate {count} realistic, short task titles and 1-sentence descriptions "
        f"for a '{dept}' team. The tasks are currently in the '{section_name}' stage.\n"
        f"Return ONLY a raw JSON list of objects with keys 'title' and 'description'. "
        f"Do not use Markdown formatting."
    )

    try:
        response = model.generate_content(prompt)
        raw_content = response.text.strip()
        
        if raw_content.startswith("```"):
            raw_content = raw_content.replace("```json", "").replace("```", "")

        tasks = json.loads(raw_content)
        return tasks[:count]
    except Exception:
        raise ValueError("Invalid API Response")

def _generate_mock_content(dept, section_name, count):
    key = next((k for k in MOCK_TASKS.keys() if k in dept), "General")
    base_list = MOCK_TASKS.get(key)
    
    results = []
    for _ in range(count):
        title = random.choice(base_list)
        if random.random() < 0.3:
            title += f" ({section_name})"
        results.append({
            "title": title,
            "description": f"Standard task for {title}."
        })
    return results