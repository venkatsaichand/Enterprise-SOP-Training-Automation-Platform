SYSTEM_PROMPT = """
You are a senior AI engineer, operations leader, process designer, corporate trainer, and product-grade
content strategist. Turn SOP documents into concise, execution-ready training assets for internal company
use. Every output must be practical, specific, and suitable for deployment in a real business setting.
Write with precision. Avoid filler, generic phrasing, duplicated ideas, and obvious statements.
""".strip()


OUTPUT_SCHEMA = """
Return valid JSON with exactly these top-level keys:
- "sop_name": string
- "summary": list of 3 to 5 strings
- "training_guide": list of 6 to 10 objects with:
  - "title": string
  - "owner": string
  - "action": string
  - "outcome": string
  - "decision_trigger": string
- "quiz": list of 4 objects with:
  - "question": string
  - "answer": string
  - "explanation": string
- "common_mistakes": list of 3 strings
- "improvements": list of 3 objects with:
  - "theme": string
  - "improvement": string
  - "impact": string
- "slides": object with:
  - "deck_title": string
  - "slides": list of 8 objects with:
    - "slide_number": integer
    - "title": string
    - "bullets": list of 2 to 5 strings
    - "visual_suggestions": list of 2 to 3 strings
  - "design_notes": object with:
    - "color_theme": string
    - "layout_suggestions": list of 2 to 4 strings
    - "font_pairing": string
""".strip()


USER_PROMPT_TEMPLATE = """
Read the SOP below and build a production-quality training package.

{output_schema}

All top-level sections are mandatory.
Do not omit, rename, or leave out any of these keys:
- "summary"
- "training_guide"
- "quiz"
- "common_mistakes"
- "improvements"
- "slides"

Content rules:
- Executive Summary:
  - Max 5 bullets.
  - Each bullet must contain an action and an owner.
  - Remove generic language.
  - Keep only decision-relevant execution points.
  - Write like a founder or department head is scanning it quickly.
- Training Guide:
  - Build a precise execution checklist.
  - Every step must start with a verb in the "title".
  - Clearly define owner, action, and expected outcome.
  - Add decision triggers where needed using "If X happens -> do Y".
  - Avoid filler and repetition.
  - Make the checklist usable without referring back to the SOP.
  - Keep each field short and operational.
- Scenario-Based Quiz:
  - Create 4 realistic workplace situations with ambiguity, risk, or a blocker.
  - Test judgment and decision-making, not memory.
  - Keep answers concise and practical.
  - Keep explanations to one line about why the action matters.
- Common Mistakes:
  - List 3 realistic execution failures teams commonly make.
  - Include the consequence in the same line.
- Process Improvements:
  - Provide exactly 3 improvements covering efficiency, automation, and clarity.
  - Make them concrete and practical for a company environment.
- Slides:
  - Create a premium executive slide deck suitable for Google Slides or PowerPoint.
  - Use exactly 8 slides:
    - Slide 1: Title
    - Slide 2: Overview
    - Slides 3 to 6: Key steps grouped logically
    - Slide 7: Common mistakes
    - Slide 8: Improvements
  - Keep each slide minimal with max 5 bullets.
  - Use clean executive headings.
  - Add visual suggestions such as icons, process flow, checklist, alert, timeline, or dividers.
  - Design notes must recommend a minimal modern color theme, layout suggestions, and font pairing.

Quality rules:
- Use plain business language.
- Avoid long paragraphs.
- Avoid repeated points across sections.
- Keep outputs tight and practical.
- Prefer concrete owners such as HR, IT, Manager, Supervisor, Operations, or Finance.
- If the SOP is incomplete, infer the safest operational assumptions without inventing policy-heavy details.
- Do not include markdown code fences.
- Do not include any text outside the JSON object.
- If a section is weak or partially inferred, still return that section with the required structure.

SOP:
{sop_text}
""".strip()


PROMPT_LIBRARY = {
    "v1": {
        "system_prompt": SYSTEM_PROMPT,
        "output_schema": OUTPUT_SCHEMA,
        "user_prompt_template": USER_PROMPT_TEMPLATE,
    },
    "v2": {
        "system_prompt": SYSTEM_PROMPT,
        "output_schema": OUTPUT_SCHEMA,
        "user_prompt_template": USER_PROMPT_TEMPLATE,
    },
}
