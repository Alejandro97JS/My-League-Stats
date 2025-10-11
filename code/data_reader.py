import pandas as pd

class DataReader:

    def read_points_data(self, filepath: str) -> pd.DataFrame:
        """
        Reads a CSV file containing league points data with a specific structure.

        This method is designed to read CSV files structured as needed, where:
            - The first row contains headers: 'Jornada' (matchday) and team names.
            - Each subsequent row contains the matchday identifier and the corresponding points for each team.
            - The delimiter used is a semicolon (';').

        Args:
            filepath (str): The path to the CSV file to be read.

        Returns:
            pandas.DataFrame: A DataFrame containing the points data, with columns for 'Jornada' and each team.

        Example:
            >>> df = read_points_data('path/to/chart.csv')
            >>> print(df.head())
        """
        return pd.read_csv(filepath, delimiter=';', encoding='utf-8')
