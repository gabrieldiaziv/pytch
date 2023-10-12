r"""°°°
## Setup
°°°"""
# |%%--%%| <NAE6zt1vmF|KBTVEfs8SK>

!nvidia-smi

# |%%--%%| <KBTVEfs8SK|Z5aC8RNeJ7>

import os
HOME = os.getcwd()
print(HOME)

# |%%--%%| <Z5aC8RNeJ7|YX0XazLQTR>

from dotenv import load_dotenv
import os


load_dotenv()

print(os.environ['KAGGLE_USERNAME'])
print(os.environ['KAGGLE_KEY'])

# |%%--%%| <YX0XazLQTR|OxkZiBXzbI>

!./.venv/bin/kaggle competitions files -c dfl-bundesliga-data-shootout | \
grep clips | head -20 | \
awk '{print $1}' | \
while read -l line; \
    ./.venv/bin/kaggle competitions download -c dfl-bundesliga-data-shootout -f $line; unzip $(string split '/' $line)[-1] -d clips; rm $(string split '/' $line)[-1].zip; \
end

# |%%--%%| <OxkZiBXzbI|x1TfashHUh>
r"""°°°
# Install YOLOv5
°°°"""
# |%%--%%| <x1TfashHUh|7vNH5vc2zf>

!git clone https://github.com/ultralytics/yolov5
%cd {HOME}/yolov5
%pip install -r requirements.txt

import torch
import utils
display = utils.notebook_init()

# |%%--%%| <7vNH5vc2zf|TgGiBJbHOv>
r"""°°°
## Use Pre Trained COCO model
°°°"""
# |%%--%%| <TgGiBJbHOv|oMGhmOz9uw>

%cd {HOME}
!activate
!./.venv/bin/python yolov5/detect.py --weights yolov5/yolov5x.pt --img 640 --conf 0.25 --source "clips/08fd33_4.mp4" --name coco

# |%%--%%| <oMGhmOz9uw|OaEE8prKQ2>
r"""°°°
## Using custom model
°°°"""
# |%%--%%| <OaEE8prKQ2|f508OcAI2z>

%cd {HOME}
!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OYwrlRti4cieuvVr8ERaJhTQdFJXWT4I' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1OYwrlRti4cieuvVr8ERaJhTQdFJXWT4I" -O best.pt && rm -rf /tmp/cookies.txt

#|%%--%%| <f508OcAI2z|e593EWwR81>

WEIGHTS_PATH = f"{HOME}/best.pt"

# |%%--%%| <e593EWwR81|VIVBuVTRCb>

%cd {HOME}
!./.venv/bin/python yolov5/detect.py --weights {HOME}/best.pt --img 1280 --conf 0.25 --source ./clips/08fd33_4.mp4 --name custom

#|%%--%%| <VIVBuVTRCb|7o4chGdUdN>

from typing import Generator

import matplotlib.pyplot as plt
import numpy as np

import cv2

%matplotlib inline 


def generate_frames(video_file: str) -> Generator[np.ndarray, None, None]:
    video = cv2.VideoCapture(video_file)

    while video.isOpened():
        success, frame = video.read()

        if not success:
            break

        yield frame

    video.release()


def plot_image(image: np.ndarray, size: int = 12) -> None:
    plt.figure(figsize=(size, size))
    plt.imshow(image[...,::-1])
    plt.show()

#|%%--%%| <7o4chGdUdN|evN0YiAuaR>

SOURCE_VIDEO_PATH = f"{HOME}/clips/08fd33_4.mp4"
frame_iterator = iter(generate_frames(video_file=SOURCE_VIDEO_PATH))

#|%%--%%| <evN0YiAuaR|ooytFHPerl>

frame = next(frame_iterator)
plot_image(frame, 16)

#|%%--%%| <ooytFHPerl|9OkfLbVkIt>


import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', WEIGHTS_PATH, device=0)
     
#|%%--%%| <9OkfLbVkIt|5nftx5vg4E>

results = model(frame, size=1280)

#|%%--%%| <5nftx5vg4E|NHly2Iir0L>

results.pandas()

#|%%--%%| <NHly2Iir0L|AguUU0YJRe>

results.pred[0]

#|%%--%%| <AguUU0YJRe|cPvIzN0Y9w>

model.names

# |%%--%%| <cPvIzN0Y9w|Qm0d16Vadb>


