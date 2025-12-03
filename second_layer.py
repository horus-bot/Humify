import os
from groq import Groq
from intent_extractor import extract_intent

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rewrite_with_groq(user_text: str, analysis_json: dict):
    """
    Layer 2: Rewrites text into a human, natural style while preserving all meaning.
    Uses Groq for fast rewriting.
    """

    prompt = f"""
You are an advanced text rewriting system.

Your goal is to rewrite the user's text into a more natural, human, clear,
and conversational style while preserving ALL meaning and ALL protected facts.

Below is the analysis JSON you MUST obey:

{analysis_json}

RULES YOU MUST FOLLOW:

1. Preserve ALL items under:
   - key_facts
   - forbidden_changes

2. Do NOT modify:
   - dates
   - numbers
   - names
   - locations
   - technical terms in key_facts

3. The tone_target MUST replace tone_current.
   - If tone_target = "professional", rewrite accordingly.
   - If tone_target = "conversational", make it human and relaxed.
   - If tone_target = "friendly", use warm and clear tone.
   - If tone_target = "empathetic", soften tense language.

4. Improve:
   - clarity
   - sentence flow
   - transitions between paragraphs
   - readability
   - sentence variety

5. You MAY:
   - split long sentences
   - merge redundant ideas
   - add small natural connectors ("so", "meanwhile", "on top of that")
   - reduce emotional exaggeration if needed

6. You MUST NOT:
   - add new facts
   - change ANY numbers
   - invent events
   - add personal opinions
   - remove essential information from key_facts

7. Output ONLY the rewritten text. No explanation.

User's text:
{user_text}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Best for rewriting + speed
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,              # balanced creativity
    )

    return response.choices[0].message.content





if __name__ == "__main__":
    # sample input
    sample_original = """
        Our team started working on the AetherSync integration on February 2, 2024, but things haven’t gone smoothly. 
The backend team reported that the API documentation was incomplete, which caused repeated misunderstandings and at least a three-week delay.

Then on March 12, 2024, Maya added a last-minute requirement involving real-time encryption, and that pushed things even further behind schedule. 
Right now, the front-end engineers are frustrated because they’ve been waiting for the backend responses to stabilize.

Clients have already started asking when the update will be ready, especially after the downtime last month that affected around 4,500 users. 
I need this rewritten clearly and professionally so I can include it in the monthly progress report.

    """

    sample_analysis = extract_intent(sample_original)

    rewritten = rewrite_with_groq(sample_original, sample_analysis)
    print("\n--- REWRITTEN TEXT ---")
    print(rewritten)
    print("-----------------------")
