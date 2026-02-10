from pandas import DataFrame, Series
from typing import Union, Dict, List

def as_json(obj : Union[DataFrame, Series, List], title : str = "") -> Dict:
    if isinstance(obj, DataFrame):
        return obj.to_dict(orient="index")
    elif isinstance(obj, Series):
        return obj.to_dict()
    elif isinstance(obj, List):
        return {title : obj}
    else:
        raise ValueError("Value is not a Dataframe or Series")
    
def normalize_team(team : str):
    normalized = []
    for w in team.split():
        normalized.append(w[0].upper() + w[1:])
    return " ".join(normalized)

def normalize_position(position : str):
    pos = {
        "goalkeeper" : "GK",
        "defender" : "DF",
        "midfielder" : "MF",
        "forward" : "FW"
    }
    if position.upper() in pos.values():
        normalized_position = position.upper()
    elif position.lower() in pos.keys():
        normalized_position = pos[position.lower()]
    else:
        raise ValueError(f"Not existent position: {position}")
    return normalized_position

def normalize_stat(stat : str):
    if stat.upper() in ["FP","TP"]:
        return stat.upper()
    elif stat.capitalize() in ["Kick","Body","Control","Guard","Speed","Stamina","Guts"]:
        return stat.capitalize()
    else:
        raise ValueError(f"Stat not found: {stat}")
