from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


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
    tracker_id: Optional[int] = None

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
