import cv2 as cv
import json

# Small script to show detected and classified lines in the original image

img = cv.imread("../datasets/calibration-2023/challenge/00000.jpg")
file = open("../predictions/challenge/extremities_00000.json")
data = json.load(file)

h, w, _ = img.shape
print(h, w)

for key in data:
    print(data[key])
    line = data[key]
    print(key)
    print((int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])))
    img = cv.line(img, (int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])), (0,0,255), 2)
    img = cv.putText(img, key, (int(w*line[0]["x"]), int(h*(line[0]["y"]))), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv.LINE_AA)
cv.imshow("Lines", img)
cv.waitKey(30000)
