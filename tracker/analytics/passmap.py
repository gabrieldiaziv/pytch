import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from .engine import Viz
from .types import Match
from PIL import Image

class passmap(Viz):
    @property
    def name(self) -> str:
        return 'passmap'

    @property
    def description(self) -> str:
        return 'map of completed passes for each team'
    
    def generate(self, match: Match) -> go.Figure:
        

        # Extract the mapping of player IDs to teams and match frames
        player_teams = match.header.player_teams
        match_frames = match.match

        # List to hold pass data
        pass_data = []

        
        last_ball_possession = None
        for frame in match_frames:
            # Check if ball is located and player is assigned
            if frame.ball is not None and frame.ball.player is not None:
                # Check if current ball owner and last known ball owner are on the same team
                if last_ball_possession is not None and player_teams[last_ball_possession.player] == player_teams[frame.ball.player]:
                    pass_data.append({"x0" : last_ball_possession.x, "y0" : last_ball_possession.y, "x1" : frame.ball.x, "y1" : frame.ball.y, "team" : player_teams[frame.ball.player]})
                last_ball_possession = frame.ball

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(pass_data)


        # Create density heatmaps for each team
        fig = px.density_heatmap(df, x='x', y='y', facet_col='team', nbinsx=30, nbinsy=30, 
                                title='Player Position Density Heatmap', marginal_x='violin', 
                                range_x=[-53, 53], range_y=[-34, 34])

        fig.update_traces(opacity=0.7)

        # Have to import local image using PIL, or else will not display local images (online images are fine regardless)
        # img = Image.open(soccer_filed_img)

        # Add the image as a background

        bg_img = dict(
            source=Viz.background(),
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
