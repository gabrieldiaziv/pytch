import sys
import logging
import os
import boto3
from dataclasses import dataclass
from mypy_boto3_s3.client import S3Client


AWS_ACCESS_KEY  = 'AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'AWS_SECRET_KEY'
AWS_BUCKET = 'AWS_BUCKET'

@dataclass
class UploadResult:
    label_url: str
    twod_url: str
    match_url: str
    thumbnail_url: str

@dataclass
class VizResult:
    viz_url: str

class PytchStore:
    def __init__(self):
        access_key = os.getenv(AWS_ACCESS_KEY)
        secret_key = os.getenv(AWS_SECRET_KEY)
        bucket = os.getenv(AWS_BUCKET)
        if access_key and secret_key and bucket:
            self.client : S3Client = boto3.client('s3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            self.bucket = bucket
        else:
            logging.fatal("aws s3 keys are not set")
            sys.exit(1)

    def _upload(self, file_path: str, obj: str):
            self.client.upload_file(
               file_path, self.bucket, obj
            )


            return self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': obj},
                ExpiresIn=31536000
            )

    def upload_data(self, match_id: str, label_video_path:str, twod_video_path:str, match_json_path: str, thumbnail_path: str):
        return UploadResult(
            thumbnail_url=self._upload(thumbnail_path, f'{match_id}-thumbnail.png'),
            label_url=self._upload(label_video_path, f'{match_id}-label.mp4'),
            twod_url=self._upload(twod_video_path, f'{match_id}-2d.mp4' ),
            match_url=self._upload(match_json_path, f'{match_id}-data.json'),
        )

    def upload_viz(self, match_id: str, viz_type: str, viz_path: str):
        return VizResult(
            viz_url=self._upload(viz_path, f'{match_id}-{viz_type}.html')
        )



            
            




        


        


