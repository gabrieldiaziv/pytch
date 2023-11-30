from collections import namedtuple

from typing import Optional
from .engine import Viz
from .types import Match, Player

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class conversions(Viz):
    def __init__(self, name: str, desc: str, conversion_dist: float):
        self.conversion_dist = conversion_dist
        self._name = name
        self._desc = desc

    @property
    def name(self) -> str:
        return self._name
    @property
    def description(self) -> str:
        return self._desc

    def generate(self, match: Match) -> go.Figure:
        
        team1_name = match.header.team1.name 
        team2_name = match.header.team2.name 

        conversions = []
 
        PLAYER = 0
        TEAM = 1
        prev_player: Optional[tuple[Player, str]] = None

        player_teams = match.header.player_teams
        
        for frame in match.match:
            ball = frame.ball
            if ball is not None and ball.player is not None:
                p_id = ball.player

                # get player that has ball
                player = list(filter(lambda x: x.id == p_id, frame.players))
                if len(player) == 0:
                    continue
                player = player[0]

                if prev_player == None:
                    prev_player = (player, player_teams[player.id])

                elif player.id in player_teams and \
                    player_teams[player.id] != prev_player[1]:

                    dist = ((prev_player[PLAYER].x - player.x) ** 2 + (prev_player[PLAYER].y - player.y) ** 2) **.5
                    if dist < self.conversion_dist: 
                        team = team1_name if prev_player[TEAM] == "0" else team2_name
                        conversions.append(
                            {'x0': prev_player[PLAYER].x, 'y0':-prev_player[PLAYER].y, 'x1': player.x, 'y1':-player.y, 'team': team} 
                        )
                    prev_player = (player, player_teams[player.id])
                else:
                    prev_player = (player, prev_player[TEAM])



        df = pd.DataFrame(conversions)

        if 'team' not in df.columns:
            # If there's no 'team' column, create a DataFrame with placeholder data for all teams
            all_teams = set([team1_name, team2_name])
            placeholder_data = [
                {'x0': None, 'y0':None, 'x1': None, 'y1':None, 'team': team} 
                 for team in all_teams
            ]
            df = pd.DataFrame(placeholder_data)

        fig = go.Figure()

        color_map = {team1_name: 'red', team2_name: 'blue'}

# Add arrows for each conversion
        for team in [team1_name, team2_name]:
            team_data = df[df['team'] == team]


            fig.add_trace(go.Scatter(
                x=team_data['x0'],
                y=team_data['y0'],
                mode='lines+markers',
                line=dict(color=color_map[team], width=2),
                marker=dict(color=color_map[team], size=10),
                name=team,
                showlegend=True,
                hoverinfo='none',
            ))

                # Add arrow annotations
            for _, row in team_data.iterrows():
                fig.add_annotation(
                    x=row['x1'],
                    y=row['y1'],
                    ax=row['x0'],
                    ay=row['y0'],
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    text="",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=color_map[team],
                )

        fig.update_layout(
            title=self.name,
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
        )

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

        fig.update_xaxes(range=[-53,53])
        fig.update_yaxes(range=[-34,34])
        fig.add_layout_image(bg_img)



        return fig












