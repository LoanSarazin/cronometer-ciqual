import pandas as pd
import re
import json

from crono_json import makeJsonDict
from cronopy import CronoPy

from nutrients_dic import NUTRIENTS_ID, SSGRP_CATEGORIES

DEFAULT = "-1"
def default_transfo(value: str):
    if value == DEFAULT:
        return 0
    if type(value) == str:
        return float(value.replace(',', '.'))
    return value

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
    # Careful, there are 2 spaces in the Ciqual table header for the energie
    exceptions = [
        "Energie, N x facteur Jones, avec fibres  (kcal/100 g)",
    ]
    
    nutrients = []
    
    # Start with energie
    lipides = default_transfo(row['Lipides (g/100 g)'])
    glucides = default_transfo(row['Lipides (g/100 g)'])
    fibres = default_transfo(row['Fibres alimentaires (g/100 g)'])
    prots = default_transfo(row['Protéines, N x facteur de Jones (g/100 g)'])
    cal_init = row["Energie, N x facteur Jones, avec fibres  (kcal/100 g)"]
    if cal_init == DEFAULT:
        cal = (4*(glucides + fibres + prots) + 9*lipides)
    elif type(cal_init) == str:
        cal = float(cal_init.replace(',', '.'))
    else:
        cal = cal_init
        
    nutrients.append(
        {
            "amount": cal,
            "id": NUTRIENTS_ID["Energie, N x facteur Jones, avec fibres"]
        }
    )
    
    for nutr, value in row.items():
        if nutr not in exceptions and value != DEFAULT and nutr in NUTRIENTS_ID.keys():
            nutrients.append(
                {
                    "amount": float(value.replace(',', '.')) if type(value) == str else value,
                    "id": NUTRIENTS_ID[nutr]
                }
            )
    
    # Vitamine A
    vit_a = (
        default_transfo(row['Beta-Carotène (µg/100 g)']) +
        default_transfo(row['Rétinol (µg/100 g)'])
    )
    nutrients.append(
        {
            "amount": vit_a,
            "id": NUTRIENTS_ID["Vitamine A"]
        }
    )
    
    # Vitamine K
    vit_k = (
        default_transfo(row['Vitamine K1 (µg/100 g)']) +
        default_transfo(row['Vitamine K2 (µg/100 g)'])
    )
    nutrients.append(
        {
            "amount": vit_k,
            "id": NUTRIENTS_ID["Vitamine K"]
        }
    )
    
    # Oméga-3
    omg3 = (
        default_transfo(row['AG 18:3 c9,c12,c15 (n-3), alpha-linolénique (g/100 g)']) +
        default_transfo(row['AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100 g)']) +
        default_transfo(row['AG 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100 g)'])
    )
    nutrients.append(
        {
            "amount": omg3,
            "id": NUTRIENTS_ID["Omega-3"]
        }
    )
    
    # Oméga-6
    omg6 = (
        default_transfo(row['AG 20:4 5c,8c,11c,14c (n-6), arachidonique (g/100 g)']) +
        default_transfo(row['AG 18:2 9c,12c (n-6), linoléique (g/100 g)'])
    )
    nutrients.append(
        {
            "amount": omg6,
            "id": NUTRIENTS_ID["Omega-3"]
        }
    )
    
    return name, category, nutrients

def main():
    path = input("\nxlsx path\n").replace("\\", "/")
    # File should be an xlsx version of the table
    foods = pd.read_excel(path, engine="openpyxl")

    # Remove NaNs and replace - and traces by default values
    foods = foods.dropna().replace(["-", "traces"], [DEFAULT, DEFAULT])
    # Remove '<' symbol
    foods = foods.replace('< ', '', regex=True)
    # Change columns header
    # foods = foods.set_axis([re.sub(" \(\S*100 g\)$", "", col).strip() for col in foods.columns], axis='columns')

    username = input("\nCronometer username\n")
    pwd = input("\nCronometer password\n")
    
    cron = CronoPy()
    msg, error = cron.Login(username, pwd)
    if error:
        raise SystemExit(msg)
    else:
        print(msg)
    
    try:
        owner = int(input("\nowner - leave it empty if not known\n"))
    except:
        owner = 0

    for _, row in foods.iterrows():
        name, category, nutrients = convert_row(row)
        crono_json_dict = makeJsonDict(
            name, nutrients, category=category, owner=owner, source="Ciqual"
        )
        msg, error = cron.importCustomFood(crono_json_dict)
        if error:
            print(f"Error: {msg}")
        else:
            print(msg)
            
    msg, error = cron.Logout()
    print(msg)
            
if __name__ == "__main__":
    main()