import cv2
import numpy as np
img = cv2.imread('data/image.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, w, _ = hsv.shape

hmin = int(h/2-50)
hmax = int(h/2+50)
wmin = int(w/2-50)
wmax = int(w/2+50)

middle = hsv[hmin:hmax,wmin:wmax]
hue = []
sat = []
val = []
mh, mw, _ = middle.shape
for i in range(mh):
    for j in range(mw):
        hue.append(middle[i][j][0])
        sat.append(middle[i][j][1])
        val.append(middle[i][j][2])
avg_hue = int(np.ceil(np.average(hue)))
avg_sat = int(np.ceil(np.average(sat)))
avg_val = int(np.ceil(np.average(val)))

lower_bound = np.array([avg_hue-60, 0, avg_val-60])
upper_bound = np.array([avg_hue+60, 255, avg_val+60])
mask = cv2.inRange(hsv, lower_bound, upper_bound)
res = cv2.bitwise_and(img,img,mask=mask)
cv2.imshow("res", res)
cv2.waitKey(20000) 