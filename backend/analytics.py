import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="smartqbank"
)

cursor = db.cursor()

# Total Exams
cursor.execute("SELECT COUNT(*) FROM exams")
total_exams = cursor.fetchone()[0]

# Average Score
cursor.execute("SELECT AVG(score) FROM student_scores")
average_score = cursor.fetchone()[0]

# Highest Score
cursor.execute("SELECT MAX(score) FROM student_scores")
highest_score = cursor.fetchone()[0]

print("\nAnalytics Dashboard")
print("-" * 30)
print("Total Exams:", total_exams)
print("Average Score:", average_score)
print("Highest Score:", highest_score)
