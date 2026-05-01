# ResearchCrew AI

ResearchCrew AI is a simple **multi-agent research assistant**. You enter a topic, then three AI agents work in sequence to produce a structured final report:

1. **Researcher Agent** → gathers thorough research on the topic  
2. **Analyst Agent** → extracts key insights from the research  
3. **Report Writer Agent** → writes a clean, structured report from the analysis  

## Tech stack

- **Python**
- **CrewAI** (agents, tasks, orchestration)
- **Streamlit** (UI)
- **Groq** (LLM provider)

## How to run

1. Create and activate a virtual environment (already created as `.venv/` if you followed the setup):

```bash
cd "ResearchCrew AI"
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Groq API key:

- Copy `.env.example` to `.env`
- Fill in your real key:

```bash
GROQ_API_KEY=your_key_here
```

Optional: choose a Groq model (defaults to `groq/llama-3.3-70b-versatile`):

```bash
GROQ_MODEL=groq/llama-3.3-70b-versatile
```

4. Start the Streamlit app:

```bash
streamlit run app.py
```

## How the multi-agent architecture works here

This project uses CrewAI’s **sequential** process:

- The UI calls `run_crew(topic)` in `agents.py`.
- `run_crew` builds three **tasks** mapped to three **agents**.
- Tasks run in order (`Process.sequential`):
  - `research_task` runs first.
  - `analysis_task` runs next and receives `research_task` output as context.
  - `report_task` runs last and receives `analysis_task` output as context.
- The final return value is the **report writer**’s output (the final report displayed in the UI).

