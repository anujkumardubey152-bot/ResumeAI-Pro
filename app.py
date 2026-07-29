import streamlit as st
import pdfplumber
import tempfile
import re

from collections import Counter

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ResumeAI Pro")

st.caption("AI Powered ATS Resume Analyzer")

st.markdown("---")
uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

analyze = st.button(
    "Analyze Resume",
    use_container_width=True
)
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text
    SKILLS = [

"Python","Java","C","C++","SQL","R",

"Machine Learning",
"Deep Learning",
"Artificial Intelligence",
"NLP",
"Natural Language Processing",

"TensorFlow",
"PyTorch",
"Keras",

"Scikit-learn",

"Pandas",

"NumPy",

"Matplotlib",

"Seaborn",

"Plotly",

"OpenCV",

"Flask",

"Django",

"FastAPI",

"Git",

"GitHub",

"Docker",

"Kubernetes",

"AWS",

"Azure",

"GCP",

"IBM Cloud",

"MySQL",

"PostgreSQL",

"MongoDB",

"SQLite",

"Linux",

"Power BI",

"Excel",

"Data Analysis",

"EDA",

"Feature Engineering",

"Feature Selection",

"Classification",

"Regression",

"Clustering",

"Decision Tree",

"Random Forest",

"XGBoost",

"LightGBM",

"Neural Networks",

"LLM",

"Generative AI",

"Prompt Engineering",

"LangChain",

"Transformers",

"HuggingFace",

"Statistics",

"Probability",

"Data Structures",

"Algorithms",

"OOP",

"DBMS",

"Operating Systems",

"Computer Vision",

"Reinforcement Learning",

"Time Series",

"REST API",

"Streamlit"

]
def calculate_ats(text):

    score = 0

    lower=text.lower()

    rules={

        "education":10,

        "experience":20,

        "skills":15,

        "projects":15,

        "certifications":10,

        "python":5,

        "machine learning":10,

        "sql":5,

        "github":5,

        "linkedin":5

    }

    for keyword,points in rules.items():

        if keyword in lower:

            score+=points

    return min(score,100)
    @st.cache_resource
     def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

