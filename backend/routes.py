from flask import Flask, render_template
import os
import shutil
from inflecteur import inflecteur


app = Flask(__name__, static_folder="../frontend/static",
            template_folder="../frontend/templates")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz1.xml')
def quiz():
    with open("./backend/quiz1.xml") as quiz:
        return "\n".join(quiz.readlines())


@app.route('/execute_script', methods=['POST'])
def execute_script():
    import subprocess
    subprocess.Popen(["python", "./backend/script.py"])

    return "Script executed successfully"


if __name__ == '__main__':
    if os.path.exists("./backend/quiz1.xml"):
        os.remove("./backend/quiz1.xml")
    shutil.copyfile("./backend/quiz_template.xml", "./backend/quiz1.xml")

    app.run(debug=True)
