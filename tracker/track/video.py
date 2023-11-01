from __future__ import annotations
from dataclasses import dataclass
from typing import Generator
import os 

import cv2
import numpy as np

def generate_frames(video_path: str) -> Generator[np.ndarray, None, None]:
    video = cv2.VideoCapture(video_path)

    while video.isOpened():
        success, frame = video.read()

        if not success:
            break

        yield frame
    video.release()

@dataclass(frozen=True)
class VideoConfig:
    fps: float
    width: int
    height: int

    def new_video(self, target_path: str) -> cv2.VideoWriter:
        video_target_dir = os.path.dirname(os.path.abspath(target_path))
        os.makedirs(video_target_dir, exist_ok=True)
        return cv2.VideoWriter(
            target_path, 
            fourcc=cv2.VideoWriter_fourcc(*"mp4v"), 
            fps=self.fps, 
            frameSize=(self.width, self.height), 
            isColor=True
        )
