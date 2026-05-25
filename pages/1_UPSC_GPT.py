import streamlit as st

from groq import Groq
from dotenv import load_dotenv
import os

# LOAD GLOBAL CSS
def load_css():

    with open(".streamlit/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )

load_css()

# LOAD ENV VARIABLES
load_dotenv()

# CREATE GROQ CLIENT
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PAGE CONFIG
st.set_page_config(
    page_title="UPSC GPT",
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
st.title("🤖 UPSC GPT")

st.markdown("""
Ask anything related to:

- UPSC Current Affairs
- Answer Writing
- Prelims MCQs
- Ethics
- Essay
- CSAT
""")

st.divider()

# SESSION STATE
if "messages" not in st.session_state:

    st.session_state.messages = []

# INPUT BOX SECTION
with st.container():

    col1, col2 = st.columns([12, 1])

    with col1:

        prompt = st.text_input(

            "Ask your question",

            placeholder="Type your UPSC question here..."
        )

    with col2:

        st.markdown("<br>", unsafe_allow_html=True)

        ask_button = st.button("➤")

st.markdown("<br>", unsafe_allow_html=True)

# DISPLAY OLD CHAT MESSAGES
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# PROCESS USER INPUT
if ask_button and prompt:

    # SAVE USER MESSAGE
    st.session_state.messages.append({

        "role": "user",

        "content": prompt
    })

    # DISPLAY USER MESSAGE
    with st.chat_message("user"):

        st.markdown(prompt)

    # AI RESPONSE
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                # SYSTEM PROMPT
                system_prompt = """
                You are an expert UPSC Civil Services mentor.

                Your answers must be:
                - UPSC oriented
                - analytical
                - structured
                - concise but informative

                For mains answers:
                - Introduction
                - Body
                - Conclusion

                For prelims:
                - Explain concepts clearly

                Use headings, subheadings and bullet points.

                Keep answers crisp and exam focused.
                """

                # API CALL
                completion = client.chat.completions.create(

                    model="llama-3.1-8b-instant",

                    messages=[

                        {
                            "role": "system",
                            "content": system_prompt
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.3,

                    max_tokens=1200,

                    timeout=60
                )

                # EXTRACT RESPONSE
                response = (

                    completion
                    .choices[0]
                    .message.content
                )

                # DISPLAY RESPONSE
                st.markdown(response)

                # SAVE RESPONSE
                st.session_state.messages.append({

                    "role": "assistant",

                    "content": response
                })

            except Exception as e:

                st.error("""
⚠️ Connection/API issue occurred.

Possible reasons:
- Internet fluctuation
- Groq temporary overload
- API timeout
- Too many requests

Please retry after few seconds.
""")

                st.exception(e)

                