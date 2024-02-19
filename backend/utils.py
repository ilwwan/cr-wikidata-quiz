import random

articles = {
    "M": "le",
    "F": "la",
    "v": "l'",
    "deM": "du",
    "deF": "de la",
    "dev": "de l'",
}


def add_article(word, inflecteur_instance, type_=""):
    word_l = word.lower()
    if word_l[0] in "aeiouy":
        return articles[type_ + "v"] + word
    gender = inflecteur_instance.get_word_form(word_l)
    if gender is None:
        return f"({articles[type_+'M']}/{articles[type_+'F']}) " + word
    for i, row in gender.iterrows():
        if row.lemma == word_l:
            return articles[type_ + row.gender] + " " + word
    return f"({articles[type_+'M']}/{articles[type_+'F']}) " + word


def generate_dummy_years(original_year: int, n: int = 3):
    max_year = max(original_year + 250, 2024)
    min_year = min(original_year - 250, 0)
    std = (max_year - min_year) / 20
    ret = []
    for _ in range(n):
        ret.append(int(random.normalvariate(original_year, std)))
    return random.sample(ret + [original_year], n + 1)
