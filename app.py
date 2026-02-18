from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

QUESTION_BANK = [
    ("What is half of 2 + 2?", "3"),
    ("What is 3 + 6 ÷ 2?", "6"),
    ("If you divide 100 by half and add 10, what do you get?", "210"),
    ("If you look in a mirror and raise your right hand, which hand does your reflection raise?", "left"),
    ("What comes next in the sequence: 2, 4, 8, 16, ?", "32"),
    ("If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? (yes/no)", "yes"),
    ("If a train leaves at 3:00 PM and arrives at 5:30 PM, how long was the journey? (hours)", "2.5"),
    ("A farmer has 17 sheep and all but 9 run away. How many are left?", "9"),
    ("If you drive 60 km in 1 hour, how long will it take to drive 180 km?", "3"),
    ("If 5 machines make 5 parts in 5 minutes, how long do 100 machines take to make 100 parts? (minutes)", "5"),
    ("What weighs more: 1kg of iron or 1kg of cotton?", "same"),
    ("If today is Monday, what day will it be in 100 days?", "wednesday"),
    ("Can a square have more than four sides? (yes/no)", "no"),
    ("If you rotate a 'b' 180 degrees, what letter do you get?", "q"),
    ("What is always coming but never arrives?", "tomorrow"),
]

MAX_ATTEMPTS = 5


@app.route("/")
def index():
    session.clear()
    questions = QUESTION_BANK.copy()
    random.shuffle(questions)
    session["questions"] = questions
    session["score"] = 0
    session["current"] = 0
    session["attempts"] = 0
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "questions" not in session:
        return redirect(url_for("index"))

    questions = session["questions"]
    current = session["current"]

    if current >= len(questions):
        return redirect(url_for("result"))

    question, answer = questions[current]

    if request.method == "POST":
        user_answer = request.form.get("answer").strip().lower()
        session["attempts"] += 1

        if user_answer == answer:
            flash("✅ Correct answer!", "success")
            session["score"] += 1
            session["current"] += 1
            session["attempts"] = 0
            return redirect(url_for("quiz"))

        if session["attempts"] >= MAX_ATTEMPTS:
            flash(f"❌ You failed! Correct answer: {answer}", "danger")
            session["current"] += 1
            session["attempts"] = 0
            return redirect(url_for("quiz"))

        flash("❌ Incorrect answer. Try again.", "warning")

    return render_template(
        "quiz.html",
        question=question,
        attempts_left=MAX_ATTEMPTS - session["attempts"]
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
