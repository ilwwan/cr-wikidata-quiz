import random
from query import get_random_element_from_identifier
from utils import add_article, generate_dummy_years
from datetime import datetime

QUESTION_TEMPLATES = [
    {
        "question": "Qui a écrit [] ?",
        "answer_relation_identifier": "P50",
        "element_type_identifier": "Q571",
        "answer_is_entity": True,
        "answer_parser": lambda x: x[0],
        "other_answers": lambda x: [x[0]] + random.sample(x, 3),
        "query_limit": 40,
        "max_offset": 1000,
    },
]


def generate_random_question():
    template = random.choice(QUESTION_TEMPLATES)
    template, answers, real_answer = generate_question_from_template(template)
    return template, random.sample(answers, len(answers)), real_answer


def generate_question_from_template(template, article_type=""):
    question = template["question"]
    replacement, answer = get_random_element_from_identifier(
        template["element_type_identifier"],
        template["answer_relation_identifier"],
        max_offset=template.get("max_offset", 250),
        limit=template.get("query_limit", 1),
        answer_is_entity=template.get("answer_is_entity", False),
        element_relation_identifier=template.get(
            "element_relation_identifier", "wdt:P31/wdt:P279*"
        ),
    )
    if template.get("find_article", True):
        first_word = replacement.split(" ")[0]
        replacement = (
            add_article(first_word, type_=template.get("article_type", ""))
            + " "
            + " ".join(replacement.split(" ")[1:])
        )
    question = question.replace("[]", replacement)
    real_answer = template["answer_parser"](answer)
    other_answers = template["other_answers"](answer)
    return question, other_answers, real_answer
