import random
from query import get_random_element_from_identifier
from utils import add_article, generate_dummy_years
from datetime import datetime

QUESTION_TEMPLATES = [
    {
        "question": "Quelle est la capitale [] ?",
        "answer_relation_identifier": "P36",
        "element_type_identifier": "Q6256",
        "max_offset": 120,
        "answer_parser": lambda x: x[0],
        "other_answers": lambda x: x,
        "query_limit": 4,
        "answer_is_entity": True,
        "article_type": "de",
    },
    {
        "question": "Dans quel pays se trouve [] ?",
        "find_article": False,
        "element_type_identifier": "Q1549591",
        "answer_relation_identifier": "P17",
        "max_offset": 120,
        "answer_parser": lambda x: x[0],
        "other_answers": lambda x: x,
        "query_limit": 4,
        "answer_is_entity": True,
    },
    {
        "question": "Dans quel pays se trouve [] ?",
        "element_type_identifier": "Q570116",
        "answer_relation_identifier": "P17",
        "max_offset": 120,
        "answer_parser": lambda x: x[0],
        "other_answers": lambda x: x,
        "query_limit": 4,
        "answer_is_entity": True,
    },
]


def generate_random_question(inflecteur_instance):
    template = random.choice(QUESTION_TEMPLATES)
    template, answers, real_answer = generate_question_from_template(
        template, inflecteur_instance)
    return template, random.sample(answers, len(answers)), real_answer


def generate_question_from_template(template, inflecteur_instance, article_type=""):
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
            add_article(first_word, inflecteur_instance,
                        type_=template.get("article_type", ""))
            + " "
            + " ".join(replacement.split(" ")[1:])
        )
    question = question.replace("[]", replacement)
    real_answer = template["answer_parser"](answer)
    other_answers = template["other_answers"](answer)
    return question, other_answers, real_answer
