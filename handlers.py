from pydantic import BaseModel
from typing import TypedDict
import json

def get_team_by_name(name:str):
    with open("teams.json",'r') as file:
        teams = json.load(file)['teams']

    return next(
        (team for team in teams if team['name'].lower() == name.lower()),
        None
    )

class SupervisorOutput(BaseModel):
    is_football_query: bool
    reason: str

    team_name: str
    opponent: str
    need_opponent: bool
    player_name: str
    competition: str
    match_date: str
    match_type: str
    intent: str
    agents: list[str]
    
class MatchupState(TypedDict):
    next_match:dict
    previous_match:dict
    head_to_head:dict

class GraphState(TypedDict):
    question: str
    finalAnswer:str
    team_name: str
    opponent: str
    need_opponent: bool
    player_name: str
    competition: str
    match_date: str
    match_type: str
    intent: str

    agents: list[str]

    match_analysis: str
    player_analysis: str
    news_analysis: str

    matchup_state: MatchupState

    matchup_agent_response:str

    final_answer: str