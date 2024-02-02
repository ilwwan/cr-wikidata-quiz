from typing import Optional
import requests
import random


def get_random_element_from_identifier(
    element_type_identifier: str,
    anwser_relation_identifier: str,
    seed: Optional[int] = None,
):
    if seed is not None:
        random.seed(seed)
    offset = random.randint(0, 200)
    query = f"""
    SELECT ?item ?itemLabel ?linkcount ?answer WHERE {{
        ?item wdt:P31/wdt:P279* wd:{element_type_identifier};
              wikibase:sitelinks ?linkcount;
                wdt:{anwser_relation_identifier} ?answer.
    FILTER (?linkcount >= 1) .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr" . }}
    }}
    ORDER BY DESC(?linkcount)
    OFFSET {offset}
    LIMIT 1
    """
    print(query)
    r = requests.get(
        "https://query.wikidata.org/sparql", params={"format": "json", "query": query}
    )
    return (
        r.json()["results"]["bindings"][0]["itemLabel"]["value"],
        r.json()["results"]["bindings"][0]["answer"]["value"],
    )
