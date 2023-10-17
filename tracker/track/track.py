from __future__ import annotations
from dataclasses import dataclass, field

import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Boxes, Results

from track.utils import Detection, Rect


@dataclass
class Tracker:
    model = YOLO()

    def detect_image(self, img) -> list[Detection]:
        predicitons: list[Results] = self.model.predict(img)

        detections = []
        boxes = predicitons[0].boxes
        if isinstance(boxes, Boxes) and isinstance(self.model.names, dict):
            for b in boxes:
                id = b.cls.item()
                x0, y0, x1, y1 = b.xyxy[0].tolist()
                conf = b.conf.item()
                detections.append(
                    Detection(
                        Rect(x0, y0, x1 - x0, y1 - y0), id, self.model.names[id], conf
                    )
                )

        return detections 
