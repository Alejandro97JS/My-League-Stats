import os
from dotenv import load_dotenv
from data_reader import DataReader
from stats_calculator import PointsStatsCalculator
from graficator import Graficator
from pdf_converter import PDFPresentation

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
    text_rounds_list.append(
        calculator.get_verbose_best_worst_round(is_overall=True)
    )

    # Display the best and worst rounds for each player:
    for player in df.columns[1:]:  # Skip the first column which is 'Jornada'
        text_rounds_list.append(
            calculator.get_verbose_best_worst_round(player)
        )

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

    # Create PDF presentation:
    pdf_report_file = PDFPresentation(
        filename=os.path.join(base_dir,
            "generated_files",
            "league_report.pdf"
            )
    )
    pdf_report_file.add_text_slide(
        text="Informe de la Liga",
    )
    for image_file_path in generated_file_paths:
        pdf_report_file.add_image_slide(
            image_path=image_file_path
        )
    for text_round in text_rounds_list:
        pdf_report_file.add_text_slide(
            text=text_round
        )
    pdf_report_file.save()
    print(f"PDF report generated at: {pdf_report_file.filename}")
