import streamlit as st
import pdfplumber
import tempfile

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ResumeAI Pro")
st.subheader("AI-Powered ATS Resume Analyzer")

uploaded_resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "💼 Paste Job Description",
    height=250
)

analyze = st.button("🚀 Analyze Resume")


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


if analyze:

    if uploaded_resume is None:

        st.error("Please upload a resume.")

    elif job_description.strip() == "":

        st.error("Please paste a job description.")

    else:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

            tmp.write(uploaded_resume.read())

            resume_path = tmp.name

        resume_text = extract_text(resume_path)

        st.success("Resume Parsed Successfully!")

        st.subheader("📄 Extracted Resume Text")

        st.text_area(
            "",
            resume_text,
            height=350
        )
