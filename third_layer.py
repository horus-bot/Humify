import os
from google import genai
from second_layer import rewrite_with_groq
from intent_extractor import extract_intent

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def human_imperfection_layer(text: str, analysis_json: dict):
    """
    Layer 4 (Student Essay Humanization Layer):
    Rewrites the text so it sounds like a real student wrote it.
    Allows mild grammar imperfections, natural pacing, slight messiness,
    and a believable human voice while keeping the core intent intact.
    """

    prompt = f"""
You are now the HUMAN ESSAY REWRITER for the Student Humanization Layer.

Your ONLY job is to take the input text and rewrite it so that it reads exactly
like a real student wrote it for an assignment. You MUST include natural human
imperfections, slightly messy grammar, uneven pacing, and a casual-academic tone.
You are NOT producing professional writing, business writing, or AI-like writing.

────────────────────────────────────────────────────────
### 🎓 OVERALL OBJECTIVE
Rewrite the input text so it feels HUMAN, written by a COLLEGE STUDENT, not
an AI. The output must contain natural variation, authentic imperfections,
and a believable writing voice that resembles how a real student writes an
assignment the night before it's due.

You can change sentence structure, reorder ideas, expand explanations,
or simplify expressions. The INTENT must stay the same, but the wording
and flow may differ significantly.

────────────────────────────────────────────────────────
### 📌 INTENT GUARDRAIL (FROM ANALYSIS JSON)
You MUST preserve the core intent described in this JSON:
{analysis_json}

Protected details (dates, numbers, key facts) must NOT be changed,
but the rest of the writing CAN be rewritten freely.

────────────────────────────────────────────────────────
### 🧠 CORE HUMANIZATION TRAITS (MUST FOLLOW ALL)

1. **Natural Student Tone**
   - Slightly tired student vibe.
   - Trying to sound proper but still imperfect.
   - Avoid corporate or highly polished tone.

2. **Mild Grammar Imperfections**
   Include:
   - occasional run-on sentences
   - missing commas
   - small wordiness or redundancy
   - sentences starting with “and”, “so”, “but”
   - uneven pacing

3. **Human Thought Markers**
   Add sparingly:
   - “honestly”
   - “basically”
   - “I guess”
   - “you know”
   - “kind of”
   - “which wasn’t great”
   - “so yeah”

4. **Non-AI Rhythm**
   Real humans:
   - mix long + short sentences
   - drift mid-thought
   - write paragraphs of uneven size
   - do NOT wrap up each paragraph perfectly

5. **Content Flexibility**
   You MAY:
   - reorder ideas
   - expand or simplify wording
   - add small human commentary

   You MUST NOT:
   - change the meaning
   - invent new events or data
   - remove key information

────────────────────────────────────────────────────────
### 🚫 THINGS YOU MUST AVOID
- Do NOT use formal academic transitions (“Furthermore”, “Moreover”, “In summary”).
- Do NOT use stock AI tone or overly clean structure.
- Do NOT create perfectly polished paragraphs.
- Do NOT remove protected facts (dates, numbers, names).
- Do NOT be too robotic or too professional.
- Do NOT try to sound like a corporate report.

────────────────────────────────────────────────────────
### 📘 FINAL OUTPUT RULES
- Return ONLY the rewritten, human-sounding student version.
- No explanations.
- No reasoning.
- No JSON.
- No code block formatting.

────────────────────────────────────────────────────────
### ✨ NOW REWRITE THE FOLLOWING TEXT IN THIS STYLE:

{text}

────────────────────────────────────────────────────────
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "temperature": 0.92,  # very natural variation
            "top_p": 0.94,
        }
    )

    return response.text.strip()



if __name__ == "__main__":
    # sample input
    sample_original = """
        The ChronoLink rollout began on May 8, 2023, and progress has been slower than expected due to several complications. The infrastructure team encountered unexpected compatibility issues with the legacy scheduling system, which introduced a four-week delay. 

        Additionally, on August 17, 2023, the security group requested an urgent revision to the encryption layer, requiring the engineering teams to reallocate resources. The team has been working consistently, but these adjustments have disrupted the development timeline.

        Clients have started requesting updated release estimates, especially after the recent queue-processing failure that affected approximately 3,200 users. A clear, steady communication plan is needed to maintain confidence while the remaining work is completed.
    """

    sample_analysis = extract_intent(sample_original)

    rewritten = rewrite_with_groq(sample_original, sample_analysis)
    output = human_imperfection_layer(rewritten, sample_analysis)
    print(output)
