import json
import plotly.express as px
import pandas as pd

# Load the JSON file
with open('analytics/testing/tmpvvub75qv.json', 'r') as file:
    data = json.load(file)

# Extract the mapping of player IDs to teams and match frames
player_teams = data['header']['player_teams']
match_frames = data['match']

# List to hold player data
ball_data = []

# Iterate over each frame and each player to extract position and team
for frame in match_frames:
    if frame["ball"] is not None:
        print(frame["ball"])
        ball_data.append({"x" : frame["ball"]["x"], "y" : frame["ball"]["y"]})

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(ball_data)

# Create density heatmaps for each team
fig = px.density_heatmap(df, x='x', y='y', nbinsx=30, nbinsy=30, 
                         title='Ball Position Heatmap')
fig.show()