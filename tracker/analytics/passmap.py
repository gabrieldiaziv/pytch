import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from .engine import Viz
from .types import Match
from PIL import Image
from plotly.subplots import make_subplots

class passmap(Viz):
    @property
    def name(self) -> str:
        return 'Pass Map'

    @property
    def description(self) -> str:
        return 'Map of completed passes for each team'
    
    def generate(self, match: Match) -> go.Figure:
        

        # Extract the mapping of player IDs to teams and match frames
        player_teams = match.header.player_teams
        match_frames = match.match
        print(match.header.player_teams)

        # List to hold pass data
        pass_data = []

        
        last_ball_possession = None
        for frame in match_frames:
            # Check if ball is located and player is assigned
            if frame.ball is not None and frame.ball.player is not None and frame.ball.player != -1:
                # Check if current ball owner and last known ball owner are on the same team
                if last_ball_possession is not None and last_ball_possession.player in player_teams and \
                    frame.ball.player in player_teams and \
                    player_teams[last_ball_possession.player] == player_teams[frame.ball.player] and last_ball_possession.player != frame.ball.player:
                    #print("Pass from " + str(last_ball_possession.player) + " to " + str(frame.ball.player))
                    pass_data.append({"x0" : last_ball_possession.x, "y0" : last_ball_possession.y * -1, "x1" : frame.ball.x, "y1" : frame.ball.y * -1, "team" : player_teams[frame.ball.player], "passer_id" : last_ball_possession.player, "receiver_id" : frame.ball.player})
                last_ball_possession = frame.ball

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(pass_data)

        fig = make_subplots(rows=1, cols=2, subplot_titles=(match.header.team1.name + " Passes", match.header.team2.name + " Passes"))

        fig.update_xaxes(title_text="x", range=[-53, 53], row=1, col=1)
        fig.update_xaxes(title_text="x", range=[-53, 53], row=1, col=2)

        fig.update_yaxes(title_text="y", range=[-34, 34], row=1, col=1)
        fig.update_yaxes(title_text="y", range=[-34, 34], row=1, col=2)
        
        team0 = df.loc[df["team"] == "0"]
        team1 = df.loc[df["team"] == "1"]

        # print(team0)
        # print(team1)


        fig.add_trace(go.Scatter(x=team0["x0"], y=team0["y0"], name="Pass Start", mode="markers", legendgroup="group1", marker=dict(color="blue",size=12)), row=1, col=1)
        fig.add_trace(go.Scatter(x=team0["x1"], y=team0["y1"], name="Pass End", mode="markers", legendgroup="group2", marker=dict(color="red",size=12)), row=1, col=1)

        fig.add_trace(go.Scatter(x=team1["x0"], y=team1["y0"], name="Pass Start", mode="markers", legendgroup="group1", marker=dict(color="blue",size=12), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=team1["x1"], y=team1["y1"], name="Pass End", mode="markers", legendgroup="group2", marker=dict(color="red",size=12), showlegend=False), row=1, col=2)



        

        bg_img = dict(
            source=Viz.background(),
            xref="x1",
            yref="y",
            x=-53,  # Adjust these values based on your field's dimensions and scale
            y=34,  # Adjust these values based on your field's dimensions and scale
            sizex=106,  # The width of your field in the same units as your x-axis
            sizey=68,  # The height of your field in the same units as your y-axis
            sizing="stretch",
            opacity=0.5,
            layer="below")
        
        bg_img2 = dict(
            source=Viz.background(),
            xref="x2",
            yref="y",
            x=-53,  # Adjust these values based on your field's dimensions and scale
            y=34,  # Adjust these values based on your field's dimensions and scale
            sizex=106,  # The width of your field in the same units as your x-axis
            sizey=68,  # The height of your field in the same units as your y-axis
            sizing="stretch",
            opacity=0.5,
            layer="below")

        fig.add_layout_image(bg_img, row=1, col=1)
        fig.add_layout_image(bg_img2, row=1, col=2)

        
        for x0,y0,x1,y1 in zip(team0["x1"], team0["y1"], team0["x0"], team0["y0"]):
            fig.add_annotation(
                            x=x0,
                            y=y0,
                            xref="x", yref="y",
                            text="",
                            showarrow=True,
                            ax=x1,
                            ay=y1,
                            axref="x",
                            ayref="y",
                            arrowhead=3,
                            arrowwidth=3,
                            arrowcolor='blue',
                            row=1,
                            col=1)

        for x0,y0,x1,y1 in zip(team1["x1"], team1["y1"], team1["x0"], team1["y0"]):
            fig.add_annotation(
                            x=x0,
                            y=y0,
                            xref="x2", yref="y2",
                            text="",
                            showarrow=True,
                            ax=x1,
                            ay=y1,
                            axref="x2",
                            ayref="y2",
                            arrowhead=3,
                            arrowwidth=3,
                            arrowcolor='blue',
                            row=1,
                            col=2
                        )

        #fig.add_layout_image(bg_img, row=1, col=2)

        # Remove grid lines
        # fig.update_xaxes(showgrid=False, zeroline=False, row=1, col=1)
        # fig.update_yaxes(showgrid=False, zeroline=False, row=1, col=1)

        # fig.update_xaxes(showgrid=False, zeroline=False, row=1, col=2)
        # fig.update_yaxes(showgrid=False, zeroline=False, row=1, col=2)

        # Save and show the figure
        return fig
