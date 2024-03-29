import random
from datetime import datetime
from .utils import add_article, generate_dummy_years
from .query import get_random_element_from_identifier

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
        "find_article": False,
    },
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
    {
        "question": "En quelle année a eu lieu [] ?",
        "answer_relation_identifier": "P585",
        "element_type_identifier": "Q13418847",
        "answer_parser": lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year,
        "other_answers": lambda x: generate_dummy_years(
            datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year
        ),
    },
    {
        "question": "Qui était l'époux ou l'épouse de [] ?",
        "answer_relation_identifier": "P26",
        "element_type_identifier": "Q116",
        "element_relation_identifier": "wdt:P106",
        "answer_is_entity": True,
        "answer_parser": lambda x: x[0],
        "other_answers": lambda x: [x[0]] + random.sample(x, 3),
        "query_limit": 40,
        "find_article": False,
    },
    {
        "question": "En quelle année est né [] ?",
        "answer_relation_identifier": "P569",
        "element_type_identifier": "Q116",
        "element_relation_identifier": "wdt:P106",
        "answer_parser": lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year,
        "other_answers": lambda x: generate_dummy_years(
            datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").year
        ),
        "find_article": False,
    },
]


async def generate_random_question():
    template = random.choice(QUESTION_TEMPLATES)
    question, answers, real_answer = await generate_question_from_template(template)
    return question, random.sample(answers, len(answers)), real_answer


async def generate_question_from_template(template):
    print("Generating question from template", template.get("question"))
    question = template["question"]
    replacement, answer = await get_random_element_from_identifier(
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
