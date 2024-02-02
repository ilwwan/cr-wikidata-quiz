from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz1.xml')
def quiz():
    with open("quiz1.xml") as quiz:
        return "\n".join(quiz.readlines())


@app.route('/execute_script', methods=['POST'])
def execute_script():
    # Execute script.py here
    # For example:
    import subprocess
    # subprocess.Popen(["python", "script.py"])

    return "Script executed successfully"


if __name__ == '__main__':
    app.run(debug=True)
