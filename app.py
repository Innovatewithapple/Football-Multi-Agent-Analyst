from langgraph.graph import StateGraph, START, END
from handlers import GraphState
from ApiRequests import supervised_Node,matchup_context_Node,matchup_agent_Node
import json
from footbal_service import FootballService
import time

app_start = time.time()

football_service = FootballService()
builder = StateGraph(GraphState)

builder.add_node("supervised",supervised_Node)
builder.add_node("matchupContext",matchup_context_Node)
builder.add_node("matchupAgent",matchup_agent_Node)

builder.add_edge(START,"supervised")
builder.add_edge("supervised","matchupContext")
builder.add_edge("matchupContext","matchupAgent")
builder.add_edge("matchupAgent",END)

graph = builder.compile()

if __name__ == "__main__":
   # teams = football_service.get_all_teams()
   # with open("teams.json", "w") as file:
   #  json.dump(teams, file, indent=4)

   #  print("Saved to teams.json")  
   answer = graph.invoke({"question":"Give me the briefing of Brazil's next match"})
   print(f"Total App Time: {time.time()-app_start:.2f}s")
   # print(f'Answer: \n{json.dumps(answer,indent=4)}')

   # for team in teams["teams"]:
   #  print(team["name"])
