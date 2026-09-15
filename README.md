# DP-600 Prep Hub

A Streamlit + Gemini practice workspace built directly from Microsoft's official
**Exam DP-600: Implementing Analytics Solutions Using Microsoft Fabric** skills-measured
outline (skills measured as of July 21, 2026). Every one of the exam's three skill areas
gets its own practice track, its own prompts, and its own analytics — none is treated as
secondary, and each is weighted the way the real exam weights it.

## Skill areas (mirrors the skills-measured outline exactly)

| # | Skill area | Exam weight | Page/Route |
|---|------------|-------------|------------|
| 1 | Maintain a Data Analytics Solution | 25–30% | `pages/maintain_solution.py` |
| 2 | Prepare Data | 45–50% | `pages/prepare_data.py` |
| 3 | Implement and Manage Semantic Models | 25–30% | `pages/semantic_models.py` |

Topic lists inside each skill area (see `utils/helpers.py::PRACTICE_BLUEPRINTS`) are taken
line-by-line from the DP-600 skills-measured outline, grouped into logical subtopics
(e.g. "Get Data" / "Transform Data" / "Query & Analyze Data" under Prepare Data).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in GEMINI_API_KEY (required) and MONGODB_URI (optional, else CSV logging is used)
streamlit run app.py
```

## How it works

- Each skill area has its own **system prompt** and **generation prompt** under
  `prompts/`, scoped strictly to that skill area's content so Gemini never drifts
  off-syllabus.
- Questions are returned as schema-validated JSON (`schemas/generation_schema.json`)
  and stored either in MongoDB (`database/mongodb.py`) or as local CSV logs
  (`utils/csv_logger.py`) — whichever is configured.
- Difficulty adapts per skill area: accuracy above 80% raises difficulty, accuracy below
  50% lowers it (`utils/helpers.py::recommend_difficulty`).
- `pages/dashboard.py` shows attempt coverage across all 3 skill areas so you can spot
  which parts of the exam you're neglecting — especially "Prepare Data", which carries
  the largest share of the exam (45–50%).

## Customizing prompts or topics

- Add/edit topics: `utils/helpers.py::PRACTICE_BLUEPRINTS`.
- Change how questions are written: edit the relevant
  `prompts/<skill_area>_system_prompt.txt` and
  `prompts/<skill_area>_generate_question.txt` files.
- Change the visual theme: `utils/streamlit_support.py::apply_brand_styles`.
