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

    prompt = f"""You are an advanced text rewriting system.

Your goal is to rewrite the user's text into a more natural, human, clear,
and conversational written style while preserving ALL meaning and ALL protected facts.

Below is the analysis JSON you MUST obey:

{analysis_json}

────────────────────────────────────────
### CORE CONSTRAINTS (MUST FOLLOW)
1. Preserve ALL items under:
   - key_facts
   - forbidden_changes

2. Do NOT modify:
   - dates
   - numbers
   - names
   - locations
   - technical terms in key_facts

3. Maintain the tone_target from analysis_json.

4. You MUST NOT:
   - add new facts
   - change ANY numbers
   - invent events
   - add personal opinions
   - remove essential information in key_facts

────────────────────────────────────────
### HUMAN-LIKE REWRITING RULES (LESS PREDICTABLE, MORE NATURAL)
Your rewrite MUST avoid mechanical patterns and overly consistent structure.
Produce writing that feels human and varied.

1. **Sentence Variety**
   - Mix short, medium, and long sentences.
   - Do NOT follow the same rhythm more than twice.
   - Include at least one sentence with a natural pause or break.
   - Avoid predictable patterns such as repeating "X caused Y" or "Because of A, B happened."

2. **Connector Diversity**
   - Do NOT overuse the same connectors.
   - Vary transitions: "so", "although", "at the same time", 
     "in a way", "still", "on the other hand", "that said", etc.
   - Avoid repeating a transition within 2–3 sentences.

3. **Paragraph Structure Variety**
   - Allow natural unevenness in paragraph length.
   - NOT every paragraph should conclude neatly; humans don't write that way.

4. **Natural Cognitive Flow**
   - Slight shifts in tone or emphasis are okay.
   - Mild reordering for clarity or more natural storytelling is allowed.
   - Avoid perfectly structured “topic → explanation → conclusion” in every paragraph.

5. **Human Texture Without Changing Meaning**
   - Mildly soften or expand an idea if it improves flow.
   - You MAY merge or split sentences when it improves clarity.
   - You MAY rephrase repeatedly structured sentences into more diverse patterns.

6. **Avoid AI-like Uniformity**
   - Do NOT repeat the same sentence template.
   - Do NOT mirror the structure of the original text too closely.
   - Avoid mechanical symmetry in paragraph endings.

────────────────────────────────────────
### IMPROVE THE FOLLOWING:
- clarity
- readability
- natural flow between ideas
- sentence variation
- overall human-like unpredictability

────────────────────────────────────────
### OUTPUT INSTRUCTIONS
Output ONLY the rewritten text. No explanations.

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
