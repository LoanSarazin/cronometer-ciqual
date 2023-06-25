import pandas as pd
import re

from .nutrients_dic import NUTRIENTS_ID, SSGRP_CATEGORIES

DEFAULT = "-1"
def default_transfo(value: str):
    return 0 if value == DEFAULT else float(value)

path = input("xlsx path").replace("\\", "/")
foods = pd.read_excel(path, engine="openpyxl")

# Remove NaNs and replace - and traces by default values
foods = foods.dropna().replace(["-", "traces"], [DEFAULT, DEFAULT])
# Remove '<' symbol
foods = foods.replace('< ', '', regex=True)
# Change columns header
foods = foods.set_axis([re.sub(" \(\S*100 g\)$", "", col).strip() for col in foods.columns], axis='columns')

def convert_row(row: pd.Series):
    """
    Apply the transformation to a row from the Ciqual table and convert it to

    Args:
        row (pd.Series): row of the Ciqual table
    """
    # Food name
    name = row["alim_nom_fr"]
    
    # Category
    ssgrp = row["alim_ssgrp_nom_fr"]
    ssssgrp = row["alim_ssssgrp_nom_fr"]
    category = SSGRP_CATEGORIES.get(ssgrp, "") if ssssgrp == "-1" else SSGRP_CATEGORIES.get(ssssgrp, "")
    
    # Nutrients
    exceptions = [
        "Lipides",
        "Glucides",
        "Protéines, N x facteur de Jones",
        "Energie, N x facteur Jones, avec fibres",
        "Sucres",
        "AG saturés",
    ]
    
    nutrients = []
    for nutr, value in row.items():
        if nutr not in exceptions and value != DEFAULT and nutr in NUTRIENTS_ID.keys():
            nutrients.append(
                {
                    "amount": float(value),
                    "id": NUTRIENTS_ID[nutr],
                    "type": "PRIMARY"
                }
            )
    
    lipides = default_transfo(row['Lipides'])
    glucides = default_transfo(row['Lipides'])
    fibres = default_transfo(row['Fibres alimentaires'])
    prots = default_transfo(row['Protéines, N x facteur de Jones'])
    cal = (4*(glucides + fibres + prots) + 9*lipides) if value == DEFAULT else float(value)
    
    nutrients.append(
        {
            "amount": cal,
            "id": NUTRIENTS_ID["Energie, N x facteur Jones, avec fibres"],
            "type": "PRIMARY"
        }
    )
    
    # Vitamine A
    vit_a = default_transfo(row['Beta-Carotène']) + default_transfo(row['Rétinol'])
    nutrients.append(
        {
            "amount": vit_a,
            "id": NUTRIENTS_ID["Vitamine A"],
            "type": "PRIMARY"
        }
    )
    
    # Oméga-3
    omg3 = (
        default_transfo(row['AG 18:3 c9,c12,c15 (n-3), alpha-linolénique']) +
        default_transfo(row['AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA']) +
        default_transfo(row['AG 20:5 5c,8c,11c,14c,17c (n-3) EPA'])
    )
    nutrients.append(
        {
            "amount": omg3,
            "id": NUTRIENTS_ID["Omega-3"],
            "type": "PRIMARY"
        }
    )
    
    # Oméga-6
    omg6 = (
        default_transfo(row['AG 20:4 5c,8c,11c,14c (n-6), arachidonique']) +
        default_transfo(row['AG 18:2 9c,12c (n-6), linoléique'])
    )
    nutrients.append(
        {
            "amount": omg6,
            "id": NUTRIENTS_ID["Omega-3"],
            "type": "PRIMARY"
        }
    )