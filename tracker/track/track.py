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
        self.localizer = localization.init_segmentation_network(width=960, height=540)
        self.homography_rate = 10

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
            # global_points = localization.get_pitch_locations(img, frame_points, self.localizer)

        return detections 

    def detect_video(self, vid_path:str) -> tuple[list[tuple[np.ndarray, list[Detection], list[tuple[float, float]], dict, list, list]], dict, list] :
        i = 0
        output = []
        inv_homography = np.eye(3)
        extremities = dict()
        line_names = []
        line_points = []
        tracked_frames = dict()
        tracked_colors = defaultdict(lambda: [[0 for _ in range(3)] for _ in range(3)])


        for frame in generate_frames(vid_path):
            if i % self.homography_rate ==0:
                inv_homography, extremities, line_names, line_points = localization.get_homography(frame, self.localizer)
                
            detections = self.detect_image(frame)
            tracks = self.byte_tracker.update(
                output_results=np.array([d.box() for d in detections]),
                img_info=frame.shape,
                img_size=frame.shape,
            )

            detections = self._match_detections(detections, tracks)
            detections, tracked_frames, tracked_colors = self._update_detected_colors(frame, detections, tracked_frames, tracked_colors)
            frame_points = [detect.rect.bottom_center.xy + (1,) for detect in detections] 
            global_points = localization.get_pitch_locations(frame_points, inv_homography, test=True)
           
            output.append((frame, detections, global_points, extremities, line_names, line_points))
            i+=1
        # get average colors for each tracked player
        for key in tracked_frames:
            index = 0
            for centroid in tracked_colors[key]:
                for i in range(3):
                    centroid[i] /= tracked_frames[key]
                centroid_bgr = (centroid[2], centroid[1], centroid[0])
                solid_img = np.full((100, 100, 3), centroid_bgr, dtype=np.uint8)
                cv.imwrite("testing/%d_color_%d.jpg"%(key,index),solid_img)
                index += 1
        second_avg_color = [tracked_colors[key][1] for key in tracked_colors]
        kmeans = KMeans(n_clusters=2, n_init=10)
        s = kmeans.fit(second_avg_color)
        centroids = kmeans.cluster_centers_
        labels = s.labels_
        labels = [str(x) for x in labels]
        teams = dict(zip([key for key in tracked_colors], labels))

        colors = ['#{:02x}{:02x}{:02x}'.format(int(centroids[0][0]), int(centroids[0][1]), int(centroids[0][2])), '#{:02x}{:02x}{:02x}'.format(int(centroids[1][0]), int(centroids[1][1]), int(centroids[1][2]))]
        return output, teams, colors

    def _match_detections(self, detects: list[Detection], tracks: list[STrack]) -> list[Detection]:
        detection_boxes = np.array([ d.box(False) for d in detects], dtype=float)
        tracks_boxes = np.array([ track.tlbr for track in tracks], dtype=float)

        iou = box_iou_batch(tracks_boxes, detection_boxes)
        track2detection = np.argmax(iou, axis=1)

        for tracker_i, detect_i in enumerate(track2detection):
            if iou[tracker_i, detect_i] != 0:
                detects[detect_i].tracker_id = tracks[tracker_i].track_id
        return detects

    def _update_detected_colors(self, frame, detections, tracked_frames, tracked_colors):
        for detection in detections:
            if detection.class_name == "player" and detection.tracker_id != -1:
                box = detection.box(False)
                img_crop = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                img_crop_rgb = cv.cvtColor(img_crop, cv.COLOR_BGR2RGB)
                cv.imwrite("testing/%d_img.jpg" %(detection.tracker_id), img_crop)
                img_crop_rgb = img_crop_rgb.reshape(img_crop_rgb.shape[1]*img_crop_rgb.shape[0], 3)
                #print("img crop")
                #print(img_crop_rgb)
                kmeans = KMeans(n_clusters=3, n_init=10)
                s = kmeans.fit(img_crop_rgb)
                labels = kmeans.labels_
                labels = list(labels)
                centroids = kmeans.cluster_centers_
                percent=[]
                for i in range(len(centroids)):
                    j=labels.count(i)
                    j=j/(len(labels))
                    percent.append(j)
                percentages_and_centroids = list(zip(percent, centroids))
                percentages_and_centroids = sorted(reversed(percentages_and_centroids), reverse=True, key=lambda x: x[0])
                tracked_frames[detection.tracker_id] = tracked_frames[detection.tracker_id] + 1 if detection.tracker_id in tracked_frames else 1
                for i in range(len(centroids)):
                    for j in range(3):
                        if detection.tracker_id in tracked_colors:
                            tracked_colors[detection.tracker_id][i][j] += percentages_and_centroids[i][1][j]
                        else:
                            tracked_colors[detection.tracker_id][i][j] = percentages_and_centroids[i][1][j]
        return detections, tracked_frames, tracked_colors
