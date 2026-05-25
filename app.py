import streamlit as st
import pandas as pd

from data.database import get_test_history

# LOAD GLOBAL CSS
def load_css():

    with open(".streamlit/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )

load_css()

# PAGE CONFIG
st.set_page_config(
    page_title="UPSC AI Dashboard",
    page_icon="assets/ashoka_logo.png",
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

# CUSTOM CSS
st.markdown("""

<style>

.main {
    background-color: #f5f7fb;
}

.metric-card {

    background: white;

    padding: 25px;

    border-radius: 15px;

    box-shadow: 0 4px 12px rgba(0,0,0,0.08);

    text-align: center;
}

.feature-card {

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    padding: 25px;

    border-radius: 18px;

    color: white;

    text-align: center;

    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}

</style>

""", unsafe_allow_html=True)

# HEADER
st.title(" Welcome to UPSC World")

st.markdown("""
Your Personalized UPSC Intelligence Workspace
""")

st.divider()

# FETCH TEST HISTORY
history = get_test_history()

# METRICS
if history:

    df = pd.DataFrame(

        history,

        columns=[
            "ID",
            "Exam",
            "Subject",
            "Difficulty",
            "Score",
            "Total Questions",
            "Created At"
        ]
    )

    total_tests = len(df)

    avg_score = round(
        df["Score"].mean(),
        2
    )

    best_score = df["Score"].max()

else:

    total_tests = 0
    avg_score = 0
    best_score = 0

# METRIC CARDS
col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""

    <div class="metric-card">

    <h2>📝 Tests Attempted</h2>

    <h1>{total_tests}</h1>

    </div>

    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""

    <div class="metric-card">

    <h2>📊 Average Score</h2>

    <h1>{avg_score}</h1>

    </div>

    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""

    <div class="metric-card">

    <h2>🏆 Best Score</h2>

    <h1>{best_score}</h1>

    </div>

    """, unsafe_allow_html=True)

st.divider()

# FEATURE SECTION
st.subheader("⚡ Quick Access")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""

    <div class="feature-card">

    <h2>📰 Current Affairs</h2>

    <p>
    Daily PIB + AI Notes + Revision
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/2_Current_Affairs.py",
        label="Open Current Affairs"
    )

with col2:

    st.markdown("""

    <div class="feature-card">

    <h2>🤖 UPSC GPT</h2>

    <p>
    AI Mentor + Doubt Solver
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/1_UPSC_GPT.py",
        label="Open UPSC GPT"
    )

col3, col4 = st.columns(2)

with col3:

    st.markdown("""

    <div class="feature-card">

    <h2>🗺️ AI Maps</h2>

    <p>
    Interactive Geography Revision
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/4_AI_Maps.py",
        label="Open Maps"
    )

with col4:

    st.markdown("""

    <div class="feature-card">

    <h2>📝 Test Generator</h2>

    <p>
    AI Mock Tests + Analytics
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.page_link(
        "pages/3_Practice_Tests.py",
        label="Open Test Generator"
    )

st.divider()

# DAILY TARGETS
st.subheader("🎯 Today's Targets")

col1, col2 = st.columns(2)

with col1:

    st.checkbox("20 MCQs Practice")

    st.checkbox("1 Current Affairs Revision")

    st.checkbox("1 Mains Answer Writing")

with col2:

    st.checkbox("Map Revision")

    st.checkbox("Read Newspaper")

    st.checkbox("CSAT Practice")

st.divider()

# MOTIVATION
st.subheader("🔥 Daily Motivation")

st.info("""
Consistency beats intensity.

Small daily improvements create massive UPSC results over time.
""")