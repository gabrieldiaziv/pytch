from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from analytics.types import Player, Ball, Frame
import numpy as np

PLAYER_BALL_PROXIMITY = 5.0

Coord = tuple[float,float]

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    @property
    def xy(self) -> tuple[float, float]:
        return (self.x, self.y)

    def int(self):
        return (int(self.x), int(self.y))


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def min_x(self) -> float:
        return self.x

    @property
    def min_y(self) -> float:
        return self.y

    @property
    def max_x(self) -> float:
        return self.x + self.width

    @property
    def max_y(self) -> float:
        return self.y + self.height

    @property
    def top_left(self) -> Point:
        return Point(x=self.x, y=self.y)

    @property
    def bottom_right(self) -> Point:
        return Point(x=self.x + self.width, y=self.y + self.height)

    @property
    def bottom_center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y + self.height)

    @property
    def top_center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y)

    @property
    def center(self) -> Point:
        return Point(x=self.x + self.width / 2, y=self.y + self.height / 2)

    def pad(self, padding: float) -> Rect:
        return Rect(
            x=self.x - padding,
            y=self.y - padding,
            width=self.width + 2 * padding,
            height=self.height + 2 * padding,
        )

    def contains_point(self, point: Point) -> bool:
        return self.min_x < point.x < self.max_x and self.min_y < point.y < self.max_y


@dataclass
class Detection:
    rect: Rect
    class_id: int
    class_name: str
    confidence: float
    tracker_id: Optional[int] = -1

    def box(self, with_confidence: bool = True) -> list[float]:
        return [
            self.rect.top_left.x, 
            self.rect.top_left.y,
            self.rect.bottom_right.x,
            self.rect.bottom_right.y,
            self.confidence
        ] if with_confidence else [
            self.rect.top_left.x, 
            self.rect.top_left.y,
            self.rect.bottom_right.x,
            self.rect.bottom_right.y
        ]

def filter_detections(detects: list[Detection], coords: list[Coord], class_name: str) -> list[tuple[Detection, Coord]]:
    return list(filter(
                lambda x: x[0].class_name == class_name,
                zip(detects, coords)
            ))
    
class DetectionClass:
    Ball = "ball"
    Player = "player"
    Referee = "referre"
    Goalkeeper = "goalkeeper"

def get_player_in_possession(
    player_detections: list[tuple[Detection,Coord]], 
    ball_detections: list[tuple[Detection, Coord]],
    proximity: float
) -> Optional[int]:
    if len(ball_detections) != 1:
        return None
    _, b_xy = ball_detections[0]
    for player, p_xy in player_detections:
        dist = ((p_xy[0] - b_xy[0]) ** 2 + (p_xy[1] - b_xy[1]) ** 2) ** 0.5
        if dist < proximity:
            return player.tracker_id

def detects_to_frame(frame: int, detects: list[Detection], coords: list[Coord]) -> Frame:
    
    ball_detects = filter_detections(detects, coords, DetectionClass.Ball)
    players_detects = filter_detections(detects, coords, DetectionClass.Player)

    players = [ Player(x=coord[0], y=coord[1], id=p.tracker_id)
        for p, coord in players_detects
    ]

    if len(ball_detects) == 0:
        return Frame(
            frame_id = frame,
            players = players,
            ball = None
        )
    _, b_coord = ball_detects[0]
    player_in_poss = get_player_in_possession(players_detects, ball_detects, PLAYER_BALL_PROXIMITY)

    return Frame(
        frame_id = frame,
        players = players,
        ball = Ball(
            x = b_coord[0],
            y = b_coord[1],
            player= player_in_poss,
        )
    )
        
   
    




