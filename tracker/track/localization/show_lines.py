import cv2 as cv
import json

# Small script to show detected and classified lines in the original image

import detect_extremities
import baseline_cameras
import localization

img = cv.imread("04040.jpg")
h, w, _ = img.shape
network = localization.init_segmentation_network(w, h)
data = detect_extremities.analyze_frame(img, network)

h, w, _ = img.shape

for key in data:
    print(data[key])
    line = data[key]
    print(key)
    print((int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])))
    img = cv.line(img, (int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])), (0,0,255), 2)
    img = cv.putText(img, key, (int(w*line[0]["x"]), int(h*(line[0]["y"]))), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv.LINE_AA)
cv.imshow("Lines", img)
cv.waitKey(30000)
