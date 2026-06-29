class FootballResponseParser:

    @staticmethod
    def _extract_match_data(match: dict, include_score: bool = False):
        match_data = {
            "match_id": match["id"],
            "date": match["utcDate"],
            "competition": match["competition"]["name"],
            "stage": match["stage"],
            "status": match["status"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"]
        }

        if include_score:
            winner = match["score"]["winner"]

            if winner == "DRAW":
                result = "Draw"
            elif winner == "HOME_TEAM":
                result = "Win"
            else:
                result = "Loss"

            match_data.update({
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"],
                "result": result
            })

        return match_data    

    @staticmethod
    def _extract_head2head_match_data(match: dict, include_score: bool = False):
        match_data = {
            "match_id": match["id"],
            "date": match["utcDate"],
            "competition": match["competition"]["name"],
            "stage": match["stage"],
            "status": match["status"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"]
        }

        if include_score:
            winner = match["score"]["winner"]

            if winner == "DRAW":
                result = "Draw"
            elif winner == "HOME_TEAM":
                result = "Win"
            else:
                result = "Loss"

            match_data.update({
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"],
                "result": result
            })

        return match_data    

    @staticmethod
    def _extract_top_scorers(scorers:list,player_ids:list):
        selected_scorers=[]
        if not player_ids:
            return scorers
        else:
            for scorer in scorers:
                for player in player_ids:
                    if scorer['player']['id'] == player:
                        selected_scorers.append(scorer)
                        break
            return selected_scorers
    
    @staticmethod
    def _extract_top_news_by_query(newsDict:list):
        top_five_news_articles_arr=[]
        for news in newsDict[:5]:
            top_five_news_articles = {
                "author":news['author'],
                "title":news['title'],
                "description":news['description'],
                "publishedAt":news['publishedAt'],
                "content":news['content'],
                "url":news['url'],
                "source_name":news['source']['name']
            }
            top_five_news_articles_arr.append(top_five_news_articles)

        return top_five_news_articles_arr