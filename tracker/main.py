import json
from analytics.conversions import conversions
from analytics.types import Match  
from analytics.heatmap_with_background import heatmap  
from analytics.touches import touchesXY  
from analytics.passmap import passmap
from analytics.engine import Engine

engine = Engine(vizs=[
    heatmap(),
    touchesXY(x_range=(-53, -18), y_range=None),
    touchesXY(x_range=(-18, 18), y_range=None),
    touchesXY(x_range=(18, 53), y_range=None),
    passmap(),
    conversions(name="Turnovers", desc="shows when a team has a turnover any where across the field.", conversion_dist=float('inf')),
    conversions(name="Successful Tackles", desc="shows when a team has a turnover because of sucessful tackle.", conversion_dist=5.0),
])

with open('./analytics/testing/1sec.json', 'r') as file:
    data = json.load(file)
    m = Match.from_dict(data)
     
    for v in engine.compute(m):
        print(v)

