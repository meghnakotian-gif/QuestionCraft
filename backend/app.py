import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# ── MySQL Configuration ────────────────────────────────────────────────────────
app.config['MYSQL_HOST']     = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER']     = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB']       = os.getenv('MYSQL_DB', 'smartqbank')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ── Health Check ───────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "QuestionCraft Backend Running Successfully"}), 200


# ── POST /add-question ─────────────────────────────────────────────────────────
@app.route('/add-question', methods=['POST'])
def add_question():
    """
    Add a new question to the database.

    Expected JSON body:
    {
        "subject":    "Mathematics",
        "topic":      "Algebra",
        "question":   "What is 2 + 2?",
        "option_a":   "3",
        "option_b":   "4",
        "option_c":   "5",
        "option_d":   "6",
        "answer":     "B",          # must be A / B / C / D
        "difficulty": "easy"        # easy / medium / hard  (optional, default: medium)
    }
    """
    data = request.get_json(silent=True)

    # ── 1. Validate request body exists ───────────────────────────────────────
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    # ── 2. Required fields check ───────────────────────────────────────────────
    required_fields = ['subject', 'topic', 'question',
                       'option_a', 'option_b', 'option_c', 'option_d', 'answer']
    missing = [f for f in required_fields if not data.get(f, '').strip()]
    if missing:
        return jsonify({"error": f"Missing or empty required fields: {missing}"}), 400

    # ── 3. Validate answer value ───────────────────────────────────────────────
    answer = data['answer'].strip().upper()
    if answer not in ('A', 'B', 'C', 'D'):
        return jsonify({"error": "Field 'answer' must be one of: A, B, C, D."}), 400

    # ── 4. Validate difficulty value ───────────────────────────────────────────
    difficulty = data.get('difficulty', 'medium').strip().lower()
    if difficulty not in ('easy', 'medium', 'hard'):
        return jsonify({"error": "Field 'difficulty' must be one of: easy, medium, hard."}), 400

    # ── 5. Insert into database ────────────────────────────────────────────────
    try:
        cursor = mysql.connection.cursor()
        sql = """
            INSERT INTO questions
                (subject, topic, question, option_a, option_b, option_c, option_d, answer, difficulty)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['subject'].strip(),
            data['topic'].strip(),
            data['question'].strip(),
            data['option_a'].strip(),
            data['option_b'].strip(),
            data['option_c'].strip(),
            data['option_d'].strip(),
            answer,
            difficulty
        )
        cursor.execute(sql, values)
        mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            "success": True,
            "message": "Question added successfully.",
            "question_id": new_id
        }), 201

    except Exception as e:
        return jsonify({"error": "Database error.", "details": str(e)}), 500


# ── GET /questions ─────────────────────────────────────────────────────────────
@app.route('/questions', methods=['GET'])
def get_questions():
    """
    Fetch all questions, with optional filters via query parameters.

    Query params (all optional):
        subject    - filter by subject     e.g. ?subject=Mathematics
        topic      - filter by topic       e.g. ?topic=Algebra
        difficulty - filter by difficulty  e.g. ?difficulty=easy
    """
    subject    = request.args.get('subject',    '').strip()
    topic      = request.args.get('topic',      '').strip()
    difficulty = request.args.get('difficulty', '').strip().lower()

    # Validate difficulty if provided
    if difficulty and difficulty not in ('easy', 'medium', 'hard'):
        return jsonify({"error": "Invalid difficulty. Must be: easy, medium, or hard."}), 400

    try:
        cursor = mysql.connection.cursor()

        # Build query dynamically based on provided filters
        sql    = "SELECT * FROM questions"
        params = []
        filters = []

        if subject:
            filters.append("subject = %s")
            params.append(subject)
        if topic:
            filters.append("topic = %s")
            params.append(topic)
        if difficulty:
            filters.append("difficulty = %s")
            params.append(difficulty)

        if filters:
            sql += " WHERE " + " AND ".join(filters)

        sql += " ORDER BY created_at DESC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return jsonify({
            "success": True,
            "count": len(rows),
            "questions": rows
        }), 200

    except Exception as e:
        return jsonify({"error": "Database error.", "details": str(e)}), 500


# ── GET /questions/<subject> ───────────────────────────────────────────────────
@app.route('/questions/<string:subject>', methods=['GET'])
def get_questions_by_subject(subject):
    """
    Fetch questions filtered by subject (path parameter).
    Additional optional query params:
        topic      - further filter by topic       e.g. ?topic=Algebra
        difficulty - further filter by difficulty  e.g. ?difficulty=hard
    """
    subject = subject.strip()
    if not subject:
        return jsonify({"error": "Subject cannot be empty."}), 400

    topic      = request.args.get('topic',      '').strip()
    difficulty = request.args.get('difficulty', '').strip().lower()

    # Validate difficulty if provided
    if difficulty and difficulty not in ('easy', 'medium', 'hard'):
        return jsonify({"error": "Invalid difficulty. Must be: easy, medium, or hard."}), 400

    try:
        cursor  = mysql.connection.cursor()
        sql     = "SELECT * FROM questions WHERE subject = %s"
        params  = [subject]

        if topic:
            sql += " AND topic = %s"
            params.append(topic)
        if difficulty:
            sql += " AND difficulty = %s"
            params.append(difficulty)

        sql += " ORDER BY created_at DESC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return jsonify({
                "success": True,
                "count": 0,
                "message": f"No questions found for subject '{subject}'.",
                "questions": []
            }), 200

        return jsonify({
            "success": True,
            "subject": subject,
            "count": len(rows),
            "questions": rows
        }), 200

    except Exception as e:
        return jsonify({"error": "Database error.", "details": str(e)}), 500


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)