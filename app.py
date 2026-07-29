import streamlit as st
import pdfplumber
import tempfile
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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


SKILLS = [
    "Python","Java","C","SQL","Machine Learning","Deep Learning",
    "Artificial Intelligence","NLP","Natural Language Processing",
    "TensorFlow","PyTorch","Scikit-learn","Pandas","NumPy",
    "Matplotlib","Seaborn","Git","GitHub","Docker","AWS",
    "Azure","GCP","IBM Cloud","MySQL","DBMS","Linux",
    "Data Structures","Algorithms","OOP","Flask","Streamlit"
]


def extract_skills(text):
    found = []

    lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower:
            found.append(skill)

    return sorted(list(set(found)))


def calculate_ats(text):

    score = 0

    lower = text.lower()

    checks = {
        "education": 10,
        "experience": 20,
        "skills": 20,
        "projects": 15,
        "certifications": 10,
        "python": 5,
        "machine learning": 10,
        "sql": 5,
        "github": 5
    }

    for word, marks in checks.items():
        if word in lower:
            score += marks

    return min(score, 100)


def match_score(resume, jd):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    emb1 = model.encode([resume])

    emb2 = model.encode([jd])

    similarity = cosine_similarity(emb1, emb2)[0][0]

    return round(similarity * 100, 2)


def missing_keywords(resume, jd):

    resume_words = set(
        re.findall(r"\b[a-zA-Z]+\b", resume.lower())
    )

    jd_words = set(
        re.findall(r"\b[a-zA-Z]+\b", jd.lower())
    )

    ignore = {
        "and","or","the","for","with","of","to","in",
        "a","an","on","is","are","be","as","by",
        "from","this","that","will","you","your"
    }

    missing = sorted(
        jd_words - resume_words - ignore
    )

    return missing[:30]


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

        ats = calculate_ats(resume_text)

        skills = extract_skills(resume_text)

        score = match_score(resume_text, job_description)

        missing = missing_keywords(
            resume_text,
            job_description
        )

        st.success("Resume Analyzed Successfully!")

        col1, col2, col3 = st.columns(3)

        col1.metric("ATS Score", f"{ats}/100")

        col2.metric("Match Score", f"{score}%")

        col3.metric("Skills Found", len(skills))

        st.divider()

        st.subheader("🛠 Skills Found")

        if skills:
            st.write(skills)
        else:
            st.warning("No known skills detected.")

        st.subheader("❌ Missing Keywords")

        if missing:
            st.write(missing)
        else:
            st.success("No important keywords missing.")

        st.subheader("💡 Suggestions")

        if ats < 70:
            st.warning("Add more projects, certifications, and technical skills.")

        if score < 70:
            st.warning("Tailor your resume to match the job description.")

        if "github" not in resume_text.lower():
            st.info("Add your GitHub profile.")

        if "linkedin" not in resume_text.lower():
            st.info("Add your LinkedIn profile.")

        if len(skills) < 10:
            st.info("Include more technical skills relevant to the role.")

        st.subheader("📄 Extracted Resume Text")

        st.text_area(
            "",
            resume_text,
            height=300
        )
