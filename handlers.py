from pydantic import BaseModel
from typing import TypedDict

class SupervisorOutput(BaseModel):
    team_name: str
    opponent: str
    need_opponent: bool
    player_name: str
    competition: str
    match_date: str
    match_type: str
    intent: str
    agents: list[str]


class GraphState(TypedDict):
    question: str

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

    final_answer: str