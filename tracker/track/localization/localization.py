from . import detect_extremities
from . import baseline_cameras
from .camera import unproject_image_point
import cv2 as cv


# Call this at the start of analyzing a video
# Initializes the network to do the line detection
def init_segmentation_network(width, height):
    return detect_extremities.SegmentationNetwork(
        "resources/soccer_pitch_segmentation.pth",
        "resources/mean.npy",
        "resources/std.npy", width=width, height=height)

# Returns a list of pitch locations given a cv2 image, a list of image points to convert, and a SegmentationNetwork instance
def get_pitch_locations(frame, points, network):
    height, width, _ = frame.shape
    extremities = detect_extremities.analyze_frame(frame, network)
    success, homography = baseline_cameras.homography_from_extremities(extremities, width, height)
    img = baseline_cameras.draw_pitch_homography(frame, homography)
    cv.imshow("h", img)
    cv.waitKey(5000)
    return [unproject_image_point(homography, point) for point in points]


def main():
    frame = cv.imread("00000.jpg")
    h, w, _ = frame.shape
    network = init_segmentation_network(w, h)
    print(get_pitch_locations(frame, [(480, 270, 1)], network))

if __name__ == "__main__":
    main()


