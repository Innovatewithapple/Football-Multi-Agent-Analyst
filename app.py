from langgraph.graph import StateGraph, START, END
from handlers import GraphState
from ApiRequests import supervised_Node
import json


builder = StateGraph(GraphState)

builder.add_node("supervised",supervised_Node)
builder.add_edge(START,"supervised")
builder.add_edge("supervised",END)

graph = builder.compile()

if __name__ == "__main__":
   answer = graph.invoke({"question":"Give me the briefing of Brazil's next match"})
   print(f'Answer: \n{json.dumps(answer,indent=4)}')
