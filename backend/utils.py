from inflecteur import inflecteur

inflecteur = inflecteur()
inflecteur.load_dict()

articles = {
    "M": "le",
    "F": "la",
}


def add_article(word):
    if word[0] in "aeiouy":
        return "l'" + word
    gender = inflecteur.get_word_form(word)
    for i, row in gender.iterrows():
        if row.lemma == word:
            return articles[row.gender] + " " + word
    return "(le/la/l')" + word
