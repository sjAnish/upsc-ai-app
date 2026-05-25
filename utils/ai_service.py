from groq import Groq
from dotenv import load_dotenv
import os


# LOAD ENV VARIABLES
load_dotenv()

# CREATE GROQ CLIENT
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_upsc_notes(article_text):

    prompt = f"""
You are an expert UPSC Civil Services mentor.

Analyze the following current affairs article strictly from UPSC exam perspective.

Generate response in EXACTLY this format:

# 📌 Prelims Focus
- 5 concise factual points
- Mention important organizations, reports, conventions, species, locations, indices, schemes etc.
- Avoid long explanations

# 📝 Mains Analysis
Include:
- Background
- Importance
- Challenges/Issues
- Government Steps
- Way Forward
- Conclusion

Keep it analytical and UPSC GS answer oriented.

# ❓ UPSC MCQs
Generate:
- 2 high-quality prelims MCQs
- Include options
- Give correct answer with explanation

# 📚 Revision Notes
Generate:
- 5 one-line revision bullets
- Crisp and memory-oriented

Current Affairs Article:
{article_text}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content