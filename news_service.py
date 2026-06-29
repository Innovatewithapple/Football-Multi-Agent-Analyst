import requests
import os
from FootballResponseParser import FootballResponseParser
import httpx


class News_service:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')

    async def _make_request(self, params):
        url = self.BASE_URL

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url=url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            print("News api timeout!")

        except httpx.ConnectError:
            print("Couldn't connect to News API!")

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e}")

        except httpx.RequestError as e:
            print(f"Unexpected Error: {e}")

        return None

    async def search_news(self, query):
        params = {
            "qInTitle": query,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
        }
        response = await self._make_request(params=params)
        if response is None:
            return None
        news_response = FootballResponseParser._extract_top_news_by_query(
            newsDict=response["articles"]
        )
        return news_response
