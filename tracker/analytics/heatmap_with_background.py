import json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from .engine import Viz

class heatmap(Viz):
    def __init__ (self):
        self.name = 'heatmap'
        self.description = 'density heatmap of both teams players'
    
    def generate(self, match: Match) -> go.Figure:
        soccer_filed_img = 'soccer_field_image.png'
        
        data = match.to_json()

        # Extract the mapping of player IDs to teams and match frames
        player_teams = data['header']['player_teams']
        match_frames = data['match']

        # List to hold player data
        player_data = []

        # Iterate over each frame and each player to extract position and team
        for frame in match_frames:
            for player in frame['players']:
                player_id = str(player['id'])  # Ensure player_id is a string for dictionary lookup
                if player_id in player_teams:
                    team = 'Team 1' if player_teams[player_id] == "0" else 'Team 2'
                    player_data.append({'x': player['x'], 'y': player['y'], 'team': team})

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(player_data)

        # Create density heatmaps for each team
        fig = px.density_heatmap(df, x='x', y='y', facet_col='team', nbinsx=30, nbinsy=30, 
                                title='Player Position Density Heatmap', marginal_x='violin', 
                                range_x=[-53, 53], range_y=[-34, 34])

        fig.update_traces(opacity=0.7)

        # Have to import local image using PIL, or else will not display local images (online images are fine regardless)
        from PIL import Image
        img = Image.open(soccer_filed_img)

        # Add the image as a background

        bg_img = dict(
            source=img,
            xref="x",
            yref="y",
            x=-53,  # Adjust these values based on your field's dimensions and scale
            y=34,  # Adjust these values based on your field's dimensions and scale
            sizex=106,  # The width of your field in the same units as your x-axis
            sizey=68,  # The height of your field in the same units as your y-axis
            sizing="stretch",
            opacity=0.5,
            layer="below")

        fig.add_layout_image(bg_img, row=1, col=1)
        fig.add_layout_image(bg_img, row=1, col=2)

        # Remove grid lines
        # fig.update_xaxes(showgrid=False, zeroline=False, row=1, col=1)
        # fig.update_yaxes(showgrid=False, zeroline=False, row=1, col=1)

        # fig.update_xaxes(showgrid=False, zeroline=False, row=1, col=2)
        # fig.update_yaxes(showgrid=False, zeroline=False, row=1, col=2)

        # Save and show the figure
        return fig
