from io import BytesIO
import tempfile

from flask import Flask, flash, request, redirect, send_file
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
from werkzeug.datastructures import FileStorage

from track.annontate import COLORS, THICKNESS, BaseAnnotator, TextAnnotator
from track.track import Tracker
from track.video import VideoConfig

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv'}
ALLOWED_EXTENSIONS =  ALLOWED_VIDEO_EXTENSIONS | ALLOWED_IMAGE_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
CORS(app)

model = Tracker(model_type='best.pt')

base_annontator = BaseAnnotator(colors=COLORS, thickness=THICKNESS)
text_annontator = TextAnnotator(background_color=(255, 255, 255), text_color=(0, 0, 0), text_thickness=2)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def file_ext(filename: str) -> str:
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename: str) -> bool:
    return "." in filename and file_ext(filename) in ALLOWED_EXTENSIONS


@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        return detect_post()
    if request.method == "GET":
        return detect_get()

    flash("invalid method")
    return redirect(request.url)


def detect_get():
    return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        """


def detect_post():
    if "file" not in request.files:
        flash("No selected file")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename is None or file.filename == "":
        flash("No selected file")
        print('no file')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash(f"filetype not supported. Use one of the following {ALLOWED_EXTENSIONS}")
        print('file not supported')
        return redirect(request.url)

    if file_ext(file.filename) in ALLOWED_IMAGE_EXTENSIONS:
        print("PROCCESSING IMAGE")
        img_bytes = file.read()
        img = np.fromstring(img_bytes, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        detections = model.detect_image(img)
        label_img = base_annontator.annotate(img, detections)
        
        image = Image.fromarray(label_img)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')

    if file_ext(file.filename) in ALLOWED_VIDEO_EXTENSIONS:
        _, upload_file = tempfile.mkstemp(suffix=f"{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(upload_file)

        _, output_file = tempfile.mkstemp(suffix=f".mp4")
        
        video_writer = VideoConfig(
            fps=30,
            width=1920,
            height=1080,
        ).new_video(output_file)

        for frame, detects, _ in model.detect_video(upload_file):
            label_img = frame.copy()
            label_img = base_annontator.annotate(label_img, detects)
            label_img = text_annontator.annotate(label_img, detects)
            
            video_writer.write(label_img)

        video_writer.release()
        return send_file(output_file, as_attachment=True)

    return 'Invalid Request'

            

        
        

