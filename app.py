import json

from langgraph.graph import StateGraph, START, END
from Modelhandlers import GraphState
from ApiRequests import player_context_Node, supervised_Node,matchup_context_Node,matchup_agent_Node,player_context_Node,player_agent_Node
from footbal_service import FootballService
from news_service import News_service
import time

app_start = time.time()

football_service = FootballService()
news_services = News_service()
builder = StateGraph(GraphState)

builder.add_node("supervised",supervised_Node)

builder.add_node("matchupContext",matchup_context_Node)
builder.add_node("matchupAgent",matchup_agent_Node)

builder.add_node("playerContext",player_context_Node)
builder.add_node("playerAgent",player_agent_Node)

builder.add_edge(START,"supervised")
builder.add_edge("supervised","playerContext")
builder.add_edge("playerContext","playerAgent")
builder.add_edge("playerAgent",END)

graph = builder.compile()

if __name__ == "__main__":
   # teams = football_service.get_all_teams()
   # with open("teams.json", "w") as file:
   #  json.dump(teams, file, indent=4)

   #  print("Saved to teams.json")  
   # answer = graph.invoke({"question":"Tell me about Messi."})
   # print(answer["player_agent_response"])
   # news_service = NewsService()
   # news = news_service.get_latest_news()
   # print(news[0]) 

   news = news_services.search_news(query="rolando")
   print(json.dumps(news,indent=4))
   print(f"Total App Time: {time.time()-app_start:.2f}s")