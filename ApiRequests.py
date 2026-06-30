from turtle import st
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from prompts import supervisor_Prompt,matchup_Prompt,player_agent_prompt,news_agent_prompt,final_agent_prompt
from Modelhandlers import GraphState, SupervisorOutput, get_team_by_name,get_playerinfo_from_json_by_name,get_team_by_playername
from dotenv import load_dotenv
import os
from footbal_service import FootballService
from news_service import News_service
import asyncio
import time
import json

load_dotenv()

football_service = FootballService()
news_services = News_service()
nvidia_API = os.getenv("NVDIA_API_Key")
base_url='https://integrate.api.nvidia.com/v1/chat/completions'
model='meta/llama-4-maverick-17b-128e-instruct'#mistralai/mistral-medium-3.5-128b'
max_Tokens = 500
temperature = 0.0
chat_Model = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API,temperature=temperature,max_completion_tokens=max_Tokens,top_p=0.9)
parser = StrOutputParser()

#FinalAgent:
final_agent_max_Tokens = 700
temperature = 0.0
final_model = 'abacusai/dracarys-llama-3.1-70b-instruct'#'mistralai/mistral-medium-3.5-128b'
final_chat_agent_Model = ChatNVIDIA(model=final_model,nvidia_api_key=nvidia_API,temperature=temperature,max_completion_tokens=final_agent_max_Tokens,top_p=0.9)

async def supervised_Node(state: GraphState):
      start = time.perf_counter()
      try:
         supervised_chain = (
            supervisor_Prompt
            | chat_Model.with_structured_output(SupervisorOutput)    
         )

         result = await supervised_chain.ainvoke({'user_query':state['question']})
         print(f"\n\nResult: {result.model_dump()}")
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
                  "players_name": result.players_name,
                  "topics":result.topics,
                  "competition": result.competition,
                  "match_type": result.match_type,
                  "intent": result.intent,
                  "agents": result.agents
         }

      finally:
         print(f"supervised_Node: {time.perf_counter()-start:.2f}s")

async def process_team(team):

    team_id = team["id"]

    # Run these two requests in parallel
    next_match, previous_match = await asyncio.gather(
        football_service.get_team_next_match_data(teamid=team_id),
        football_service.get_team_previous_match_data(teamid=team_id)
    )

    # Depends on next_match
    head2head = None
    if next_match:
        head2head = await football_service.get_Head2Head_match_data(
            matchid=next_match["match_id"]
        )

    return {
        "team": team["name"],
        "next_match": next_match,
        "previous_match": previous_match,
        "head_to_head": head2head
    }

async def matchup_context_Node(state: GraphState):
      start = time.perf_counter()

      try:
        teams = []

        # If the user explicitly mentioned a team
        if state["team_name"]:
            teams.append(get_team_by_name(state["team_name"]))

        # Otherwise infer team(s) from player(s)
        else:
            for player in state["players_name"]:
                team = get_team_by_playername(player)

                # Skip if no team found
                if team:
                    teams.append(team)

        # Remove duplicate teams (recommended)
        unique_teams = list({team["id"]: team for team in teams}.values())

        results = []

        for team in unique_teams:
            result = await process_team(team)
            results.append(result)

        return {
               "matchup_state": results
               }

      finally:
        print(f"matchup_context_Node: {time.perf_counter() - start:.2f}s")

async def matchup_agent_Node(state: GraphState):
      start = time.perf_counter()
      try:
         matchup_chain = (
            matchup_Prompt
            | chat_Model
            | parser
         )

         result = await matchup_chain.ainvoke({
            'user_query':state['question'],
            'context': state['matchup_state']
            })
         #print(f'\n\nmatchupResponse: {result}')
         return {
            "matchup_agent_response":result
         }
      
      finally:
         print(f"matchup_agent_Node: {time.perf_counter()-start:.2f}s")

async def player_context_Node(state:GraphState):
      start = time.perf_counter()
      try:
         selected_player_ids=[]
         fetched_player_info_list=[]
         for player in state['players_name']:
            player = get_playerinfo_from_json_by_name(name=player)
            selected_player_ids.append(player['id'])

         fetched_scorer_data = await football_service.get_tournament_Top_scores_player(player_ids=selected_player_ids) #this incude top ones too, if there are no specific names in search
         
         for i in selected_player_ids:
            player_info, matches = await asyncio.gather(
               football_service.get_player_info(player_id=i),
               football_service.get_player_matches_info(player_id=i)
            )
            player_info['matches'] = matches
            fetched_player_info_list.append(player_info)
         # #print(f'\n\n =====PlayerIDS: {selected_player_ids}')
         # #print(f'\n\n fetched_player_info_list: {fetched_player_info_list}')
         # #print(f'\n\n fetched_scorer_data: {fetched_player_info_list}')
         return {
            "player_state":{
               "players_info":fetched_player_info_list,
               "top_scorers":fetched_scorer_data
            }
         }

      finally:
         print(f"player_context_Node: {time.perf_counter()-start:.2f}s")

async def player_agent_Node(state:GraphState):
      start = time.perf_counter()
      try:
         player_chain=(
            player_agent_prompt
            | chat_Model
            | parser
         )
         result = await player_chain.ainvoke({
            "user_query":state['question'],
            "context":state['player_state']
         })
         #print(f'\n\nfinal_result: {result}')
         return {
            "player_agent_response":result
         }

      finally:
         print(f"player_agent_Node: {time.perf_counter()-start:.2f}s")

async def news_context_node(state:GraphState):
      start = time.perf_counter()
      try:
         fetched_articles =[]
         if state["team_name"] and not state["players_name"]:
            fetch_news = await news_services.search_news(query=state["team_name"])
            fetched_news_dict= {
            state["team_name"]:fetch_news
            }
            fetched_articles.append(fetched_news_dict)
         else:
            for player in state['players_name']:
               fetch_news = await news_services.search_news(query=player)
               fetched_news_dict= {
                  player:fetch_news
               }
               fetched_articles.append(fetched_news_dict)

         return {
            "news_state":fetched_articles
            }
      
      finally:
         print(f"news_context_node: {time.perf_counter()-start:.2f}s")

async def news_agent_Node(state:GraphState):
      start = time.perf_counter()
      try:
         news_chain=(
            news_agent_prompt
            | chat_Model
            | parser
         )
         result = await news_chain.ainvoke({
            "user_query":state['question'],
            "context":state['news_state'],
            "topics":state['topics']
         })

         return {
            "news_agent_response":result
         }
      
      finally:
         print(f"news_agent_Node: {time.perf_counter()-start:.2f}s")

async def final_agent_node(state:GraphState):
      # print("\nFinal Agent State:")
      # print(json.dumps(state, indent=4, default=str))
      print("🔥 FINAL AGENT EXECUTED") 
      start = time.perf_counter()
      try:
         final_chain=(
            final_agent_prompt
            |chat_Model
            |parser
         )

         result = await final_chain.ainvoke({
         "user_query":state['question'],
         "matchup_response":state.get('matchup_agent_response',""),
         "player_response":state.get('player_agent_response',""),
         "news_response":state.get('news_agent_response',"")
         })

         return {
            "final_answer": result
         }
      
      finally:
         print(f"final_agent_node: {time.perf_counter()-start:.2f}s")

def route_agents(state:GraphState):
    return state['agents']