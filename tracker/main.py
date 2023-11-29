import json
from analytics.types import Match  
from analytics.heatmap_with_background import heatmap  

with open('./analytics/testing/match-30.json', 'r') as file:
    data = json.load(file)
    m = Match.from_dict(data)

     
    H = heatmap()
    H.generate(m).show()

