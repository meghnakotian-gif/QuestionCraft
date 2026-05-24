import random
import mysql.connector

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="smartqbank"
)

cursor = db.cursor(dictionary=True)

# Function to fetch random questions
def fetch_questions(difficulty, count):
    query = """
    SELECT * FROM questions
    WHERE difficulty = %s
    ORDER BY RAND()
    LIMIT %s
    """
    
    cursor.execute(query, (difficulty, count))
    return cursor.fetchall()

# Difficulty Ratio
easy_count = 4
medium_count = 4
hard_count = 2

# Fetch Questions
easy_questions = fetch_questions("easy", easy_count)
medium_questions = fetch_questions("medium", medium_count)
hard_questions = fetch_questions("hard", hard_count)

# Combine Questions
question_paper = (
    easy_questions +
    medium_questions +
    hard_questions
)

# Shuffle Final Paper
random.shuffle(question_paper)

# Display Questions
print("\nGenerated Question Paper\n")

for index, question in enumerate(question_paper, start=1):
    print(f"{index}. {question['question_text']}")
    print(f"Difficulty: {question['difficulty']}")
    print("-" * 40)