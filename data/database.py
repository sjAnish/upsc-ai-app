import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect(
    "upsc_app.db",
    check_same_thread=False
)

cursor = conn.cursor()

# CREATE TEST HISTORY TABLE
cursor.execute("""

CREATE TABLE IF NOT EXISTS test_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    exam_type TEXT,

    subject TEXT,

    difficulty TEXT,

    score INTEGER,

    total_questions INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

conn.commit()

# SAVE TEST RESULT
def save_test_result(

    exam_type,
    subject,
    difficulty,
    score,
    total_questions
):

    cursor.execute(

        """
        INSERT INTO test_history (

            exam_type,
            subject,
            difficulty,
            score,
            total_questions

        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            exam_type,
            subject,
            difficulty,
            score,
            total_questions
        )
    )

    conn.commit()

# FETCH TEST HISTORY
def get_test_history():

    cursor.execute(

        """
        SELECT *

        FROM test_history

        ORDER BY created_at DESC
        """
    )

    return cursor.fetchall()