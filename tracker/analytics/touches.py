from typing import Optional

from .engine import Viz
from .types import Match

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class touchesXY(Viz):
    def __init__(self, x_range: Optional[tuple[float,float]], y_range: Optional[tuple[float,float]]):
        self.x_range = x_range
        self.y_range = y_range

    @property
    def name(self) -> str: 
        x = "" if self.x_range is None else f"X [{self.x_range}]"
        y = "" if self.y_range is None else f" and Y [{self.y_range}]"
        return "touches in " + x + y

    @property
    def description(self) -> str:
        return 'density heatmap of both teams players'
    
    def generate(self, match: Match) -> go.Figure:
        
        player_in_possesion = [] 
        player_teams = match.header.player_teams


        team1_name = match.header.team1.name 
        team2_name = match.header.team2.name 

        for frame in match.match:
            ball = frame.ball
            if ball is not None and ball.player is not None:
                p_id = ball.player

                # get player that has ball
                player = list(filter(lambda x: x.id == p_id, frame.players))
                if len(player) == 0:
                    continue
                player = player[0]
                
                # if x range exists and not in range then continue
                if self.x_range is not None \
                    and not (self.x_range[0] <= player.x <= self.x_range[1]):
                        continue

                # if y range exists and not in range then continue
                if self.y_range is not None \
                    and not (self.y_range[0] <= player.y <= self.y_range[1]):
                        continue

                if p_id in player_teams:
                    team = team1_name if player_teams[p_id] == "0" else team2_name
                    player_in_possesion.append({'x': player.x, 'y': -player.y, 'team': team})

        print(player_in_possesion)


        df = pd.DataFrame(player_in_possesion)
        if 'team' not in df.columns:
            # If there's no 'team' column, create a DataFrame with placeholder data for all teams
            all_teams = set(player_teams.values())
            placeholder_data = [{'x': None, 'y': None, 'team': team} for team in all_teams]
            df = pd.DataFrame(placeholder_data)

        teams_present = df['team'].unique()
        if len(teams_present) < 2:
            # Identify the missing team(s) and add an empty row for them
            missing_teams = set([team1_name, team2_name]) - set(teams_present)
            for team in missing_teams:
                missing_df = pd.DataFrame({'x': [None], 'y': [None], 'team': [team]})       # Create density heatmaps for each team
                df = pd.concat([df, missing_df], ignore_index=True)

        fig = px.density_heatmap(
            df, x='x', y='y', 
            facet_col='team', nbinsx=30, nbinsy=30, 
            title=self.name, 
            range_x=[-53, 5], range_y=[-34, 34]
        )

        fig.update_traces(opacity=0.7)


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
            layer="below"
        )

        fig.add_layout_image(bg_img, row=1, col=1)
        fig.add_layout_image(bg_img, row=1, col=2)

        return fig

