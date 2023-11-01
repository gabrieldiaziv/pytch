from __future__ import annotations
from dataclasses import dataclass
from typing import Generator

import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Boxes, Results
from onemetric.cv.utils.iou import box_iou_batch

from yolox.tracker.byte_tracker import BYTETracker, STrack

from .video import generate_frames
from .utils import Detection, Rect

from .localization import localization  

@dataclass(frozen=True)
class BYTETrackerArgs:
    track_thresh: float = 0.25
    track_buffer: int = 30
    match_thresh: float = 0.8
    aspect_ratio_thresh: float = 3.0
    min_box_area: float = 1.0
    mot20: bool = False

class Tracker:
    def __init__(self, model_type:str = 'best.pt', tracker_args: BYTETrackerArgs = BYTETrackerArgs()):
        self.model = YOLO(model=model_type)
        self.byte_tracker = BYTETracker(tracker_args)
        self.localizer = localization.init_segmentation_network(width=1920, height=1080)

    def detect_image(self, img: np.ndarray) :
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
            frame_points = [detect.rect.bottom_center for detect in detections] 
            global_points = localization.get_pitch_locations(img, frame_points, self.localizer)

        return detections 

    def detect_video(self, vid_path:str) -> Generator[tuple[np.ndarray, list[Detection], list[tuple[float, float]]], None, None]:
        for frame in generate_frames(vid_path):
            detections = self.detect_image(frame)
            print(detections[0].class_id)
            # tracks = self.byte_tracker.update(
            #     output_results=np.array([d.box() for d in detections]),
            #     img_info=frame.shape,
            #     img_size=frame.shape,
            # )

            # detections = self._match_detections(detections, tracks)
            frame_points = [detect.rect.bottom_center for detect in detections] 
            global_points = localization.get_pitch_locations(frame, frame_points, self.localizer)
            global_points = []
            
            yield frame, detections, global_points

    
    def _match_detections(self, detects: list[Detection], tracks: list[STrack]) -> list[Detection]:
        detection_boxes = np.array([ d.box(False) for d in detects], dtype=float)
        tracks_boxes = np.array([ track.tlbr for track in tracks], dtype=float)

        iou = box_iou_batch(tracks_boxes, detection_boxes)
        track2detection = np.argmax(iou, axis=1)

        for tracker_i, detect_i in enumerate(track2detection):
            if iou[tracker_i, detect_i] != 0:
                detects[detect_i].tracker_id = tracks[tracker_i].track_id
        return detects

