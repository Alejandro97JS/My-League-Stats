from data_reader import DataReader
from stats_calculator import PointsStatsCalculator
from graficator import Graficator

if __name__ == "__main__":
    # Path to the CSV file
    csv_path = "" # TODO: Env variables

    # Read the data using DataReader
    reader = DataReader()
    df = reader.read_points_data(csv_path)

    # Instantiate the PointsStatsCalculator
    calculator = PointsStatsCalculator(df)

    # Display the best and worst rounds overall:
    print(calculator.get_best_worst_round())

    # Display the best and worst rounds for each player:
    for player in df.columns[1:]:  # Skip the first column which is 'Jornada'
        best, worst = calculator.get_best_worst_round(player)
        print(f"\nPlayer: {player}")
        print(f"  Best Round: {best}")
        print(f"  Worst Round: {worst}")

    # Graphics:
    graficator = Graficator()
    
    df_positions = calculator.get_position_data()
    graficator.plot_lines(df_positions, value_column="position", 
                          reverse_y_axis=True)
    
    df_points = calculator.get_points_data()
    graficator.plot_lines(df_points, value_column="aggregated_points", 
                          round_numbers_to_exclude=[6])
