import os
from google import genai
from second_layer import rewrite_with_groq
from intent_extractor import extract_intent

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def human_imperfection_layer(text: str, analysis_json: dict):
    """
    Layer 3: Adds light, natural human-like imperfections using Gemini.
    Does NOT change meaning or any protected facts.
    """

    prompt = f"""
You are a subtle human-style enhancer.

Your job is to take a professionally rewritten text (already polished)
and add LIGHT, natural human imperfections WITHOUT changing any meaning.

Here is the analysis JSON that defines protected information:
{analysis_json}

You MUST follow these rules:

1. Do NOT change:
   - any key_facts
   - any forbidden_changes
   - any dates
   - any numbers
   - any names
   - any locations

2. Only add VERY LIGHT human-like elements:
   - contractions (it's, we're, they've)
   - soft hedges (a bit, kind of, seems, probably)
   - natural connectors (so, anyway, honestly)
   - small rhythm shifts
   - light conversational flow

3. KEEP the tone_target exactly as defined.
   Don't make it overly casual unless tone_target says so.

4. DO NOT:
   - add new facts
   - remove important details
   - exaggerate
   - add emotional language beyond mild natural phrasing

5. Return ONLY the enhanced text.
    - No JSON
    - No code fences
    - No explanations

Text to enhance:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={"temperature": 0.7}

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