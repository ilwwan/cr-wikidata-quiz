from typing import Optional
import random
import re
from query import get_random_element_from_identifier
from utils import add_article
from datetime import datetime

QUESTION_TEMPLATES = [
    {
        "question": "En quelle année a eu lieu [] ?",
        "anwser_relation_identifier": "P585",
        "element_type_identifier": "Q13418847",
        "anwser_parser": lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year,
        "other_answers": lambda a: random.sample(
            [a + random.randint(-250, 250) for _ in range(3)] + [a], 4
        ),
    }
]


def generate_random_question():
    template = random.choice(QUESTION_TEMPLATES)
    template, answers, real_answer = generate_question_from_template(template)
    return template, answers


def generate_question_from_template(template):
    question = template["question"]
    replacement, anwser = get_random_element_from_identifier(
        template["element_type_identifier"], template["anwser_relation_identifier"]
    )
    first_word = replacement.split(" ")[0]
    replacement = add_article(first_word) + " " + " ".join(replacement.split(" ")[1:])
    question = question.replace("[]", replacement)
    answer = template["anwser_parser"](anwser)
    return question, template["other_answers"](answer), answer