model=load_model()
def calculate_match(resume,jd):

    resume_embedding=model.encode([resume])

    jd_embedding=model.encode([jd])

    similarity=cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    return round(similarity*100,2)
    def missing_keywords(resume,jd):

    resume_words=set(
        re.findall(r"\b[a-zA-Z]+\b",resume.lower())
    )

    jd_words=set(
        re.findall(r"\b[a-zA-Z]+\b",jd.lower())
    )

    stopwords={

        "the","and","or","to","a","of","for",
        "with","is","are","be","an","on",
        "in","by","this","that"

    }

    missing=sorted(

        jd_words-resume_words-stopwords

    )

    return missing[:25]
    def detect_sections(text):

    lower=text.lower()

    sections=[]

    possible=[

        "summary",

        "skills",

        "experience",

        "projects",

        "education",

        "certifications",

        "awards",

        "languages"

    ]

    for section in possible:

        if section in lower:

            sections.append(section.title())

    return sections
    def suggestions(score,skills):

    tips=[]

    if score<70:
        tips.append("Increase ATS keywords.")

    if len(skills)<10:
        tips.append("Add more technical skills.")

    if "Docker" not in skills:
        tips.append("Learning Docker can improve many AI/ML resumes.")

    if "AWS" not in skills:
        tips.append("Cloud skills such as AWS or Azure are valuable.")

    return tips
    if analyze:

    if uploaded_resume is None:

        st.error("Please upload a resume.")

    elif job_description.strip() == "":

        st.error("Please paste a job description.")

    else:

        with st.spinner("Analyzing Resume..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

                tmp.write(uploaded_resume.read())

                resume_path = tmp.name

            resume_text = extract_text(resume_path)

            ats = calculate_ats(resume_text)

            match = calculate_match(
                resume_text,
                job_description
            )

            skills = extract_skills(
                resume_text
            )

            missing = missing_keywords(
                resume_text,
                job_description
            )

            sections = detect_sections(
                resume_text
            )

            tips = suggestions(
                ats,
                skills
            )

        st.success("Resume Analysis Completed!")

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "ATS Score",
            f"{ats}/100"
        )

        col2.metric(
            "Match Score",
            f"{match}%"
        )

        col3.metric(
            "Skills Found",
            len(skills)
        )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("📌 Resume Sections")

            if sections:

                for sec in sections:

                    st.success(sec)

            else:

                st.warning("No sections detected.")

            st.subheader("🛠 Skills Found")

            if skills:

                st.write(skills)

            else:

                st.warning("No skills detected.")

        with right:

            st.subheader("❌ Missing Keywords")

            if missing:

                st.write(missing)

            else:

                st.success("No important keywords missing.")

            st.subheader("💡 Suggestions")

            if tips:

                for tip in tips:

                    st.info(tip)

            else:

                st.success("Excellent Resume!")

        st.divider()

        st.subheader("📄 Resume Preview")

        st.text_area(
            "",
            resume_text,
            height=350
        )
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

    return "F"
    def strengths(skills, ats):

    good = []

    if ats >= 80:
        good.append("Strong ATS compatibility")

    if len(skills) >= 15:
        good.append("Good technical skill coverage")

    if "Python" in skills:
        good.append("Python detected")

    if "Machine Learning" in skills:
        good.append("Machine Learning experience")

    if "GitHub" in skills:
        good.append("GitHub profile included")

    return good
    def weaknesses(skills, missing):

    bad = []

    if "Docker" not in skills:
        bad.append("Docker not found")

    if "AWS" not in skills:
        bad.append("AWS not found")

    if "TensorFlow" not in skills:
        bad.append("TensorFlow not found")

    if len(missing) > 15:
        bad.append("Many job description keywords are missing")

    return bad
    def skill_coverage(skills):

    return round((len(skills) / len(SKILLS)) * 100, 1)
    def keyword_coverage(jd, missing):

    total = len(set(re.findall(r"\b[a-zA-Z]+\b", jd.lower())))

    if total == 0:
        return 0

    covered = total - len(missing)

    return round((covered / total) * 100, 1)
    grade = resume_grade(ats)

strength = strengths(
    skills,
    ats
)

weak = weaknesses(
    skills,
    missing
)

skill_percent = skill_coverage(
    skills
)

keyword_percent = keyword_coverage(
    job_description,
    missing
)
tabs = st.tabs([
    "📊 Overview",
    "🛠 Skills",
    "🔑 Keywords",
    "📄 Resume"
])
with tabs[0]:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("ATS", f"{ats}/100")

    col2.metric("Match", f"{match}%")

    col3.metric("Grade", grade)

    col4.metric("Skills", len(skills))

    st.markdown("### ATS Progress")

    st.progress(ats / 100)

    st.markdown("### Match Progress")

    st.progress(match / 100)

    st.markdown("### Skill Coverage")

    st.progress(skill_percent / 100)

    st.markdown("### Keyword Coverage")

    st.progress(keyword_percent / 100)
    with tabs[1]:

    st.subheader("Detected Skills")

    st.write(skills)

    st.divider()

    st.subheader("Strengths")

    for item in strength:

        st.success(item)

    st.subheader("Weaknesses")

    for item in weak:

        st.warning(item)
        with tabs[2]:

    st.subheader("Missing Keywords")

    if missing:

        st.write(missing)

    else:

        st.success("No important keywords missing.")

    st.divider()

    st.subheader("Suggestions")

    for tip in tips:

        st.info(tip)
        with tabs[3]:

    st.subheader("Detected Sections")

    st.write(sections)

    st.divider()

    st.text_area(
        "Resume Text",
        resume_text,
        height=500
    )
    
    
