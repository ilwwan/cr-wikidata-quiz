from flask import Flask, render_template, Response
from pathlib import Path
from backend.main import generate_random_question


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/question")
async def get_question():
    question, answers, real_answer = await generate_random_question()
    return {
        "question": question,
        "answers": answers,
        "real_answer": real_answer,
    }


if __name__ == "__main__":
    app.run(debug=True)
