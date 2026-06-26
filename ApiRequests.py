from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from prompts import supervisor_Prompt,matchup_Prompt
from handlers import GraphState, SupervisorOutput, get_team_by_name
from dotenv import load_dotenv
import os
from footbal_service import FootballService

load_dotenv()

football_service = FootballService()
nvidia_API = os.getenv("NVDIA_API_Key")
base_url='https://integrate.api.nvidia.com/v1/chat/completions'
model='meta/llama-4-maverick-17b-128e-instruct'#mistralai/mistral-medium-3.5-128b'
max_Tokens = 350
temperature = 0.0
chat_Model = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API,temperature=temperature,max_completion_tokens=max_Tokens,top_p=0.9)
parser = StrOutputParser()

def supervised_Node(state: GraphState):
    supervised_chain = (
        supervisor_Prompt
        | chat_Model.with_structured_output(SupervisorOutput)    
    )

    result = supervised_chain.invoke({'user_query':state['question']})
    print(f"\n\nResult: {result}")
    if not result.is_football_query:
        return {
            "finalAnswer":"This is Football Analyser Agent! Please search Football related question."
        }
    else:
        return {
            "is_football_query":result.is_football_query,
            "reason":result.reason,
            "team_name": result.team_name,
            "opponent": result.opponent,
            "need_opponent": result.need_opponent,
            "player_name": result.player_name,
            "competition": result.competition,
            "match_type": result.match_type,
            "intent": result.intent,
            "agents": result.agents
    }

def matchup_context_Node(state:GraphState):
    team_name = get_team_by_name(name=state['team_name'])
    print(f'\n\nFetchedTeam: {team_name}')
    id = team_name['id']
    print(f'\n\nteamID: {id}')
    
    next_match= football_service.get_team_next_match_data(teamid=id)
    previous_match= football_service.get_team_previous_match_data(teamid=id)
    head2head_match= football_service.get_Head2Head_match_data(matchid=next_match['match_id'])
    result = {
        "matchup_state":{
            "next_match":next_match,
            "previous_match":previous_match,
            "head_to_head":head2head_match
        }
    }
    return result

def matchup_agent_Node(state: GraphState):
    matchup_chain = (
        matchup_Prompt
        | chat_Model
        | parser
    )

    result = matchup_chain.invoke({
        'user_query':state['question'],
        'context': state['matchup_state']
        })
    print(f'\n\nmatchupResponse: {result}')
    return {
        "matchup_agent_response":result
    }