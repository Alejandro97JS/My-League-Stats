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

    def plot_market_moves_bar(self, moves_dict: dict) -> str:
        """
        Generates a bar plot where the x-axis represents teams and the y-axis is the number of market moves.
        The plot is saved as an image in the 'generated_files' folder.

        Args:
            moves_dict (dict): Dictionary with team names as keys and number of moves as values.

        Returns:
            str: Path to the saved plot image.
        """
        import matplotlib.cm as cm

        # Sort moves_dict by number of moves in descending order
        sorted_items = sorted(moves_dict.items(), key=lambda x: x[1], reverse=True)
        teams = [item[0] for item in sorted_items]
        moves = [item[1] for item in sorted_items]

        # Normalize moves for colormap (higher moves = darker blue, lower = normal blue)
        norm = plt.Normalize(vmin=min(moves), vmax=max(moves))
        cmap = cm.get_cmap('Blues')

        # Invert the normalized values so that higher moves are darker blue
        colors = [cmap(norm(val)) for val in moves]

        # To ensure higher moves are darker, reverse the colormap
        colors = [cmap(0.4 + 0.6 * (val - min(moves)) / (max(moves) - min(moves) if max(moves) != min(moves) else 1)) for val in moves]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(teams, moves, color=colors)
        plt.xlabel('Equipo')
        plt.ylabel('Compras/Ventas')
        plt.title('Movimientos de Mercado por Equipo')
        plt.xticks(rotation=30, ha='right')

        # Annotate bars with values
        for bar, value in zip(bars, moves):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value),
                     ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        output_dir = os.path.join(
            os.getenv('BASE_DIR'),
            'generated_files'
        )
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'market_moves_per_team.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        return output_path
