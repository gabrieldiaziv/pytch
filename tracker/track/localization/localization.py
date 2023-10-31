import detect_extremities
import baseline_cameras
from camera import unproject_image_point


# Call this at the start of analyzing a video
# Initializes the network to do the line detection
def init_segmentation_network():
    return detect_extremities.SegmentationNetwork(
        "resources/soccer_pitch_segmentation.pth",
        "resources/mean.npy",
        "resources/std.npy")

# Returns a list of pitch locations given a cv2 image, a list of image points to convert, and a SegmentationNetwork instance
def get_pitch_locations(frame, points, network):
    height, width, _ = frame.shape
    extremities = detect_extremities.analyze_frame(frame, network)
    _, homography = baseline_cameras.homography_from_extremities(extremities, width, height)
    return [unproject_image_point(homography, point) for point in points]

