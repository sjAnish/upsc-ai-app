import streamlit as st
import feedparser
import re

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from utils.ai_service import generate_upsc_notes

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
    page_title="Current Affairs",
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

# PAGE TITLE
st.title("📰 Daily PIB Current Affairs")

# TOP FILTER BAR
# FILTER SECTION
st.subheader("📅 Filter Articles")

filter_option = st.selectbox(

    "Select Time Range",

    [
        "Today",
        "Last 7 Days",
        "Last 21 Days",
        "Custom Range"
    ]
)

# CUSTOM DATE RANGE
if filter_option == "Custom Range":

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date",
            datetime.today() - timedelta(days=7)
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            datetime.today()
        )

# RSS URL
RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=site:pib.gov.in+Press+Release&hl=en-IN&gl=IN&ceid=IN:en"
)

# FETCH FEED
feed = feedparser.parse(RSS_URL)

# ARTICLES
articles = feed.entries

# DATE FILTER LOGIC
filtered_articles = []

today = datetime.today()

for article in articles:

    try:

        article_date = datetime.strptime(

            article.published,

            "%a, %d %b %Y %H:%M:%S %Z"
        )

    except:

        continue

    # TODAY
    if filter_option == "Today":

        if article_date.date() == today.date():

            filtered_articles.append(article)

    # LAST 7 DAYS
    elif filter_option == "Last 7 Days":

        if article_date >= today - timedelta(days=7):

            filtered_articles.append(article)

    # LAST 21 DAYS
    elif filter_option == "Last 21 Days":

        if article_date >= today - timedelta(days=21):

            filtered_articles.append(article)

    # CUSTOM RANGE
    elif filter_option == "Custom Range":

        if start_date <= article_date.date() <= end_date:

            filtered_articles.append(article)

# REPLACE ARTICLES
articles = filtered_articles

st.write(f"Articles fetched: {len(articles)}")

# IGNORE NON-UPSC ARTICLES
ignore_keywords = [
    "recruitment",
    "vacancy",
    "tender",
    "auction",
    "holiday",
    "bid",
    "corrigendum"
]

count = 0

# LOOP ARTICLES
for article in articles:

    if count >= 10:
        break

    title_lower = article.title.lower()

    # SKIP USELESS ARTICLES
    if any(word in title_lower for word in ignore_keywords):
        continue

    # CLEAN HTML SUMMARY
    clean_summary = BeautifulSoup(
        article.summary,
        "html.parser"
    ).get_text()

    # ARTICLE CARD
    with st.container(border=True):

        # TITLE
        st.markdown(f"## {article.title}")

        # DATE
        if hasattr(article, "published"):
            st.caption(article.published)

        # SUMMARY
        st.write(clean_summary)

        # OPEN ARTICLE BUTTON
        st.link_button(
            "🔗 Open Full Article",
            article.link
        )

        st.divider()

        # GENERATE NOTES BUTTON
        if st.button(
            "🧠 Generate UPSC Notes",
            key=article.link
        ):

            with st.spinner("Generating UPSC Notes..."):

                try:

                    # AI NOTES
                    notes = generate_upsc_notes(
                        clean_summary
                    )

                    st.success(
                        "Notes Generated Successfully ✅"
                    )

                    # CREATE TABS
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📌 Prelims",
                        "📝 Mains",
                        "❓ MCQs",
                        "📚 Revision"
                    ])

                    # REGEX EXTRACTION

                    prelims_match = re.search(
                        r"Prelims Focus(.*?)(Mains Analysis|$)",
                        notes,
                        re.DOTALL | re.IGNORECASE
                    )

                    mains_match = re.search(
                        r"Mains Analysis(.*?)(UPSC MCQs|$)",
                        notes,
                        re.DOTALL | re.IGNORECASE
                    )

                    mcqs_match = re.search(
                        r"UPSC MCQs(.*?)(Revision Notes|$)",
                        notes,
                        re.DOTALL | re.IGNORECASE
                    )

                    revision_match = re.search(
                        r"Revision Notes(.*)",
                        notes,
                        re.DOTALL | re.IGNORECASE
                    )

                    # SAFE EXTRACTION

                    prelims = (
                        prelims_match.group(1).strip()
                        if prelims_match else
                        "No Prelims Notes Found"
                    )

                    mains = (
                        mains_match.group(1).strip()
                        if mains_match else
                        "No Mains Analysis Found"
                    )

                    mcqs = (
                        mcqs_match.group(1).strip()
                        if mcqs_match else
                        "No MCQs Found"
                    )

                    revision = (
                        revision_match.group(1).strip()
                        if revision_match else
                        "No Revision Notes Found"
                    )

                    # DISPLAY TABS

                    with tab1:
                        st.markdown(prelims)

                    with tab2:
                        st.markdown(mains)

                    with tab3:
                        st.markdown(mcqs)

                    with tab4:
                        st.markdown(revision)

                except Exception as e:

                    st.error(f"Error: {e}")

    count += 1

# NO ARTICLES
if count == 0:
    st.warning("No useful PIB articles found.")