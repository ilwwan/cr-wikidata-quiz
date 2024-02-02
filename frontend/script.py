import xml.etree.ElementTree as ET
import json
import random

# Open and parse the XML file
tree = ET.parse('quiz1.xml')
root = tree.getroot()

# Open and load the JSON file
with open('questions.json', 'r') as json_file:
    questions_data = json.load(json_file)

# Find the first question in the XML file
first_question = root.find('.//question[1]/name')

# Check if the first question is exactly named "Question"
if first_question.text == "Question":
    # Randomly select a question from the JSON data
    random_question = random.choice(questions_data)

    # Update the text of the first question in the XML file with the random question
    first_question.text = random_question["question"]

    # Update the answer options in the XML file with the options from the random question
    answer_options = root.find('.//question[1]')
    answer_options.clear()
    for option in random_question["options"]:
        answer = ET.Element("answerRight" if option ==
                            random_question["options"][0] else "answerWrong")
        answer.text = option
        answer_options.append(answer)

    # Save the modified XML file
    tree.write('quiz1.xml')

    print("First question modified successfully!")
else:
    print("First question is not named 'Question'.")
