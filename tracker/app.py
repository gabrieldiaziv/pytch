from io import BytesIO
import tempfile
from typing import Optional
import zipfile
from dataclasses import asdict
import os
import uuid


from dotenv import load_dotenv
import jwt
import requests
from flask import Flask, flash, request, redirect, send_file
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
from werkzeug.datastructures import FileStorage
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from pydantic import BaseModel, ValidationError
from flask_pydantic import validate
from analytics.engine import Engine
from analytics.touches import touchesXY

from analytics.types import Frame, Header, Match, Team
from dotenv import load_dotenv
from store.db import PytchDB
from store.s3 import PytchStore

from track.annontate import COLORS, THICKNESS, BaseAnnotator, TextAnnotator
from track.track import Tracker
from track.utils import detects_to_frame
from track.video import VideoConfig
from track.localization import localization
from analytics.heatmap_with_background import heatmap

load_dotenv()  # load environment variables from .env file

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv'}
ALLOWED_EXTENSIONS = ALLOWED_VIDEO_EXTENSIONS | ALLOWED_IMAGE_EXTENSIONS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'super secret key'

model = Tracker(model_type='best.pt') 
engine = Engine(vizs=[
    heatmap(),
    touchesXY(x_range=(-53, -18), y_range=None),
    touchesXY(x_range=(-18, 18), y_range=None),
    touchesXY(x_range=(18, 53), y_range=None),
])
store = PytchStore()
db = PytchDB()


base_annontator = BaseAnnotator(colors=COLORS, thickness=THICKNESS)
text_annontator = TextAnnotator(background_color=(
    255, 255, 255), text_color=(0, 0, 0), text_thickness=2)


@app.before_request
def verify_id_token():
    # bypass verification for initial OPTIONS request
    if os.getenv("DEVELOPMENT", "false") == "true":
        return

    if request.method == 'OPTIONS':
        return None

#     print('verifying access token')

#     # get the access token from the Authorization header
#     auth_header = request.headers.get('Authorization', '')
#     if not auth_header:
#         return 'Authorization header expected', 401
#     id_token = auth_header.split()[1]

#     # decode the headers of the JWT
#     token_headers = jwt.get_unverified_header(id_token)
#     if token_headers['alg'] != 'RS256':
#         return 'Invalid token headers', 401

#     # fetch the JWKS from Auth0
#     jwks_url = os.environ.get('AUTH0_ISSUER', '') + '/.well-known/jwks.json'
#     jwks = requests.get(jwks_url).json()

#     # find the matching JWK
#     matched_jwk = next(
#         (jwk for jwk in jwks['keys'] if jwk['kid'] == token_headers['kid']), None)
#     if not matched_jwk or 'x5c' not in matched_jwk:
#         return 'No JWK found', 401

#     # get the certificate from the JWK
#     certificate = '-----BEGIN CERTIFICATE-----\n' + \
#         matched_jwk['x5c'][0] + '\n-----END CERTIFICATE-----'
#     public_key = load_pem_x509_certificate(
#         certificate.encode(), default_backend()).public_key()

#     # verify the JWT
#     try:
#         jwt.decode(
#             id_token,
#             public_key,
#             audience=os.environ.get('AUTH0_CLIENT_ID', ''),
#             issuer=os.environ.get('AUTH0_ISSUER', '') + '/',
#             algorithms=['RS256']
#         )
#     except jwt.InvalidTokenError as e:
#         return 'Invalid token: ' + str(e), 401

#     print('access token verified')



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def file_ext(filename: str) -> str:
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename: str) -> bool:
    return "." in filename and file_ext(filename) in ALLOWED_EXTENSIONS


class DetectParams(BaseModel):
    match_id: str
    team1: str
    team2: str

    class Config:
        fields = {
            'match_id': 'match_id',
            'team1' : 'team_1',
            'team2' : 'team_2'
        }


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
        flash(
            f"filetype not supported. Use one of the following {ALLOWED_EXTENSIONS}")
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

        _, upload_file = tempfile.mkstemp(
            suffix=f"{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(upload_file)

        _, label_vid = tempfile.mkstemp(suffix=f".mp4")
        _, twod_vid = tempfile.mkstemp(suffix=f".mp4")
        _, match_json = tempfile.mkstemp(suffix=f".json")
        _, thumbnail = tempfile.mkstemp(suffix=f".jpg")

        
        req: Optional[DetectParams] = DetectParams(match_id=str(uuid.uuid4()), team1='gabe', team2='ryan')
        ### TODO: REMOVE THE FOLLOWING LINE: 
        db.insert_match(req.match_id)
        # try:
        #     req = DetectParams(**request.get_json())
        # except ValidationError as e:
        #    return e.errors()

        label_writer = VideoConfig(
            fps=30,
            width=1920,
            height=1080,
        ).new_video(label_vid)

        twod_writer = VideoConfig(
            fps=30,
            width=1920,
            height=1080,
        ).new_video(twod_vid)

        match_writer = open(match_json, 'w')

        frames: list[Frame] = []

        i = 0

        output, teams, colors = model.detect_video(upload_file)

        for frame, detects, coords, extremities, line_names, line_points in output:
            label_img = frame.copy()
            h, w, _ = frame.shape

            label_img = base_annontator.annotate(label_img, detects)
            label_img = text_annontator.annotate(label_img, detects, coords)
            label_img = localization.show_lines(label_img, extremities)

            twod_img = localization.twod_img(
                h, w, coords, line_names, line_points)
            frames.append(detects_to_frame(i, detects, coords))

             
            if i == 0:
                cv2.imwrite(thumbnail, label_img)

            label_writer.write(label_img)
            twod_writer.write(twod_img)
            i += 1

        m = Match(
            header=Header(
                team1=Team(id=0, name=req.team1, color=colors[0]),
                team2=Team(id=1, name=req.team2, color=colors[1]),
                player_teams=teams
            ), match=frames)

        match_writer.write(m.to_json())

        match_writer.close()
        label_writer.release()
        twod_writer.release()

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(match_json)
            zipf.write(label_vid)
            zipf.write(twod_vid)
            zipf.write(thumbnail)

        # Set the file pointer to the beginning of the file
        memory_file.seek(0)

        urls = store.upload_data(
            req.match_id, 
            label_vid, twod_vid, match_json, thumbnail
        )

        db.update_match(
            req.match_id,
            urls.twod_url,
            urls.label_url,
            urls.match_url,
            urls.thumbnail_url,
        )

        vizs = engine.compute(m)
        for v in vizs:
            upload = store.upload_viz(
                req.match_id,
                v.name,
                v.path
            )

            db.insert_viz(
                req.match_id,
                v.name,
                v.desc,
                upload.viz_url
            )

        # Send the zip file as an attachment
        return send_file(memory_file, download_name='files.zip', as_attachment=True)

    return 'Invalid Request'
