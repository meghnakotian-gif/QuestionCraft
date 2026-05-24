# Automatic Score Calculation

def calculate_score(correct_answers, student_answers):
    score = 0

    for qid, correct_answer in correct_answers.items():
        if qid in student_answers:
            if student_answers[qid] == correct_answer:
                score += 1

    return score


# Example Correct Answers
correct_answers = {
    1: "A",
    2: "B",
    3: "C",
    4: "D"
}

# Example Student Answers
student_answers = {
    1: "A",
    2: "B",
    3: "D",
    4: "D"
}

# Calculate Result
final_score = calculate_score(correct_answers, student_answers)

print(f"Student Score: {final_score}")
import mysql.connector
from datetime import datetime

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="smartqbank"
)

cursor = db.cursor()

# Function to Store Result
def store_result(student_id, exam_id, score):

    query = """
    INSERT INTO student_scores
    (student_id, exam_id, score, exam_date)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        student_id,
        exam_id,
        score,
        datetime.now()
    )

    cursor.execute(query, values)
    db.commit()

    print("Result Stored Successfully")


# Example Call
store_result(1, 101, final_score)