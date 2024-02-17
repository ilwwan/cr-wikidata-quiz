from typing import Optional
import requests
import random


def get_random_element_from_identifier(
    element_type_identifier: str,
    anwser_relation_identifier: str,
    element_relation_identifier: Optional[str] = "wdt:P31/wdt:P279*",
    seed: Optional[int] = None,
    max_offset: Optional[int] = 200,
    limit: Optional[int] = 1,
    answer_is_entity: Optional[bool] = False,
):
    if answer_is_entity:
        answer_query_field = "answerLabel"
    else:
        answer_query_field = "answer"
    if seed is not None:
        random.seed(seed)
    offset = random.randint(0, max_offset)
    query = f"""
    SELECT DISTINCT ?item ?itemLabel ?linkcount ?{answer_query_field} WHERE {{
        ?item {element_relation_identifier} wd:{element_type_identifier};
              wikibase:sitelinks ?linkcount;
                wdt:{anwser_relation_identifier} ?answer.
    FILTER (?linkcount >= 1) .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr" . }}
    }}
    ORDER BY DESC(?linkcount)
    OFFSET {offset}
    LIMIT {limit}
    """
    print(query)
    r = requests.get(
        "https://query.wikidata.org/sparql",
        params={"format": "json", "query": query},
        headers={"User-Agent": "Mozilla/5.0"},
    )
    r.raise_for_status()
    response = r.json()
    if len(r.json()["results"]["bindings"]) == 0:
        return get_random_element_from_identifier(
            element_type_identifier,
            anwser_relation_identifier,
            seed=seed,
            max_offset=max_offset,
            limit=limit,
            answer_is_entity=answer_is_entity,
        )
    if limit == 1:
        return (
            r.json()["results"]["bindings"][0]["itemLabel"]["value"],
            r.json()["results"]["bindings"][0][answer_query_field]["value"],
        )
    else:
        return (
            r.json()["results"]["bindings"][0]["itemLabel"]["value"],
            [
                row[answer_query_field]["value"]
                for row in r.json()["results"]["bindings"]
            ],
        )
