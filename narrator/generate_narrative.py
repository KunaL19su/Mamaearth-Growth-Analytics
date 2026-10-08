
import os
import json
import time

from google import genai
from google.genai import types


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

NARRATOR_DIR = os.path.join(BASE_DIR, "narrator")
FINDINGS_PATH = os.path.join(NARRATOR_DIR, "findings.json")
OUTPUT_PATH = os.path.join(NARRATOR_DIR, "sample_output.txt")


with open(FINDINGS_PATH, "r", encoding="utf-8") as f:
    findings = json.load(f)


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable not found."
    )


client = genai.Client(api_key=API_KEY)


def generate_narrative(findings, retries=3):

    prompt = f"""
You are a business analytics consultant.

Create a complete but concise management-level narrative
for the Mamaearth Growth Analytics project.

Use ONLY the findings provided below.
Do NOT invent or change any numbers.

Return EXACTLY these 4 sections:

1. Executive Summary
2. Key Findings
3. Business Recommendations
4. Caveats

Requirements:

- Mention the data-quality improvements.
- Mention raw vs cleaned revenue and the difference.
- Mention COD return rate.
- Mention the highest-risk COD + City Tier 2 segment.
- Mention the 2 quantity outliers.
- Mention that January appears highest with outliers,
  but March 2026 is the corrected peak without outliers.
- Give practical business recommendations.
- Explicitly state that correlation does not imply causation.
- Keep the response concise enough to finish all 4 sections.
- Do not mention that you are an AI.

FINDINGS:

{json.dumps(findings, indent=4)}
"""

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    max_output_tokens=2048
                )
            )

            return response.text

        except Exception as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)

    raise RuntimeError(
        "Gemini narrative generation failed after retries."
    )


narrative = generate_narrative(findings)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(narrative)

print("Narrative generated successfully!")
print("Saved:", OUTPUT_PATH)
