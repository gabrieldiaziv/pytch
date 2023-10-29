from io import BytesIO

from flask import Flask, flash, request, redirect, send_file
from PIL import Image
import cv2
import numpy as np

from track.annontate import COLORS, BaseAnnotator
from track.track import Tracker

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)

model = Tracker()
annotr = BaseAnnotator(colors=COLORS,thickness=3)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash(f"filetype not supported. Use one of the following {ALLOWED_EXTENSIONS}")
        return redirect(request.url)

    img_bytes = file.read()
    img = np.fromstring(img_bytes, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    detections = model.detect_image(img)
    label_img = annotr.annotate(img, detections)
    
    image = Image.fromarray(label_img)
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the image as a response
    return send_file(img_io, mimetype='image/png')

