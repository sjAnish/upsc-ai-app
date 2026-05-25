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
    page_title="Performance Analytics",
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
st.title("📊 Performance Analytics")

# FETCH DATA
history = get_test_history()

# NO DATA
if not history:

    st.warning(
        "No test history available."
    )

else:

    # DATAFRAME
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

    # METRICS
    total_tests = len(df)

    avg_score = round(
        df["Score"].mean(),
        2
    )

    best_score = df["Score"].max()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Tests Attempted",
            total_tests
        )

    with col2:

        st.metric(
            "Average Score",
            avg_score
        )

    with col3:

        st.metric(
            "Best Score",
            best_score
        )

    st.divider()

    # TABLE
    st.subheader("📚 Test History")

    st.dataframe(
        df,
        width="stretch"
    )