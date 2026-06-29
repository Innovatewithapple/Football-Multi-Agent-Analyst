import os
import time
from urllib import response
import requests
import json
from dotenv import load_dotenv
from FootballResponseParser import FootballResponseParser
import httpx

load_dotenv()

class FootballService:
    BASE_URL = "https://api.football-data.org/v4/"

    # params = {
    # "limit":100,
    # "season":2026
    # }

    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_API_KEY')
        self.headers={"X-Auth-Token":self.api_key}

    async def _make_request(self,endpoint:str):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=10,headers=self.headers) as client:
                response = await client.get(url=url)#,params=self.params)
                response.raise_for_status()
                return response.json()
        
        except httpx.TimeoutException:
            print('Football api timeout!')
            return {}

        except httpx.ConnectError:
            print("Couldn't connect to Football API!")
            return {}

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e}")
            return {}

        except httpx.RequestError as e:
            print(f"Unexpected Error: {e}")
            return {}

        return None
    
    #----Get All Teams----!
    async def get_all_teams(self):
        return self._make_request(endpoint="competitions/2000/teams")
    
    async def get_team_next_match_data(self,teamid):
        response = await self._make_request(endpoint=f"teams/{teamid}/matches?status=SCHEDULED")
        matches = response.get("matches", [])
        #print(f'\n\nNextMatch: {json.dumps(matches,indent=4)}')
        if not matches:
            return None
        match = FootballResponseParser._extract_match_data(match=matches[0])
        return match
    
    async def get_team_previous_match_data(self,teamid):
        response = await self._make_request(endpoint=f"teams/{teamid}/matches?status=FINISHED")
        matches = response.get("matches", [])
        #print(f'\n\npreviousMatch: {json.dumps(matches,indent=4)}')
        if not matches:
            return None
        latest_match = max(matches, key=lambda m: m["utcDate"]) # latest finished match
        j = json.dumps(latest_match, indent=4)
        #print(f'\n\n latest_match: {j}')
        match = FootballResponseParser._extract_match_data(match=latest_match, include_score=True)
        return match

    async def get_Head2Head_match_data(self,matchid):
        response = await self._make_request(endpoint=f'matches/{matchid}/head2head?limit=50')
        matches = response.get("matches",[])

        if not matches:
            return None
        match = FootballResponseParser._extract_head2head_match_data(matches[0])
        return match

    async def get_tournament_Top_scores_player(self,player_ids:list):
        response = await self._make_request(endpoint='competitions/2000/scorers?limit=15')
        scorers = response.get("scorers",[])

        if not scorers:
            return None
        fetched_Scorers = FootballResponseParser._extract_top_scorers(scorers=scorers,player_ids=player_ids)
        return fetched_Scorers

    async def get_player_info(self,player_id):
        response = await self._make_request(endpoint=f'persons/{player_id}')
        return response
    
    async def get_player_matches_info(self,player_id):
        response = await self._make_request(endpoint=f'persons/{player_id}/matches')
        matches = response.get('matches',[])

        if not matches:
            return None
        return matches


