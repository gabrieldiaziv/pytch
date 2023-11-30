from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Generator

import numpy as np
import cv2 as cv
from ultralytics import YOLO
from ultralytics.engine.results import Boxes, Results
from onemetric.cv.utils.iou import box_iou_batch
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from yolox.tracker.byte_tracker import BYTETracker, STrack

from .video import generate_frames
from .utils import Detection, GenWrapper, Rect
from .localization import localization  

import time

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
        self.localizer = localization.init_segmentation_network(width=960, height=540)
        self.homography_rate = 10
        self.color_rate = 5
        self.kmeans2 = KMeans(n_clusters=2, n_init=10)
        self.kmeans3 = KMeans(n_clusters=3, n_init=10)

    def detect_image(self, img: np.ndarray) -> list[Detection]:
        predicitons: list[Results] = self.model.predict(img)

        detections : list[Detection] = []
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
            # frame_points = [detect.rect.bottom_center for detect in detections] 
            # global_points = localization.get_pitch_locations(img, frame_points, self.localizer)

        return detections 

    def _players_and_color(self, vid_path: str): 
        tracked_frames: defaultdict[int,int]        = defaultdict(lambda: 0)
        tracked_colors: defaultdict[int,np.ndarray] = defaultdict(lambda: np.zeros((3,3)))
        tracked_players : list[list[Detection]] = []

        for i, frame in enumerate(generate_frames(vid_path)):
            if i % 10 == 0:
                print(f'player and color : {i}')

            detections = self.detect_image(frame)
            tracks = self.byte_tracker.update(
                output_results=np.array([d.box() for d in detections]),
                img_info=frame.shape,
                img_size=frame.shape,
            )
            self._match_detections(detections, tracks)

            if i % self.color_rate:
                self._update_detected_colors(frame, detections, tracked_frames, tracked_colors)
            tracked_players.append(detections)


        teams, colors = self._avg_colors(tracked_frames, tracked_colors)
        return tracked_players, teams, colors


    def _avg_colors(self, tracked_frames: dict[int, int], tracked_colors: dict[int, np.ndarray]) -> tuple[dict[int,str], list[str]]:
        for key in tracked_frames:
            for centroid in tracked_colors[key]:
                    centroid /= tracked_frames[key]

        second_avg_color = [tracked_colors[key][1] for key in tracked_colors]
        s = self.kmeans2.fit(second_avg_color)
        centroids = self.kmeans2.cluster_centers_
        labels = s.labels_
        labels = [str(x) for x in labels]
        teams = dict(zip([key for key in tracked_colors], labels))

        colors = [
            '#{:02x}{:02x}{:02x}'.format(int(centroids[0][0]), int(centroids[0][1]), int(centroids[0][2])), 
            '#{:02x}{:02x}{:02x}'.format(int(centroids[1][0]), int(centroids[1][1]), int(centroids[1][2]))
        ]

        return teams, colors


    def detect_video(self, vid_path:str) \
        -> Generator[tuple[np.ndarray, list[Detection], list, dict, list[str], list], None, tuple[dict[int,str], list[str]]]:
        i = 0
        inv_homography = np.eye(3)
        extremities = dict()
        valid_homography = False
        line_names = []
        line_points = []
        global_points = []

        tracked_players, teams, colors, = self._players_and_color(vid_path)

        for detections, frame in zip(tracked_players, generate_frames(vid_path)):

            if i % self.homography_rate == 0:
                res = localization.get_homography(frame, self.localizer)
                print(f'localization frame : {i}')
                if res is not None:
                    valid_homography = True
                    inv_homography, extremities, line_names, line_points = res

            frame_points = [detect.rect.bottom_center.xy + (1,) for detect in detections] 

            if valid_homography:
                global_points = localization.get_pitch_locations(frame_points, inv_homography, test=True)
           
            yield frame, detections, global_points, extremities, line_names, line_points
            i+=1

        return teams, colors

    def _match_detections(self, detects: list[Detection], tracks: list[STrack]):
        detection_boxes = np.array([ d.box(False) for d in detects], dtype=float)
        tracks_boxes = np.array([ track.tlbr for track in tracks], dtype=float)

        iou = box_iou_batch(tracks_boxes, detection_boxes)
        track2detection = np.argmax(iou, axis=1)

        for tracker_i, detect_i in enumerate(track2detection):
            if iou[tracker_i, detect_i] != 0:
                detects[detect_i].tracker_id = tracks[tracker_i].track_id

    def _update_detected_colors(self, frame: np.ndarray, detections: list[Detection], tracked_frames: defaultdict[int,int], tracked_colors: dict[int, np.ndarray]):
        for detection in detections:
            if detection.class_name == "player" and detection.tracker_id != -1:
                box = detection.box(False)
                chopped_height = (int(box[3]) - int(box[1])) / 2
                height_max = int(box[1]) + int(chopped_height)
                img_crop = frame[int(box[1]):height_max, int(box[0]):int(box[2])]
                # cv.imwrite("testing/" + str(detection.tracker_id) + ".jpg", img_crop)
                img_crop_rgb = cv.cvtColor(img_crop, cv.COLOR_BGR2RGB)
                img_crop_rgb = img_crop_rgb.reshape(img_crop_rgb.shape[1]*img_crop_rgb.shape[0], 3)

                s = self.kmeans3.fit(img_crop_rgb)
                labels = self.kmeans3.labels_
                labels = list(labels)
                centroids = self.kmeans3.cluster_centers_
                percent=[]
                for i in range(len(centroids)):
                    j=labels.count(i) 
                    j=j/(len(labels))
                    percent.append(j)
                percentages_and_centroids = list(zip(percent, centroids))
                percentages_and_centroids = sorted(reversed(percentages_and_centroids), reverse=True, key=lambda x: x[0])

                if detection.tracker_id is not None:
                    tracked_frames[detection.tracker_id] += 1
                    tracked_colors[detection.tracker_id] += np.array([c[1] for c in percentages_and_centroids])
