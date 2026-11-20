# ⭐ IMPORTANT: Groq JSON mode ke liye prompt mein word "json" hona ZAROORI hai
CONTRACT_ANALYSIS_PROMPT = """
You are an expert AI Legal Contract Analyst specializing in Indian Legal Frameworks and Commercial Contracts.

Analyze the contract text below and generate a structured json report.

Contract Text (Excerpt):
-----------------------
{contract_text}
-----------------------

Respond ONLY with a valid json object matching this schema EXACTLY (no markdown, no extra text):
{{
    "summary": "High-level summary of the contract.",
    "contract_type": "Type of agreement (e.g., NDA, Employment Agreement, Vendor Contract)",
    "key_clauses": [
        {{
            "clause_title": "Title of clause",
            "clause_text": "Exact or summarized text from contract",
            "explanation": "Legal meaning and implications"
        }}
    ],
    "risk_flags": [
        {{
            "title": "Short title of the risk",
            "description": "Detailed explanation of why this poses a legal or commercial risk",
            "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
        }}
    ],
    "overall_risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "recommendations": [
        "Actionable recommendation for the client/lawyer"
    ]
}}
"""