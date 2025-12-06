import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_intent(text: str):
    """
    Extracts intent, key facts, tone, structure, and constraints from raw text
    using Gemini. Returns a clean JSON dictionary.
    """
    
    prompt = f"""
You are an advanced semantic analysis system.
Your job is to read the user text and extract ONLY the precise meaning,
intent, tone, and non-negotiable facts.

You MUST return STRICT JSON with the following fields:

- intent: A short 1–2 sentence summary of what the author is trying to do.
- key_facts: A list of facts that MUST NOT be changed under any circumstance.
- tone_current: The tone of the original text.
- tone_target: The ideal human tone (choose: conversational, friendly, empathetic, professional, casual).
- complexity_level: A number from 1 to 4 (1=simple, 2=normal, 3=technical, 4=academic).
- structure_notes: Summary of document structure.
- forbidden_changes: Content that must not be altered.
- risk_flags: Sensitive content categories.

Rules:
- DO NOT rewrite the text.
- DO NOT add opinions.
- DO NOT add explanations.
- RETURN ONLY RAW JSON.
- DO NOT add ```json or any code fences.
- Output MUST start with {{ and end with }}.

User text:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",    
        contents=prompt,
    )

  
    result_text = response.text.strip()

   
    if result_text.startswith("```"):
        result_text = result_text.replace("```json", "").replace("```", "").strip()

  
    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON:\n" + result_text)

    return data



if __name__ == "__main__":
    sample_text = """  Over the past few months, our team at NovaTech has been struggling to roll out the new Orion v3.2 update. The project officially started on March 14, 2023, and the expected release date was supposed to be December 5, 2023, but that obviously didn’t happen. 

The biggest issue wasn’t the engineers — they were working 60-hour weeks — but the unclear specifications coming from upper management. For example, on July 7, 2023, the CTO, Michael Reeves, changed the entire security module’s design without consulting the engineering leads. That single decision caused a six-week delay.

Customers have been emailing us nonstop asking when the update will drop, especially after the outage on September 9 that affected nearly 12,000 users across India and Singapore. Some clients even threatened to switch to HelioSystems if we don’t deliver soon.

Right now, the mood in the office is a mix of exhaustion and frustration. A few engineers joked that “Orion is cursed,” but honestly, morale is low. I’m thinking of recommending that we push the release to Q2 2024, but I’m not sure how well that will be received.

Anyway, I need help organizing all this information for a report. It needs to be clear, factual, and not emotionally exaggerated, even though the whole situation has been incredibly stressful.
"""
    result = extract_intent(sample_text)
    print("\n--- Extracted Intent JSON ---")
    print(result)
    print("--------------------------------")
