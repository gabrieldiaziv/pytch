import json
from .heatmap_with_background import heatmap
from .passmap import passmap
from .types import Match

# Load the JSON file
def analyze():
    with open('./testing/output_redyellow_30.json', 'r') as file:
        data = json.load(file)
        m = Match(**data)

         
        H = passmap()
        H.generate(m).show()

