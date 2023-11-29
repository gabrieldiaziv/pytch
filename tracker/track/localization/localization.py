from . import detect_extremities
from . import baseline_cameras
from .camera import unproject_image_point
import cv2 as cv
import numpy as np
import time
from .soccerpitch import SoccerPitch

PITCH = SoccerPitch()
# Call this at the start of analyzing a video
# Initializes the network to do the line detection
def init_segmentation_network(width, height):
    return detect_extremities.SegmentationNetwork(
        "resources/soccer_pitch_segmentation.pth",
        "resources/mean.npy",
        "resources/std.npy", width=width, height=height)

def get_homography(frame, network):
    height, width, _ = frame.shape
    extremities = detect_extremities.analyze_frame(frame, network)
    success, homography, line_names, line_points = baseline_cameras.homography_from_extremities(extremities, width, height)
    if not success:
        return None
    inv_homography = np.linalg.inv(homography)
    return inv_homography, extremities, line_names, line_points


# Returns a list of pitch locations given a cv2 image, a list of image points to convert, and a SegmentationNetwork instance
def get_pitch_locations(points, inv_homography, test=False):
    localized_points = [unproject_image_point(inv_homography, point) for point in points]
    # if test:
        # img_viz = np.full((height, width, 3), 255, dtype=np.uint8)
        # img_homography = baseline_cameras.draw_pitch_homography(frame, homography)
        #img_viz = baseline_cameras.draw_detected_pitch_lines(img_viz, line_points, line_names, pitch)
        #cv.imshow("Detected Lines", img_lines)
        #cv.imshow("Homography", img_homography)
        #cv.imshow("Field Visualization", img_viz)
    return localized_points

def twod_img( height, width, localized_points,line_names, line_points):
    img = np.full((height, width, 3), 255, dtype=np.uint8)

    img = baseline_cameras.draw_detected_pitch_lines(img, line_points, line_names, PITCH)
    for localized_point in localized_points:
        x_image = PITCH.x_to_image(width, localized_point[0])
        y_image = PITCH.y_to_image(height, localized_point[1])
        if (x_image < 0 or x_image > width) or (y_image < 0 or y_image > height):
            print("Couldn't draw localized point: Out of bounds")
        else:
            img = cv.circle(img, (PITCH.x_to_image(width, localized_point[0]), PITCH.y_to_image(height, localized_point[1])), 6, (0, 255, 0), 6)
    return img

# Returns the image with the detected lines drawn and labeled
def show_lines(img, extremities):
    h, w, _ = img.shape

    for key in extremities:
        line = extremities[key]
        print((int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])))
        img = cv.line(img, (int(w*line[0]["x"]), int(h*line[0]["y"])), (int(w*line[1]["x"]), int(h*line[1]["y"])), (0,0,255), 2)
        img = cv.putText(img, key, (int(w*line[0]["x"]), int(h*(line[0]["y"]))), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv.LINE_AA)
    return img


def main():
    frame = cv.imread("output_010.jpg")
    h, w, _ = frame.shape
    network = init_segmentation_network(w, h)
    print(get_pitch_locations(frame, [(480, 270, 1)], network, test=True))

if __name__ == "__main__":
    main()


