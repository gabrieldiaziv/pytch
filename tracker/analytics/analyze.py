import json
from .heatmap_with_background import heatmap
from .types import Match

# Load the JSON file
def analyze():
    with open('.trcking/testing/match-30.json', 'r') as file:
        data = json.load(file)
        m = Match(**data)

         
        H = heatmap()
        H.generate(m).show()

