import cv2
import numpy as np

def hsv_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, w, _ = hsv.shape

    hmin = int(h/2-50)
    hmax = int(h/2+50)
    wmin = int(w/2-50)
    wmax = int(w/2+50)

    middle = hsv[hmin:hmax,wmin:wmax]
    hue = []
    val = []
    mh, mw, _ = middle.shape
    for i in range(mh):
        for j in range(mw):
            hue.append(middle[i][j][0])
            val.append(middle[i][j][2])
    avg_hue = int(np.ceil(np.average(hue)))
    avg_val = int(np.ceil(np.average(val)))

    lower_bound = np.array([avg_hue-60, 0, avg_val-60])
    upper_bound = np.array([avg_hue+60, 255, avg_val+60])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(img,img,mask=mask)
    return res

def tophat(img):
    (B, G, R) = cv2.split(img)
 
    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Getting the kernel to be used in Top-Hat 
    filterSize =(3, 3) 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,  
                                    filterSize)

    # Applying the Top-Hat operation 
    top_b = cv2.morphologyEx(B,  
                                cv2.MORPH_TOPHAT, 
                                kernel)
    top_g = cv2.morphologyEx(G,  
                    cv2.MORPH_TOPHAT, 
                    kernel)
    top_r = cv2.morphologyEx(R,  
                    cv2.MORPH_TOPHAT, 
                    kernel)

    processed = gray

    h, w = processed.shape

    for i in range(h):
        for j in range(w):
            processed[i][j] = min(top_b[i][j], top_g[i][j], top_r[i][j])
    return processed

def lines(img, img_color):
    l = img
    # Apply edge detection method on the image
    edges = cv2.Canny(l, 50, 150, apertureSize=3)
    
    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
    
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
    
        # x0 stores the value rcos(theta)
        x0 = a*r
    
        # y0 stores the value rsin(theta)
        y0 = b*r
    
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
    
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
    
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
    
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
    
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv2.line(img_color, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img_color


image = cv2.imread('data/image.jpg')

res = hsv_mask(image)
th_nomask = tophat(image)
th_mask = tophat(res)
img_lines = lines(th_mask, image)

cv2.imshow("img", res)
cv2.imshow("nomask", th_nomask)
cv2.imshow("mask", th_mask)
cv2.imshow("lines", img_lines)
cv2.waitKey(60000) 