import json
import re
from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.models import AnalysisResult
from app.services.prompts import CONTRACT_ANALYSIS_PROMPT


def sanitize_json_response(raw_text: str) -> str:
    """
    Safety net cleanup:
    1. Removes <think>...</think> blocks (Qwen3 reasoning output)
    2. Removes markdown code fences (```json ... ```)
    """
    cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL)
    cleaned = re.sub(r"```json\s*", "", cleaned)
    cleaned = re.sub(r"```\s*", "", cleaned)
    return cleaned.strip()


def run_groq_analysis(contract_id: str, contract_text: str) -> AnalysisResult:
    """
    Calls Groq (Qwen3-32B) to analyze contract text.
    Returns validated Pydantic AnalysisResult object.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured in .env file.")

    # 1. Create Groq Client (OpenAI jaisa hi syntax hai)
    client = Groq(api_key=GROQ_API_KEY)

    # 2. Trim text (context window bachao)
    truncated_text = contract_text[:15000]
    prompt = CONTRACT_ANALYSIS_PROMPT.format(contract_text=truncated_text)

    # 3. Call Groq API
    response = client.chat.completions.create(
        model=GROQ_MODEL,  # "qwen/qwen3-32b"
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI Legal Contract Analyst. Always respond with valid json only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,                    # Low = focused, deterministic output
        max_completion_tokens=8000,         # Lamba JSON report ke liye enough space
        response_format={"type": "json_object"},  # ⭐ GUARANTEED JSON output!
        extra_body={"reasoning_effort": "none"}   # ⭐ Qwen3 thinking OFF (fast + clean)
    )

    # 4. Extract & Clean Response
    raw_response = response.choices[0].message.content
    sanitized = sanitize_json_response(raw_response)
    data_dict = json.loads(sanitized)

    # 5. Inject metadata + Validate with Pydantic
    data_dict["contract_id"] = contract_id
    analysis_result = AnalysisResult(**data_dict)
    return analysis_result