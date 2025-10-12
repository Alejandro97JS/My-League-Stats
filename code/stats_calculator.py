import os
import pandas as pd
import json

class PointsStatsCalculator:

    def __init__(self, dataframe):
        self.data_dict = self.__transform_round_points_to_json(dataframe)

    def __transform_round_points_to_json(self, dataframe):
        """
        Transforms a DataFrame with the structure of points for each team
        per round into a dictionary with the following structure:
        [
            {
                "round": 1,
                "data": [
                    {
                        "team": "Test Team",
                        "round_points": 100,
                        "aggregated_points": 300,
                        "position": 1
                    }
                ]
            }
            ...
        ]

        :param dataframe: pd.DataFrame - DataFrame structured as needed.
        :return: list - A JSON-like dictionary matching the previous structure.
        """
        # Create a list to store the final JSON structure
        result = []

        # Iterate over the rows of the DataFrame
        for index, row in dataframe.iterrows():
            # Extract the round by removing the leading 'J' from the Jornada value
            round_number = int(row['Jornada'][1:])

            # Initialize a list to hold team data for the current round
            round_data = []
            
            # Iterate through each team column to gather points and calculate aggregated points
            for team in dataframe.columns[1:]:
                round_points = row[team]
                
                # Calculate the aggregated points by summing the rows for the current team up to this round
                aggregated_points = dataframe.loc[:index, team].sum()

                # Add the team data to the round's list
                round_data.append({
                    "team": team,
                    "round_points": int(round_points),
                    "aggregated_points": int(aggregated_points),
                    "position": None  # Placeholder for now, can be calculated if needed
                })

            # Calculate positions based on aggregated points for this round
            # Sorting in descending order of aggregated points
            round_data = sorted(round_data, key=lambda x: x["aggregated_points"], reverse=True)

            # Assign positions based on sorted order
            for position, team_data in enumerate(round_data, start=1):
                team_data["position"] = position

            # Append the round's data to the result list
            result.append({
                "round": round_number,
                "data": round_data
            })
        # Save the result as a JSON file
        json_folder_path = os.path.join(
            os.getenv('BASE_DIR'),
            'generated_files'
        )
        json_file_path = os.path.join(
            json_folder_path,
            'points_stats.json'
        )
        os.makedirs(json_folder_path, exist_ok=True)
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        result = sorted(result, key=lambda x: x["round"])
        return result

    def get_position_data(self):
        records = []
        for round_info in self.data_dict:
            round_number = round_info["round"]
            for team_data in round_info["data"]:
                records.append({
                    "round": round_number,
                    "player": team_data["team"],
                    "position": team_data["position"]
                })
        return pd.DataFrame(records, columns=["round", "player", "position"])
    
    def get_points_data(self):
        records = []
        for round_info in self.data_dict:
            round_number = round_info["round"]
            for team_data in round_info["data"]:
                records.append({
                    "round": round_number,
                    "player": team_data["team"],
                    "aggregated_points": team_data["aggregated_points"]
                })
        return pd.DataFrame(records, columns=["round", "player", "aggregated_points"])
    
    def get_best_worst_round(self, player=None):
        best = {"player": None, "round_number": None, "points": float('-inf')}
        worst = {"player": None, "round_number": None, "points": float('inf')}

        for round_info in self.data_dict:
            round_number = round_info["round"]
            for team_data in round_info["data"]:
                if player is not None and team_data["team"] != player:
                    continue
                points = team_data["round_points"]
                if points > best["points"]:
                    best = {
                        "player": team_data["team"],
                        "round_number": round_number,
                        "points": points
                    }
                if points < worst["points"]:
                    worst = {
                        "player": team_data["team"],
                        "round_number": round_number,
                        "points": points
                    }
        # If player is specified but not found, return None for both
        if player is not None and (best["player"] is None or worst["player"] is None):
            return None, None
        return best, worst

    def get_data_dict(self):
        return self.data_dict
