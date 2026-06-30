import json
import asyncio
from langgraph.graph import StateGraph, START, END
from Modelhandlers import GraphState
from ApiRequests import player_context_Node, supervised_Node,matchup_context_Node,matchup_agent_Node,player_context_Node,player_agent_Node,news_context_node,news_agent_Node,final_agent_node,route_agents
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

builder.add_node("newsContext",news_context_node)
builder.add_node("newsAgent",news_agent_Node)

builder.add_node("finalAgent",final_agent_node)

builder.add_edge(START,"supervised")
#builder.add_edge("supervised","matchupContext")
builder.add_edge("matchupContext","matchupAgent")

#builder.add_edge("supervised","playerContext")
builder.add_edge("playerContext","playerAgent")

#builder.add_edge("supervised","newsContext")
builder.add_edge("newsContext","newsAgent")

builder.add_edge("matchupAgent", "finalAgent")
builder.add_edge("playerAgent", "finalAgent")
builder.add_edge("newsAgent", "finalAgent")

#----Conditional Edge------!
builder.add_conditional_edges(
   "supervised", route_agents,
   {
      "Matchup-Agent":"matchupContext",
      "Player-Agent":"playerContext",
      "News-Agent":"newsContext"
   }
)

builder.add_edge("finalAgent",END)

graph = builder.compile()

async def main():
   png = graph.get_graph().draw_mermaid_png()

   with open("graph.png", "wb") as f:
    f.write(png)

   print("Graph saved!")
   query = "Who is Cristiano Ronaldo?"
   answer = await graph.ainvoke({"question":query})
   print(f'\n\n Query: {query}')
   print(f'\n Answer: \n{answer["final_answer"]}')
#Compare Cristiano Ronaldo and Lionel Messi based on their recent performances, current form, and the latest football news surrounding both players.
if __name__ == "__main__":
   # teams = football_service.get_all_teams()
   # with open("teams.json", "w") as file:
   #  json.dump(teams, file, indent=4)
   asyncio.run(main())
   print(f"Total App Time: {time.time()-app_start:.2f}s")