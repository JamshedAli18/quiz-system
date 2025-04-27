from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import config
import uuid
import time

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# MySQL Configuration
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title FROM quizzes")
    quizzes = cur.fetchall()
    cur.close()
    return render_template('index.html', quizzes=quizzes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, is_admin FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['is_admin'] = user[2]
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during registration: {e}")
            flash('Username or email already exists')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Check if user has a cheating attempt recorded for this quiz
    cur = mysql.connection.cursor()
    cur.execute("SELECT 1 FROM cheating_attempts WHERE user_id = %s AND quiz_id = %s", (session['user_id'], quiz_id))
    has_cheated = cur.fetchone()
    cur.close()
    if has_cheated:
        print(f"User {session['user_id']} has cheated on quiz {quiz_id}, redirecting to cheating page")
        return redirect(url_for('cheating_detected'))

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, question_text, option_a, option_b, option_c, option_d FROM questions WHERE quiz_id = %s ORDER BY id",
        (quiz_id,))
    questions = cur.fetchall()
    cur.execute("SELECT title, time_limit FROM quizzes WHERE id = %s", (quiz_id,))
    quiz = cur.fetchone()
    cur.close()

    total_questions = len(questions)
    if total_questions == 0:
        flash('No questions available for this quiz.')
        return redirect(url_for('index'))

    # Initialize session for quiz if not already started or if quiz_id has changed
    if 'quiz_id' not in session or session['quiz_id'] != quiz_id:
        session['quiz_id'] = quiz_id
        session['quiz_answers'] = {}
        session['timer_start'] = int(time.time())
        session['time_limit'] = quiz[1]
        session['quiz_started'] = True
        session.modified = True

    # Check if time is up
    time_remaining = max(0, session['time_limit'] - (int(time.time()) - session['timer_start']))
    if time_remaining <= 0:
        print(f"Time is up for quiz {quiz_id}, submitting quiz")
        return redirect(url_for('submit_quiz', quiz_id=quiz_id))

    if request.method == 'POST':
        print(f"Received POST request for quiz {quiz_id}")
        # Process all answers at once
        answers = {}
        for q in questions:
            answer = request.form.get(f'answer_{q[0]}')
            print(f"Question {q[0]} answer: {answer}")
            if answer:
                answers[str(q[0])] = answer

        # Calculate score
        score = 0
        cur = mysql.connection.cursor()
        for q in questions:
            cur.execute("SELECT correct_option FROM questions WHERE id = %s", (q[0],))
            correct_answer = cur.fetchone()[0]
            if str(q[0]) in answers and answers[str(q[0])] == correct_answer:
                score += 1
        print(f"Calculated score: {score}/{total_questions}")
        cur.execute("INSERT INTO scores (user_id, quiz_id, score) VALUES (%s, %s, %s)",
                    (session['user_id'], quiz_id, score))
        mysql.connection.commit()
        cur.close()
        session['score'] = score
        session['total_questions'] = total_questions
        session['quiz_title'] = quiz[0]
        # Clear quiz-related session data
        session.pop('quiz_answers', None)
        session.pop('quiz_id', None)
        session.pop('timer_start', None)
        session.pop('time_limit', None)
        session.pop('quiz_started', None)
        session.modified = True
        print(f"Redirecting to results for quiz {quiz_id}")
        return redirect(url_for('results', quiz_id=quiz_id))

    return render_template('quiz.html', questions=questions, quiz=quiz, quiz_id=quiz_id,
                           total_questions=total_questions, time_remaining=time_remaining)


@app.route('/submit_quiz/<int:quiz_id>', methods=['GET'])
def submit_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Calculate score for timed-out quizzes
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, correct_option FROM questions WHERE quiz_id = %s", (quiz_id,))
    questions = cur.fetchall()
    cur.execute("SELECT title FROM quizzes WHERE id = %s", (quiz_id,))
    quiz = cur.fetchone()
    score = 0
    answers = session.get('quiz_answers', {})
    for q in questions:
        if str(q[0]) in answers and answers[str(q[0])] == q[1]:
            score += 1
    cur.execute("INSERT INTO scores (user_id, quiz_id, score) VALUES (%s, %s, %s)",
                (session['user_id'], quiz_id, score))
    mysql.connection.commit()
    cur.close()
    session['score'] = score
    session['total_questions'] = len(questions)
    session['quiz_title'] = quiz[0]
    # Clear quiz-related session data
    session.pop('quiz_answers', None)
    session.pop('quiz_id', None)
    session.pop('timer_start', None)
    session.pop('time_limit', None)
    session.pop('quiz_started', None)
    session.modified = True
    return redirect(url_for('results', quiz_id=quiz_id))


@app.route('/cheating_detected')
def cheating_detected():
    return render_template('cheating.html')


@app.route('/submit_cheating/<int:quiz_id>', methods=['GET'])
def submit_cheating(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print(f"Cheating detected for user {session['user_id']} on quiz {quiz_id}")
    # Log the cheating attempt in the database
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO cheating_attempts (user_id, quiz_id) VALUES (%s, %s)", (session['user_id'], quiz_id))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error logging cheating attempt: {e}")
        # If the user already has a cheating attempt for this quiz, ignore the error (due to UNIQUE constraint)
        pass
    cur.close()
    # Log out the user by clearing the session
    session.clear()
    session.modified = True
    return redirect(url_for('cheating_detected'))


@app.route('/results/<int:quiz_id>')
def results(quiz_id):
    if 'user_id' not in session or 'score' not in session:
        return redirect(url_for('index'))
    score = session['score']
    total_questions = session['total_questions']
    quiz_title = session['quiz_title']
    percentage = (score / total_questions) * 100

    # Determine message and emoji based on performance
    if percentage >= 80:
        message = "Outstanding performance! You're a quiz master!"
        emoji = "🏆"
    elif percentage >= 60:
        message = "Great job! Keep practicing to reach the top!"
        emoji = "🌟"
    elif percentage >= 40:
        message = "Nice effort! Review the material and try again!"
        emoji = "💪"
    else:
        message = "Don't give up! Study harder and you'll improve!"
        emoji = "📖"

    return render_template('results.html', score=score, total_questions=total_questions,
                           quiz_title=quiz_title, message=message, emoji=emoji, quiz_id=quiz_id)


@app.route('/leaderboard/<int:quiz_id>')
def leaderboard(quiz_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT u.username, s.score, s.date_taken FROM scores s JOIN users u ON s.user_id = u.id WHERE s.quiz_id = %s ORDER BY s.score DESC, s.date_taken",
        (quiz_id,))
    scores = cur.fetchall()
    cur.execute("SELECT title FROM quizzes WHERE id = %s", (quiz_id,))
    quiz = cur.fetchone()
    cur.close()
    return render_template('leaderboard.html', scores=scores, quiz=quiz)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        time_limit = request.form['time_limit']
        questions = []
        for i in range(1, int(request.form['question_count']) + 1):
            question = {
                'text': request.form[f'question_{i}'],
                'option_a': request.form[f'option_a_{i}'],
                'option_b': request.form[f'option_b_{i}'],
                'option_c': request.form[f'option_c_{i}'],
                'option_d': request.form[f'option_d_{i}'],
                'correct': request.form[f'correct_{i}']
            }
            questions.append(question)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO quizzes (title, time_limit) VALUES (%s, %s)", (title, time_limit))
        quiz_id = cur.lastrowid
        for q in questions:
            cur.execute(
                "INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (quiz_id, q['text'], q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct']))
        mysql.connection.commit()
        cur.close()
        flash('Quiz created successfully!')
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)