import os
import pandas as pd
from dotenv import load_dotenv
from stats_calculator import PointsStatsCalculator
from graficator import Graficator
from pdf_converter import PDFPresentation
from ai_data_assistant import OpenAIDataAssistant

if __name__ == "__main__":
    # Cargar variables de entorno desde .env
    load_dotenv()
    # BASE_DIR env variable should point to the 
    # project root directory:
    base_dir = os.getenv("BASE_DIR")
    # Check if we have to include market data:
    include_market_data = str(os.getenv('INCLUDE_MARKET_DATA')).lower() == "true"
    # Path to the CSV points per round file
    csv_points_path = os.path.join(
        base_dir,
        "dataset",
        "points.csv"
    )
    # Read points data using DataReader
    df = pd.read_csv(csv_points_path, delimiter=';', encoding='utf-8')

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

    # Market data:
    if include_market_data:
        # Path to the CSV market data file
        csv_market_path = os.path.join(
            base_dir,
            "dataset",
            "market.csv"
        )
        # Read the data:
        df_market = pd.read_csv(csv_market_path, delimiter=';', encoding='utf-8')
        market_data_dict = calculator.get_market_movements_dict(df_market)

    # AI Questions:
    ai_questions_list = [
        {
            "readable_question": "Lo más destacado",
            "ai_question": "¿Qué es lo más destacado de los datos hasta ahora?",
            "data": calculator.get_data_dict()
        },
        {
            "readable_question": "Una curiosidad",
            "ai_question": "¿Qué curiosidad o dato curioso y rebuscado ves en los datos?",
            "data": calculator.get_data_dict()
        },
        {
            "readable_question": "Tendencias",
            "ai_question": "¿Quién tiene una mejor y peor tendencia fijándose solamente en las últimas jornadas?",
            "data": calculator.get_data_dict()
        },
        {
            "readable_question": "Una predicción",
            "ai_question": "¿Qué predicción harías sobre las siguientes jornadas? Responde lo más destacado en tres o cuatro frases.",
            "data": calculator.get_data_dict()
        }
    ]
    if include_market_data:
        ai_questions_list.append(
            {
                "readable_question": "El mercado",
                "ai_question": "Dime un dato curioso y relevante sobre el número de operaciones en el mercado de fichajes por cada equipo: ",
                "data": market_data_dict
            }
        )
    ai_answers_list = []
    open_ai_api_token = os.getenv('OPEN_AI_API_TOKEN')
    if open_ai_api_token:
        ai_data_assistant = OpenAIDataAssistant(api_token=open_ai_api_token)
        for question in ai_questions_list:
            answer = ai_data_assistant.ask_insight(f"{question.get('ai_question')}: {question.get('data')}")
            ai_answers_list.append(f'{question.get("readable_question")}\nIA: "{answer}"')

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
    if include_market_data:
        pdf_report_file.add_image_slide(
            image_path=graficator.plot_market_moves_bar(market_data_dict)
        )
    for ai_answer in ai_answers_list:
        pdf_report_file.add_text_slide(
            text=ai_answer
        )
    pdf_report_file.save()
    print(f"PDF report generated at: {pdf_report_file.filename}")
