import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def humanize_with_groq(text: str):
    """
    Layer 4 — HUMAN STUDENT ESSAY MODE (WRITTEN, NOT SPOKEN)
    Adds natural human-like variation, controlled imperfections,
    and explicit burstiness + reduced predictability patterns.
    """

    prompt = f"""
You are the HUMAN STUDENT ESSAY REWRITER (WRITTEN MODE).

Your task is to rewrite the text so it reads like a real student typed it—
natural, slightly imperfect, structured like written work, but NEVER sounding
like spoken dialog. Maintain intent and accuracy while shaping the writing into
a human-like pattern with realistic variation, small inconsistencies, and
natural irregularities in rhythm and style.

────────────────────────────────────────
### 🎯 STYLE GOALS (WRITTEN, NOT SPOKEN)
- Written student assignment tone.
- Natural human texture, not chatty conversation.
- Mild grammar imperfections.
- Slightly uneven flow and structure.
- Occasional soft hesitations (in written form only):
  - “kind of”
  - “basically”
  - “in a way”
  - “wasn’t great”
- DO NOT use spoken-language fillers:
  - “you know?”
  - “I mean—”
  - “so yeah”
  - “well actually…”

────────────────────────────────────────
### ✔ HUMAN IMPERFECTIONS ALLOWED (1–3 TOTAL)
- a missing comma or extra comma
- a tiny duplication (“we we”)
- a slightly run-on sentence
- a dropped article (“the”, “a”) if meaning stays clear
- mild phrasing inconsistency

Keep errors subtle; maintain readability.

────────────────────────────────────────
### ❌ FORBIDDEN
- DO NOT introduce speech tone.
- DO NOT add new facts or alter protected details (dates, names, numbers).
- DO NOT remove essential meaning.
- DO NOT overuse casual fillers or repeated connectors.

────────────────────────────────────────
### ✔ ALLOWED FLEXIBILITY
You MAY:
- reorder sentences for smoother written flow
- expand or compress ideas if meaning remains the same
- include mild personal inflection appropriate for a student writer
- introduce small inconsistencies that real humans produce unintentionally

────────────────────────────────────────
### 🔥 BURSTINESS REQUIREMENTS (MUST FOLLOW)
Your rewritten text must show **human burstiness**, meaning natural variation
in sentence lengths, shapes, and pacing. Explicitly:

1. Mix:
   - short, choppy sentences
   - medium sentences
   - long, flowing sentences
2. Include at least one:
   - fragment
   - abrupt ending
   - overly long sentence that wanders slightly
3. Paragraphs should not be uniform in size.
4. Avoid perfect rhythm or repeated cadence.

Human writing has unpredictable pushes and pauses. Reflect that.

────────────────────────────────────────
### 🔥 LOW-PREDICTABILITY REQUIREMENTS (MUST FOLLOW)
Reduce structural predictability found in synthetic writing by:

1. Avoiding:
   - repeated sentence templates
   - mirrored paragraph structure
   - identical connector patterns (“X happened, which caused Y” repeatedly)
2. Introducing:
   - varied connectors (“though”, “still”, “at the same time”, “even then”)
   - slight tonal shifts (neutral → reflective → mildly frustrated)
   - one micro detour of thought (“or at least that’s how it seemed”)
3. Using vocabulary that is:
   - simple overall
   - occasionally irregular or slightly expressive
   - NOT overly safe or repetitive

Your outcome should FEEL human, not algorithmic.

────────────────────────────────────────
### 📘 OUTPUT RULES
- Output ONLY the rewritten text.
- No explanations.
- No markup.
- No lists.

────────────────────────────────────────
### 🔥 TEXT TO REWRITE IN THIS STYLE:

{text}

────────────────────────────────────────
END.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,
        top_p=0.92,
    )

    return response.choices[0].message.content
