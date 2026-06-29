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

def get_playerinfo_from_json_by_name(name:str):
    with open('teams.json','r') as file:
        teams = json.load(file)['teams']
        for i in teams:
            for player in i['squad']:
                if name.lower() in player["name"].lower():
                    return player
                
def get_team_by_playername(name:str):
    with open('teams.json','r') as file:
        teams = json.load(file)['teams']
        for i in teams:
            for player in i['squad']:
                if name.lower() in player["name"].lower():
                    return i


class SupervisorOutput(BaseModel):
    is_football_query: bool
    reason: str

    team_name: str
    opponent: str
    topics:list[str]
    need_opponent: bool
    players_name: list[str]
    competition: str
    match_date: str
    match_type: str
    intent: str
    agents: list[str]
    
class MatchupState(TypedDict):
    team: str
    next_match: dict
    previous_match: dict
    head_to_head: dict

class PlayerState(TypedDict):
    players_info:list
    top_scorers:list

class NewsState(TypedDict):
    news_articles:list

class GraphState(TypedDict):
    question: str
    finalAnswer:str
    team_name: str
    opponent: str
    need_opponent: bool
    players_name: str
    competition: str
    match_date: str
    match_type: str
    intent: str
    topics:list[str]
    agents: list[str]

    player_state: PlayerState
    player_agent_response:str
    player_analysis: str

    news_state:NewsState
    news_agent_response:str
    news_analysis: str

    matchup_state: list[MatchupState]
    matchup_agent_response:str
    match_analysis: str

    final_answer: str