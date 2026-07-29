import re
import streamlit as st
import pdfplumber
import tempfile
from docx import Document

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:

    st.title("🤖 ResumeAI Pro")

    st.markdown("---")

    st.write("### Features")

    st.success("✔ PDF Support")
    st.success("✔ DOCX Support")
    st.info("ATS Analysis")
    st.info("Resume Matching")
    st.info("AI Suggestions")
    st.info("Analytics Dashboard")

    st.markdown("---")

    st.write("Version 1.0")

# ----------------------------
# HEADER
# ----------------------------

st.title("🤖 ResumeAI Pro")

st.subheader("AI Powered ATS Resume Analyzer")

st.markdown("---")

# ----------------------------
# INPUTS
# ----------------------------

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=220
)

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# ----------------------------
# PDF READER
# ----------------------------

def read_pdf(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text

# ----------------------------
# DOCX READER
# ----------------------------

def read_docx(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text

# ----------------------------
# MAIN
# ----------------------------

if analyze:

    if uploaded_resume is None:

        st.error("Please upload a resume.")

    elif job_description.strip() == "":

        st.error("Please paste a Job Description.")

    else:

        with st.spinner("Reading Resume..."):

            if uploaded_resume.name.endswith(".pdf"):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(uploaded_resume.read())

                    resume_text = read_pdf(tmp.name)

            else:

                resume_text = read_docx(uploaded_resume)

        st.success("Resume Loaded Successfully!")

        st.markdown("---")

        st.subheader("Resume Preview")

        st.text_area(
            "",
            resume_text,
            height=500
        )

        st.markdown("---")

        st.subheader("Job Description")

        st.text_area(
            "",
            job_description,
            height=300
        )
        def calculate_ats_score(text):

    score = 0
    text = text.lower()

    weights = {
        "summary": 10,
        "skills": 15,
        "experience": 20,
        "projects": 15,
        "education": 10,
        "certifications": 10,
        "python": 5,
        "machine learning": 5,
        "sql": 5,
        "github": 5
    }

    for keyword, points in weights.items():
        if keyword in text:
            score += points

    return min(score, 100)
    def resume_grade(score):

    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"
        def detect_contact(text):

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    phone = re.findall(
        r"(?:\+91[- ]?)?[6-9]\d{9}",
        text
    )

    return (
        email[0] if email else "Not Found",
        phone[0] if phone else "Not Found"
    )
    def detect_sections(text):

    sections = []

    keywords = [
        "summary",
        "skills",
        "experience",
        "projects",
        "education",
        "certifications",
        "awards",
        "languages"
    ]

    lower = text.lower()

    for item in keywords:

        if item in lower:
            sections.append(item.title())

    return sections
    def detect_education(text):

    education = [
        "Bachelor",
        "Master",
        "B.Tech",
        "M.Tech",
        "B.E",
        "MCA",
        "BCA",
        "MBA",
        "PhD"
    ]

    found = []

    for degree in education:

        if degree.lower() in text.lower():
            found.append(degree)

    return found
    def detect_experience(text):

    keywords = [
        "intern",
        "internship",
        "experience",
        "worked",
        "developer",
        "engineer",
        "analyst"
    ]

    total = 0

    lower = text.lower()

    for word in keywords:

        if word in lower:
            total += 1

    return total
    resume_text = read_pdf(...)
    ats = calculate_ats_score(resume_text)

grade = resume_grade(ats)

email, phone = detect_contact(resume_text)

sections = detect_sections(resume_text)

education = detect_education(resume_text)

experience = detect_experience(resume_text)
st.success("Resume Loaded Successfully!")

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric(
    "ATS Score",
    f"{ats}/100"
)

col2.metric(
    "Grade",
    grade
)

col3.metric(
    "Experience Indicators",
    experience
)

st.progress(ats / 100)

st.markdown("---")
left, right = st.columns(2)

with left:

    st.subheader("Contact")

    st.write("📧", email)

    st.write("📞", phone)

    st.subheader("Education")

    if education:
        st.success(", ".join(education))
    else:
        st.warning("Not Detected")

with right:

    st.subheader("Sections")

    if sections:

        for section in sections:

            st.success(section)

    else:

        st.warning("No Sections Found")
        st.markdown("---")

st.subheader("Resume Preview")

st.text_area(
    "",
    resume_text,
    height=450
)

        
