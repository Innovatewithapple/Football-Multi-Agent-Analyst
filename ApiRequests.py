from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from prompts import supervisor_Prompt
from handlers import GraphState, SupervisorOutput
from dotenv import load_dotenv
import os

load_dotenv()

nvidia_API = os.getenv("NVDIA_API_Key")
base_url='https://integrate.api.nvidia.com/v1/chat/completions'
model='meta/llama-4-maverick-17b-128e-instruct'#mistralai/mistral-medium-3.5-128b'
max_Tokens = 100
temperature = 0.0
chat_Model = ChatNVIDIA(model=model,nvidia_api_key=nvidia_API,temperature=temperature,max_completion_tokens=max_Tokens,top_p=0.9)

def supervised_Node(state: GraphState):
    supervised_chain = (
        supervisor_Prompt
        | chat_Model.with_structured_output(SupervisorOutput)    
    )

    result = supervised_chain.invoke({'user_query':state['question']})
    print(f"Result: \n{result}")
    return {
        "team_name": result.team_name,
        "opponent": result.opponent,
        "need_opponent": result.need_opponent,
        "player_name": result.player_name,
        "competition": result.competition,
        "match_type": result.match_type,
        "intent": result.intent,
        "agents": result.agents
    }

# async def matchup_agent_Node(state: GraphState):
#     matchup_chain = (
#         matchup_Prompt
#         |
#     )