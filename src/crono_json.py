# -*- coding: utf-8 -*-
from nutrients_dic import LANGUAGES

def makeJsonDict(
    name,
    nutrients,
    names={},
    category=0,
    tags=[],
    notes="",
    barcodes=["xxx"],
    measures=[],
    defaultmeasure=73661880,
    label="EU",
    owner=0,
    id=1,
    source="Custom",
):
    js = {}
    js["owner"] = owner
    js["comments"] = notes
    js["labelType"] = label
    js["foodTags"] = tags
    js["source"] = source
    js["barcodes"] = barcodes
    js["nutrients"] = nutrients
    js["measures"] = [
        {
            "amount": 1,
            "name": "Portion 100g",
            "id": 73661880,
            "type": "Weight",
            "value": 100,
        },
        {
            "amount": 1,
            "name": "g",
            "id": 73662093,
            "type": "Weight",
            "value": 1,
        },
    ]
    if len(measures) > 0:
        js["measures"].extend(measures)
    js["defaultMeasureId"] = defaultmeasure
    js["translations"] = [
        {"translationId": LANGUAGES["en"], "name": name, "languageCode": "en"}
    ]
    for lang in names:
        js["translations"].append(
            {
                "translationId": LANGUAGES[lang],
                "name": names[lang],
                "languageCode": lang,
            }
        )
    js["name"] = name
    js["id"] = id
    js["category"] = category
    js["properties"] = {}  # please contact me if you figure what this does
    return js