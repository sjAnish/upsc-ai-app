import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re

from data.database import save_test_result

# LOAD GLOBAL CSS
def load_css():

    with open(".streamlit/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )

load_css()

# LOAD ENV
load_dotenv()

# GROQ CLIENT
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PAGE CONFIG
st.set_page_config(
    page_title="AI Test Generator",
    page_icon="assets/ashoka_logo.jpg",
    layout="wide"
)

hide_streamlit_style = """

<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

</style>

"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

# TITLE
st.title("📝 AI Test Generator")

st.markdown("""
Practice AI-generated mock tests for:

- UPSC Prelims
- BPSC Prelims
- CSAT
""")

# TOP FILTERS
col1, col2 = st.columns(2)

col3, col4 = st.columns(2)

with col1:

    exam_type = st.selectbox(

        "Exam",

        [
            "UPSC Prelims",
            "BPSC Prelims",
            "CSAT"
        ]
    )

with col2:

    subject = st.selectbox(

        "Subject",

        [
            "Polity",
            "History",
            "Geography",
            "Economy",
            "Environment",
            "Science & Tech",
            "Current Affairs",
            "Mixed"
        ]
    )

with col3:

    difficulty = st.selectbox(

        "Difficulty",

        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

with col4:

    question_count = st.selectbox(

        "Questions",

        [5, 10, 15, 20]
    )

# GENERATE TEST
if st.button("Generate AI Test"):

    with st.spinner("Generating Questions..."):

        try:

            prompt = f"""
            Generate {question_count} MCQs for:

            Exam: {exam_type}
            Subject: {subject}
            Difficulty: {difficulty}

            STRICT FORMAT:

            Q1. Question text

            A. option
            B. option
            C. option
            D. option

            Answer: A

            Explanation: short explanation

            Repeat properly for all questions.
            """

            completion = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.4,

                max_tokens=4000
            )

            response = (
                completion
                .choices[0]
                .message.content
            )

            # STORE QUIZ
            st.session_state["quiz_data"] = response

        except Exception as e:

            st.error(f"Error: {e}")

# DISPLAY QUIZ
if "quiz_data" in st.session_state:

    raw_text = st.session_state["quiz_data"]

    # SPLIT QUESTIONS
    questions = re.split(
        r"\nQ\d+\.",
        raw_text
    )

    # REMOVE EMPTY
    questions = [
        q.strip()
        for q in questions
        if q.strip()
    ]

    user_answers = {}

    correct_answers = {}

    explanations = {}

    st.divider()

    st.subheader("Attempt Test")

    # QUESTION LOOP
    for idx, q in enumerate(questions):

        lines = q.split("\n")

        question_text = lines[0]

        options = []

        answer = ""

        explanation = ""

        for line in lines:

            line = line.strip()

            if line.startswith("A."):

                options.append(line)

            elif line.startswith("B."):

                options.append(line)

            elif line.startswith("C."):

                options.append(line)

            elif line.startswith("D."):

                options.append(line)

            elif line.startswith("Answer:"):

                answer = (
                    line
                    .replace("Answer:", "")
                    .strip()
                )

            elif line.startswith("Explanation:"):

                explanation = (
                    line
                    .replace("Explanation:", "")
                    .strip()
                )

        correct_answers[idx] = answer

        explanations[idx] = explanation

        # QUESTION CARD
        with st.container(border=True):

            st.markdown(
                f"### Q{idx+1}. {question_text}"
            )

            selected = st.radio(

                "Select Answer",

                options,

                key=f"q_{idx}",

                index=None,

                label_visibility="collapsed"
            )

            user_answers[idx] = selected

    # SUBMIT TEST
    if st.button("Submit Test"):

        score = 0

        unanswered = 0

        st.divider()

        st.subheader("Result Analysis")

        # SCORE CALCULATION
        for idx, selected in user_answers.items():

            if selected is None:

                chosen_option = ""

                unanswered += 1

            else:

                chosen_option = selected[0]

            correct_option = correct_answers[idx]

            if chosen_option == correct_option:

                score += 1

        # SAVE TO DATABASE
        save_test_result(

            exam_type,
            subject,
            difficulty,
            score,
            len(questions)
        )

        # SCORE DISPLAY
        st.success(
            f"Your Score: {score} / {len(questions)}"
        )

        st.warning(
            f"Unanswered Questions: {unanswered}"
        )

        st.progress(
            score / len(questions)
        )

        st.divider()

        # DETAILED ANALYSIS
        for idx, selected in user_answers.items():

            if selected is None:

                chosen_option = ""

            else:

                chosen_option = selected[0]

            correct_option = correct_answers[idx]

            with st.container(border=True):

                st.markdown(f"### Q{idx+1}")

                st.write(
                    f"Your Answer: {chosen_option}"
                )

                st.write(
                    f"Correct Answer: {correct_option}"
                )

                if chosen_option == correct_option:

                    st.success("Correct ✅")

                else:

                    st.error("Incorrect ❌")

                st.info(
                    explanations[idx]
                )