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
