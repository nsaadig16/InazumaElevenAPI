import pandas as pd
from fastapi import FastAPI, HTTPException
from utils import as_json, normalize_team, normalize_position, normalize_stat

app = FastAPI(title="Inazuma Eleven API")

df = pd.read_csv("database.csv")
df.set_index("Name", inplace=True)

MOVE_COLS = ["1st Move", "2nd Move", "3rd Move", "4th Move"]

@app.get("/")
def root():
    return {"message" : "Welcome to the Inazuma Eleven API!"}

@app.get("/metadata")
def get_metadata():
    return {
        "version": "0.2.0",
        "name": "Inazuma Eleven API",
        "total_players": len(df),
        "available_filters": {
            "teams": df["Team"].unique().tolist(),
            "positions": df["Position"].unique().tolist(),
            "element": df["Element"].unique().tolist(),
            "recruitment_types": df["Recruitment"].unique().tolist(),
            "stats": [
                "FP",
                "TP",
                "Kick",
                "Body",
                "Control",
                "Guard",
                "Speed",
                "Stamina",
                "Guts",
            ],
        },
        "endpoints": [
            "/players",
            "/players/{name}",
            "/teams",
            "/teams/{team}",
            "/positions",
            "/positions/{position}",
            "/elements",
            "/elements/{element}",
            "/moves",
            "/moves/{move}",
            "/recruitment",
            "/recruitment/{recruitment_type}",
            "/player_stats/{stat}",
        ],
    }

@app.get("/all")
def get_all():
    return as_json(df)

@app.get("/players")    
def get_all_players():
    return as_json(df.index.tolist(), title="players")

@app.get("/players/{name}")
def get_player_by_name(name : str):
    nrml_name = name.title()
    if nrml_name not in df.index.to_list():
        raise HTTPException(404, f"Player {nrml_name} not found")
    return as_json(df.loc[nrml_name])

@app.get("/teams/")
def get_all_teams():
    return as_json(df["Team"].unique().tolist(), title="teams")

@app.get("/teams/{team}")
def get_players_by_team(team : str):
    nrml_team = normalize_team(team)
    if nrml_team not in df["Team"].to_list():
        raise HTTPException(404, f"Team {nrml_team} not found")
    return as_json(df[df["Team"] == nrml_team])

@app.get("/recruitment/")
def get_all_recruitment_types():
    return as_json(df["Recruitment"].unique().tolist(), "recruitment_types")

@app.get("/recruitment/{recruitment_type}")
def get_players_by_recruitment_type(rec_type : str):
    nrml_recruitment = rec_type.capitalize()
    if nrml_recruitment not in df["Recruitment"].to_list():
        raise HTTPException(404, f"Recruitment type {nrml_recruitment} not found")
    return as_json(df[df["Recruitment"].str.contains(nrml_recruitment)])

@app.get("/positions/")
def get_all_positions():
    return as_json(df["Position"].unique().tolist(), title="positions")

@app.get("/positions/{position}")
def get_players_by_position(position : str):
    nrml_position = normalize_position(position)
    if nrml_position not in df["Position"].to_list():
        raise HTTPException(404, f"Position {nrml_position} not found")
    return as_json(df[df["Position"] == nrml_position])

@app.get("/elements")
def get_all_elements():
    return as_json(df["Element"].unique().tolist(), title="elements")

@app.get("/elements/{element}")
def get_players_by_element(element : str):
    nrml_element = element.capitalize()
    if nrml_element not in df["Element"].to_list():
        raise HTTPException(404, f"Element {element} not found")
    return as_json(df[df["Element"] == nrml_element])

@app.get("/moves/")
def get_all_moves():
    all_moves = df[MOVE_COLS].stack()
    return as_json(all_moves.unique().tolist(), title="moves") # type: ignore

@app.get("/moves/{move}")
def get_players_by_move(move : str):
    nrml_move = move.title()
    mask = df[MOVE_COLS].apply(lambda r : nrml_move in r.values, axis = 1)
    if not mask.any():
        raise HTTPException(404, f"Move {nrml_move} not found") 
    return as_json(df[mask].reset_index())

@app.get("/player_stats/{stat}")
def get_players_by_stat(
    stat: str, min_value: int | None = None, max_value: int | None = None
):
    nrml_stat = normalize_stat(stat)
    mask = pd.Series([True] * len(df))
    if min_value is not None:
        mask &= df[nrml_stat] > min_value
    if max_value is not None:
        mask &= df[nrml_stat] <= max_value
    return as_json(df[mask])
