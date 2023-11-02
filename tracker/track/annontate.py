from dataclasses import dataclass
from typing import Sequence

import cv2 
import numpy as np

from track.utils import Rect, Point, Detection

Color = Sequence[int]

def draw_rect(image: np.ndarray, rect: Rect, color: Color, thickness: int = 2) -> np.ndarray:
    cv2.rectangle(image, rect.top_left.int(), rect.bottom_right.int(), color, thickness)
    return image


def draw_filled_rect(image: np.ndarray, rect: Rect, color: Color ) -> np.ndarray:
    cv2.rectangle(image, rect.top_left.int(), rect.bottom_right.int(), color, -1)
    return image


def draw_polygon(image: np.ndarray, countour: np.ndarray, color: Color, thickness: int = 2) -> np.ndarray:
    cv2.drawContours(image, [countour], 0, color, thickness)
    return image


def draw_filled_polygon(image: np.ndarray, countour: np.ndarray, color: Color) -> np.ndarray:
    cv2.drawContours(image, [countour], 0, color, -1)
    return image


def draw_text(image: np.ndarray, anchor: Point, text: str, color: Color, thickness: int = 2) -> np.ndarray:
    cv2.putText(image, text, anchor.int(), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, thickness, 2, False)
    return image


def draw_ellipse(image: np.ndarray, rect: Rect, color: Color, thickness: int = 2) -> np.ndarray:
    cv2.ellipse(
        image,
        center=rect.bottom_center.int(),
        axes=(int(rect.width), int(0.35 * rect.width)),
        angle=0.0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=thickness,
        lineType=cv2.LINE_4
    )
    return image

# white
BALL_COLOR = (255, 255, 255) 
# red
GOALKEEPER_COLOR = (133, 1, 1) 
# green
PLAYER_COLOR = (0, 212, 187) 
# yellow
REFEREE_COLOR =(255, 255, 0) 

COLORS : dict[int, Color] = {
    0: BALL_COLOR,
    1: GOALKEEPER_COLOR,
    2: PLAYER_COLOR,
    3: REFEREE_COLOR
}
THICKNESS = 4

@dataclass
class BaseAnnotator:
    colors: dict[int, Color]
    thickness: int

    def annotate(self, image: np.ndarray, detections: list[Detection]) -> np.ndarray:
        annotated_image = image.copy()
        for detection in detections:
            annotated_image = draw_ellipse(
                image=image,
                rect=detection.rect,
                color=self.colors[detection.class_id],
                thickness=self.thickness
            )
        return annotated_image

# text annotator to display tracker_id
@dataclass
class TextAnnotator:
    background_color: Color
    text_color: Color
    text_thickness: int

    def annotate(self, image: np.ndarray, detections: list[Detection], extra: list) -> np.ndarray:
        annotated_image = image.copy()
        for detection, info in zip(detections, extra):
            # if tracker_id is not assigned skip annotation
            if detection.tracker_id is None:
                continue

            label = f'{str(detection.tracker_id)} - {info[:2]}'
            # calculate text dimensions
            size, _ = cv2.getTextSize(
                label, 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                thickness=self.text_thickness)
            width, height = size
            
            # calculate text background position
            center_x, center_y = detection.rect.bottom_center.xy
            x = center_x - width // 2
            y = center_y - height // 2 + 10
            
            # draw background
            # annotated_image = draw_filled_rect(
            #     image=annotated_image, 
            #     rect=Rect(x=x, y=y, width=width, height=height).pad(padding=5), 
            #     color=self.background_color)
            
            # draw text
            annotated_image = draw_text(
                image=annotated_image, 
                anchor=Point(x=x, y=y + height), 
                text=label, 
                color=self.text_color, 
                thickness=self.text_thickness)
        return annotated_image
     
