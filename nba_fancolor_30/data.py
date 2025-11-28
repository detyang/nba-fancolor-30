# nba_fnacolor_30/data.py

TEAMS = [
    {"name": "Atlanta Hawks", "abbr": "ATL", "color": "#C8102E"},
    {"name": "Boston Celtics", "abbr": "BOS", "color": "#007A33"},
    {"name": "Brooklyn Nets", "abbr": "BKN", "color": "#000000"},
    {"name": "Charlotte Hornets", "abbr": "CHA", "color": "#1D1160"},
    {"name": "Chicago Bulls", "abbr": "CHI", "color": "#CE1141"},
    {"name": "Cleveland Cavaliers", "abbr": "CLE", "color": "#6F263D"},
    {"name": "Dallas Mavericks", "abbr": "DAL", "color": "#00538C"},
    {"name": "Denver Nuggets", "abbr": "DEN", "color": "#0E2240"},
    {"name": "Detroit Pistons", "abbr": "DET", "color": "#C8102E"},
    {"name": "Golden State Warriors", "abbr": "GSW", "color": "#1D428A"},
    {"name": "Houston Rockets", "abbr": "HOU", "color": "#CE1141"},
    {"name": "Indiana Pacers", "abbr": "IND", "color": "#002D62"},
    {"name": "LA Clippers", "abbr": "LAC", "color": "#C8102E"},
    {"name": "Los Angeles Lakers", "abbr": "LAL", "color": "#552583"},
    {"name": "Memphis Grizzlies", "abbr": "MEM", "color": "#5D76A9"},
    {"name": "Miami Heat", "abbr": "MIA", "color": "#98002E"},
    {"name": "Milwaukee Bucks", "abbr": "MIL", "color": "#00471B"},
    {"name": "Minnesota Timberwolves", "abbr": "MIN", "color": "#0C2340"},
    {"name": "New Orleans Pelicans", "abbr": "NOP", "color": "#0C2340"},
    {"name": "New York Knicks", "abbr": "NYK", "color": "#006BB6"},
    {"name": "Oklahoma City Thunder", "abbr": "OKC", "color": "#007AC1"},
    {"name": "Orlando Magic", "abbr": "ORL", "color": "#0077C0"},
    {"name": "Philadelphia 76ers", "abbr": "PHI", "color": "#006BB6"},
    {"name": "Phoenix Suns", "abbr": "PHX", "color": "#1D1160"},
    {"name": "Portland Trail Blazers", "abbr": "POR", "color": "#E03A3E"},
    {"name": "Sacramento Kings", "abbr": "SAC", "color": "#5A2D81"},
    {"name": "San Antonio Spurs", "abbr": "SAS", "color": "#C4CED4"},
    {"name": "Toronto Raptors", "abbr": "TOR", "color": "#CE1141"},
    {"name": "Utah Jazz", "abbr": "UTA", "color": "#002B5C"},
    {"name": "Washington Wizards", "abbr": "WAS", "color": "#002B5C"},
]

FAVOR_LEVELS = ["Hometeam", "Like", "Neutral", "Dislike", "Hate"]

NUM_COLS = 6

COLOR_MAP = {
    "Hometeam": "#1d4ed8",
    "Like": "#22c55e",
    "Neutral": "#808080", 
    "Dislike": "#fdba74",
    "Hate": "#c91313",
}