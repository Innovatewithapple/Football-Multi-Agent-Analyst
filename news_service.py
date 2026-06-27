import requests
import os

class News_service:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.session = requests.Session()

    def _make_request(self,params):
        url = self.BASE_URL

        try:
            response = self.session.get(url=url,params=params,timeout=10)
            print(params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print('News api timeout!')

        except requests.exceptions.ConnectionError:
            print("Couldn't connect to News API!")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Unexpected Error: {e}")

        return None

    def search_news(self,query):
        params = {
            "q":query,
            "language":"en",
            "sortBy":"publishedAt",
            "apikey":self.api_key
        }
        print("params")
        response = self._make_request(params=params)
        return response

