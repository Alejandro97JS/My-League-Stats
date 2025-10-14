# My-League-Stats
## 🏆 Fantasy League Football Statistics

A fantasy football league statistics analyzer that provides detailed insights about each team performance, generating a PDF report (in Spanish) with interesting data and graphics for your fantasy league with your friends.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎮 Overview

My-League-Stats is a Python-based application that uses fantasy football leagues data to process and analyze team statistics for your fantasy league. The application provides detailed statistics about each team, generating a report as a PDF file.

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/alejandro97js/My-League-Stats.git
cd My-League-Stats
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. The only mandatory env var in your `.env` file (you have to create it!) is `BASE_DIR`, the absolute path to the project's root directory:
```env
BASE_DIR=your_api_key_here
```
Additionally, you can set up `OPEN_AI_API_TOKEN` env var with your api key to the OpenAI API, in order to ask AI models for interesting insights in the data. You can also set up `INCLUDE_MARKET_DATA` as `True`, and the script will look for the `.csv` file with market data and will analyze it.

4. You have to create a `/dataset` folder in the project's root directory and, inside it, you have to put your `points.csv` file, with the following structure:
```csv
Jornada;Team Thunder;The Stars;Just My Team;Another Team;Team Example
J1;56;39;7;56;69
J2;64;38;40;43;60
J6;29;45;21;34;52
J3;46;54;36;25;51
```

If you are asking for market data analysis (`INCLUDE_MARKET_DATA` env var), you also need to have in that directory a `market.csv` file with the following structure:
```csv
Mes;Team Thunder;The Stars;Just My Team;Another Team;Team Example
Julio 2025;1;0;1;0;0
Agosto 2025;58;22;14;22;32
Septiembre 2025;46;3;13;18;17
Octubre 2025;16;6;2;1;5
```

Some fantasy leagues apps allow to download these csv files directly with the needed structure.

## 💻 Usage

Run the main application:

```bash
python main.py
```

## 📁 Project Structure

```
My-League-Stats/
├── .env.example         # Example of environment variables (just for documentation)
├── .env                 # Environment variables (not in repo)
├── requirements.txt     # Python dependencies
└── dataset/             # Input data
|    ├── points.csv      # Mandatory
|    └── market.csv      # Optional
└── code/                # Source code
|    ├── ...             # Python files
└── generated_files/     # Directory where results will be created (the folder
                         # will be created if it does not exist, too)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](#file:LICENSE) file for details.
