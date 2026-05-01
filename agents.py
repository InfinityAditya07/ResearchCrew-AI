import os

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv


load_dotenv()


def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "")


def get_groq_model() -> str:
    # Allow easy model swaps when Groq deprecates models.
    return os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")


groq_llm = LLM(
    model=get_groq_model(),
    api_key=get_groq_api_key(),
)


researcher_agent = Agent(
    role="Researcher Agent",
    goal="Research a given topic thoroughly and compile accurate, relevant information.",
    backstory="You are a meticulous researcher who prioritizes credible sources and comprehensive coverage.",
    llm=groq_llm,
)

analyst_agent = Agent(
    role="Analyst Agent",
    goal="Analyze the research and extract key insights, patterns, and implications.",
    backstory="You are an analytical thinker who synthesizes information into clear, actionable insights.",
    llm=groq_llm,
)

report_writer_agent = Agent(
    role="Report Writer Agent",
    goal="Write a clean, structured report based on the analysis with clear sections and conclusions.",
    backstory="You are an excellent technical writer who turns complex analysis into a well-organized report.",
    llm=groq_llm,
)


def run_crew(topic: str) -> str:
    research_task = Task(
        description=(
            "Research the topic: {topic}. Provide a thorough, factual summary with clear bullet points, "
            "key terms, and relevant background. Prefer credible sources and note any uncertainties."
        ),
        expected_output=(
            "A well-structured research brief including: overview, key facts, important context, "
            "and a list of notable findings."
        ),
        agent=researcher_agent,
    )

    analysis_task = Task(
        description=(
            "Analyze the research findings for {topic}. Extract the most important insights, patterns, "
            "trade-offs, and implications. Identify what matters most and why."
        ),
        expected_output=(
            "A concise analysis with key insights, supporting reasoning, and implications. "
            "Include any risks, unknowns, and recommended next questions."
        ),
        agent=analyst_agent,
        context=[research_task],
    )

    report_task = Task(
        description=(
            "Write a clean, structured report on {topic} using the analysis. Use headings, short paragraphs, "
            "and bullet points where helpful. End with clear conclusions and next steps."
        ),
        expected_output=(
            "A polished report with sections (Executive summary, Key findings, Analysis, Conclusions, Next steps)."
        ),
        agent=report_writer_agent,
        context=[analysis_task],
    )

    crew = Crew(
        agents=[researcher_agent, analyst_agent, report_writer_agent],
        tasks=[research_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff(inputs={"topic": topic})
    return str(result)

