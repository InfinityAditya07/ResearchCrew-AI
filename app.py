import streamlit as st

from agents import get_groq_api_key, run_crew


def main() -> None:
    st.set_page_config(
        page_title="ResearchCrew AI",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("ResearchCrew AI - Multi Agent Research Assistant")

    with st.sidebar:
        st.header("Agents")
        st.markdown(
            """
- **Researcher Agent**: Research a given topic thoroughly  
- **Analyst Agent**: Analyze research and extract key insights  
- **Report Writer Agent**: Write a clean, structured report  
""".strip()
        )

    if "final_report" not in st.session_state:
        st.session_state.final_report = ""
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = ""

    api_key = get_groq_api_key()
    if not api_key:
        st.error(
            "Missing **`GROQ_API_KEY`**. Add it to your `.env` file (see `.env.example`), then rerun the app."
        )
        st.info(
            "Example:\n\n"
            "```\n"
            "GROQ_API_KEY=your_key_here\n"
            "```"
        )
        return

    topic = st.text_input(
        "Enter a research topic",
        value=st.session_state.last_topic,
        placeholder="e.g., Impact of quantum computing on cryptography",
    )

    start_disabled = not topic.strip()
    if st.button("Start Research", type="primary", disabled=start_disabled):
        st.session_state.last_topic = topic.strip()
        try:
            with st.spinner("Agents are working..."):
                st.session_state.final_report = run_crew(st.session_state.last_topic)
        except Exception as e:
            st.session_state.final_report = ""
            st.error("Research run failed. See details below.")
            st.exception(e)
            return

    if st.session_state.final_report:
        st.subheader("Final Report")
        st.container(border=True).markdown(st.session_state.final_report)


if __name__ == "__main__":
    main()

