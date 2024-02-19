import xml.etree.ElementTree as ET
import questions.histoire
import questions.geography
import questions.arts
import random
import html
from inflecteur import inflecteur

inflecteur_instance = inflecteur()
inflecteur_instance.load_dict()

question_generators = [questions.arts, questions.geography, questions.histoire]

print("Script starting...")


def generate_random_question(inflecteur_instance):
    generator = random.choice(question_generators)
    return generator.generate_random_question(inflecteur_instance)


def unescape_html(s):
    # Replace &#233; with é, etc.
    s = html.unescape(s)
    s = s.replace("é", "e")
    s = s.replace("è", "e")
    s = s.replace("ê", "e")
    s = s.replace("à", "a")
    s = s.replace("â", "a")
    s = s.replace("ç", "c")
    return s


for i in range(10):
    # Open and parse the XML file
    tree = ET.parse('./backend/quiz1.xml')
    root = tree.getroot()

    # Find the first question in the XML file
    first_question = root.find('.//question[name="Question"]')

    if first_question is not None:
        q, r, a = generate_random_question(inflecteur_instance)
        print(r)
        print(a)
        r.remove(a)
        q = unescape_html(q)
        a = unescape_html(a)
        r = [unescape_html(x) for x in r]

        name_element = first_question.find('name')
        name_element.text = str(q)

        # Modify answerWrong elements (assuming there are multiple)
        answer_wrong_elements = first_question.findall('answerWrong')
        for answer_wrong_element in answer_wrong_elements:
            answer_wrong_element.text = str(r[0])
            r.pop(0)

        # Modify answerRight element
        answer_right_element = first_question.find('answerRight')
        answer_right_element.text = str(a)

        # Save the modified XML file
        tree.write('./backend/quiz1.xml', encoding="utf-8")

        print("First question modified successfully!")
    else:
        print("First question named 'Question' not found.")
