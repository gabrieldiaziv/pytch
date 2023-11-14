from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class Ball:
    x: float
    y: float
    player: Optional[int] = None
    
@dataclass_json
@dataclass
class Player:
    x: float
    y: float
    id: Optional[int]
    team: int

@dataclass_json
@dataclass
class Frame:
    frame_id: int
    players: list[Player]
    ball: Optional[Ball]

@dataclass_json
@dataclass
class Team:
    id: int
    name: str
    color: str

@dataclass_json
@dataclass
class Header:
    team1: Team
    team2: Team
    

@dataclass_json
@dataclass
class Match:
    header: Header
    match: list[Frame]

