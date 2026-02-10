import pandas as pd
from fastapi import FastAPI
from utils import as_json, normalize_team, normalize_position, normalize_stat

app = FastAPI(title="Inazuma Eleven API")

df = pd.read_csv("database.csv")
df.set_index("Name", inplace=True)

MOVE_COLS = ["1st Move", "2nd Move", "3rd Move", "4th Move"]

@app.get("/")
def root():
    return {"message" : "Welcome to the Inazuma Eleven API!"}

@app.get("/all")
def get_all():
    return as_json(df)

@app.get("/players")    
def get_all_players():
    return df.index.tolist()

@app.get("/players/{name}")
def get_player_by_name(name : str):
    normalized_name = name.title()
    return as_json(df.loc[normalized_name])

@app.get("/teams/")
def get_all_teams():
    return df["Team"].unique().tolist()

@app.get("/teams/{team}")
def get_players_by_team(team : str):
    normalized_team = normalize_team(team)
    return as_json(df[df["Team"] == normalized_team])

@app.get("/recruitment/")
def get_all_recruitment_types():
    return as_json(df[df["Team"] == "Recruitable"])

@app.get("/recruitment/{recruitment_type}")
def get_players_by_recruitment_type(rec_type : str):
    normalized_recruitment = rec_type.capitalize()
    return as_json(df[df["Recruitment"] == normalized_recruitment])

@app.get("/positions/")
def get_all_positions():
    return df["Position"].unique().tolist()

@app.get("/positions/{position}")
def get_players_by_position(position : str):
    normalized_position = normalize_position(position)
    return as_json(df[df["Position"] == normalized_position])

@app.get("/elements")
def get_all_elements():
    return df["Element"].unique().tolist()

@app.get("/elements/{element}")
def get_players_by_element(element : str):
    normalized_element = element.capitalize()
    return as_json(df[df["Element"] == normalized_element])

@app.get("/moves/")
def get_all_moves():
    all_moves = df[MOVE_COLS].stack()
    return all_moves.unique().tolist() # type: ignore

@app.get("/moves/{move}")
def get_players_by_move(move : str):
    normalized_move = move.title()
    mask = df[MOVE_COLS].apply(lambda r : normalized_move in r.values, axis = 1)
    return as_json(df[mask].reset_index())

@app.get("/player_stats/{stat}/min/{min_value}")
def get_players_stats_greater_than_value(stat : str, min_value : int):
    normalized_stat = normalize_stat(stat)
    return as_json(df[df[normalized_stat] > min_value])

@app.get("/player_stats/{stat}/max/{max_value}")
def get_players_stats_lesser_or_equal_than_value(stat : str, max_value : int):
    normalized_stat = normalize_stat(stat)
    return as_json(df[df[normalized_stat] <= max_value])