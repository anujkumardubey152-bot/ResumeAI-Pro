import streamlit as st

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ResumeAI Pro")
st.subheader("AI-Powered ATS Resume Analyzer")

st.markdown("---")

uploaded_resume = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "💼 Paste Job Description",
    height=250
)

analyze_button = st.button("🚀 Analyze Resume")
