import json
from groq import Groq
from fastapi import HTTPException
from app.core.config import settings

# Initialize Groq Client
client = Groq(api_key=settings.GROQ_API_KEY)

CROP_ANALYSIS_PROMPT = """
You are an expert plant pathologist and agricultural AI scientist. Analyze this crop image in detail.

Respond STRICTLY with a valid JSON object matching this structure:
{
  "crop_detected": "Name of plant/crop identified",
  "is_healthy": true/false,
  "confidence_score": 0.95,
  "severity": "None / Mild / Moderate / Severe / Critical",
  "diseases": [
    {
      "name": "Disease name",
      "symptoms_observed": ["Symptom 1", "Symptom 2"]
    }
  ],
  "recommended_treatments": [
    {
      "type": "Chemical / Organic / Cultural",
      "action": "Description of treatment step"
    }
  ],
  "overall_health_summary": "Short summary of plant condition",
  "prevention_tips": ["Tip 1", "Tip 2"]
}
"""

def analyze_crop_image(base64_image: str, content_type: str = "image/jpeg") -> dict:
    """
    Sends base64 image payload to Groq Cloud Vision AI model.
    """
    try:
        response = client.chat.completions.create(
            model=settings.GROQ_VISION_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": CROP_ANALYSIS_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2
        )

        raw_json_str = response.choices[0].message.content
        return json.loads(raw_json_str)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Groq AI model returned invalid JSON structure."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Groq Vision API Error: {str(e)}"
        )