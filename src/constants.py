import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

layout = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "rgb(255, 255, 255)",
    "font": {
        "family": "Courier New, monospace",
        "size": 14,
        "color": "#fff",
    },
}

markdown = """
    # Welcome to Stock Viewer
    Stock Viewer is a simple app that gets the stock prices from an API and does some visualisations, 
    the purpose of this app is just to showcase my abilties to create a reliable tool.
"""
