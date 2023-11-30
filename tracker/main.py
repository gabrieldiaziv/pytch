import json
from analytics.types import Match  
from analytics.heatmap_with_background import heatmap
from analytics.passmap import passmap  

with open('./testing/output_redyellow_30.json', 'r') as file:
    data = json.load(file)
    m = Match.from_dict(data)

     
    H = passmap()
    H.generate(m).show()

