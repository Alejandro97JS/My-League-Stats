import os
import pandas as pd
import matplotlib.pyplot as plt

class Graficator:
    """
    A class to generate various plots from league statistics data.
    """
    def plot_lines(self, df: pd.DataFrame, value_column: str = None, reverse_y_axis=False, 
                   round_numbers_to_exclude=None) -> None:
        """
        Generates a line plot where the x-axis represents the rounds, the y-axis is the value,
        and each player is represented as a separate colored line in the plot.
        The plot is saved as an image in the 'generated_files' folder.

        Args:
            df (pd.DataFrame): DataFrame with columns 'round', 'player', and a value column.
            value_column (str, optional): Name of the column representing the value to plot.
                If None, it is inferred as the column that is not 'round' or 'player'.
            reverse_y_axis (bool, optional): If True, the y-axis will be reversed (descending order).
            round_numbers_to_exclude (list, optional): List of round numbers to exclude from the plot.
        """
        if value_column is None:
            value_column = next(
                col for col in df.columns if col not in ['round', 'player']
            )
        # Exclude specified rounds if provided
        if round_numbers_to_exclude is not None:
            df = df[~df['round'].isin(round_numbers_to_exclude)]

        # Create a wide horizontal figure
        plt.figure(figsize=(14, 6))
        for player, group in df.groupby('player'):
            plt.plot(group['round'], group[value_column], marker='o', label=player)
        # Visual translation of column names
        visual_names = {
            'position': 'Posición',
            'aggregated_points': 'Puntos',
        }
        y_label = visual_names.get(value_column, value_column)
        title_value = visual_names.get(value_column, value_column)
        plt.xlabel('Jornada')
        plt.ylabel(y_label)
        plt.title(f'{title_value} por Jornada y Equipo')

        # Show grid in the background
        plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.7, alpha=0.7)

        # Legend below the plot, outside of it
        plt.legend(title='Equipo', loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False)
        plt.tight_layout(rect=[0, 0.08, 1, 1])

        if reverse_y_axis:
            plt.gca().invert_yaxis()

        # Create the directory if it doesn't exist
        output_dir = os.path.join(
            os.getenv('BASE_DIR'),
            'generated_files'
        )
        os.makedirs(output_dir, exist_ok=True)
        # Use the visual name also in the generated file
        output_path = os.path.join(output_dir, f'{value_column}_per_round_and_team.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        return output_path
