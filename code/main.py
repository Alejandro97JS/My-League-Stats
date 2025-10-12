import os
from dotenv import load_dotenv
from data_reader import DataReader
from stats_calculator import PointsStatsCalculator
from graficator import Graficator

if __name__ == "__main__":
    # Cargar variables de entorno desde .env
    load_dotenv()
    # BASE_DIR env variable should point to the 
    # project root directory:
    base_dir = os.getenv("BASE_DIR")
    # Path to the CSV points per round file
    csv_points_path = os.path.join(
        base_dir,
        "dataset",
        "points.csv"
    )
    # Read the data using DataReader
    reader = DataReader()
    df = reader.read_points_data(csv_points_path)

    # Instantiate the PointsStatsCalculator
    calculator = PointsStatsCalculator(df)

    # Display the best and worst rounds overall:
    text_rounds_list = []
    best_overall, worst_overall = calculator.get_best_worst_round()
    text_round_overall = "Mejor / Peor Jornada Global:\n"
    text_round_overall += f"\nMejor jornada: {best_overall.get('player')}\n"
    text_round_overall += f"Fue en la jornada: {best_overall.get('round_number')}\n"
    text_round_overall += f"Puntos conseguidos: {best_overall.get('points')}\n"
    text_round_overall += f"\nPeor jornada: {worst_overall.get('player')}\n"
    text_round_overall += f"Fue en la jornada: {worst_overall.get('round_number')}\n"
    text_round_overall += f"Puntos conseguidos: {worst_overall.get('points')}\n"
    print(text_round_overall)
    text_rounds_list.append(text_round_overall)

    # Display the best and worst rounds for each player:
    for player in df.columns[1:]:  # Skip the first column which is 'Jornada'
        best, worst = calculator.get_best_worst_round(player)
        text_round_player = f"Mejor / Peor Jornada de {player}:\n"
        text_round_player += f"\nFue en la jornada: {best.get('round_number')}\n"
        text_round_player += f"Puntos conseguidos: {best.get('points')}\n"
        text_round_player += f"\nFue en la jornada: {worst.get('round_number')}\n"
        text_round_player += f"Puntos conseguidos: {worst.get('points')}\n"
        print(text_round_player)
        text_rounds_list.append(text_round_player)

    # Graphics:
    graficator = Graficator()
    generated_file_paths = []

    df_positions = calculator.get_position_data()
    position_image_path = graficator.plot_lines(df_positions, value_column="position", 
                          reverse_y_axis=True)
    generated_file_paths.append(position_image_path)
    
    df_points = calculator.get_points_data()
    points_image_path = graficator.plot_lines(df_points, value_column="aggregated_points", 
                          round_numbers_to_exclude=[6])
    generated_file_paths.append(points_image_path)
