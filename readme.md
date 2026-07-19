# SOP AI Training System

SOP AI Training System is a simple Streamlit MVP that turns SOP documents into structured training assets using the Google Gemini API.

## What it does

- Accepts SOP input as pasted text or uploaded `.txt` / `.pdf` files
- Generates concise SOP summaries
- Produces beginner-friendly step-by-step training instructions
- Creates scenario-based quiz questions with answers and explanations
- Lets users download results as `.json` or `.txt`

## Project structure

- `main.py`: Streamlit entry point and UI
- `prompts.py`: Prompt library with `v1` and improved `v2`
- `utils.py`: File parsing, Gemini calls, JSON cleanup, and export helpers
- `requirements.txt`: Python dependencies

## How to run

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

PowerShell:

```powershell
python -m pip install -r requirements.txt
```

3. Set your Gemini API key:

```bash
export GEMINI_API_KEY="your_api_key"
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key"
```

You can also store the API key in Streamlit secrets:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_api_key"
```

4. Start the app:

```bash
streamlit run main.py
```

If the app shows a missing dependency warning, install packages into the same Python interpreter that runs Streamlit. A reliable Windows check is:

```powershell
python -m streamlit run main.py
```

## Example input

```text
Before opening the store, the supervisor verifies alarm deactivation, checks the cash drawer, inspects safety hazards, and confirms staffing coverage. If the register count is short, the supervisor must escalate to the manager before sales begin.
```

## Example output shape

```json
{
  "summary": [
    "Store opening starts with security and safety checks.",
    "The supervisor verifies the cash drawer before operations begin."
  ],
  "training_steps": [
    "Confirm the alarm is deactivated before entering normal operations.",
    "Decision Point: If the register count is short, escalate to the manager before opening sales."
  ],
  "quiz": [
    {
      "question": "You find the register count is short during opening. What should you do next?",
      "answer": "Pause opening actions and escalate to the manager.",
      "explanation": "The SOP requires escalation before sales begin when the count is short."
    }
  ]
}
```

## Notes

- The default model is `gemini-2.5-flash`, but the UI lets you switch to another compatible Gemini model.
- The app has no demo fallback. If `GEMINI_API_KEY` is missing, it shows an error instead of generating placeholder output.
- Prompt `v2` is the recommended version because it gives more explicit guidance around decision points, checks, and beginner-level training.
