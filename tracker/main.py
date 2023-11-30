import json
from analytics.types import Match  
from analytics.heatmap_with_background import heatmap  
from analytics.touches import touchesXY  

with open('./analytics/testing/output_redyellow_30.json', 'r') as file:
    data = json.load(file)
    m = Match.from_dict(data)

     

    H = touchesXY(x_range=(-53, -18), y_range=None)
    H.generate(m).show()
    H = touchesXY(x_range=(-18, 18), y_range=None)
    H.generate(m).show()
    H = touchesXY(x_range=(18, 53), y_range=None)
    H.generate(m).show()

