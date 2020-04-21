import email
import io
import os

from PIL import Image, ImageFile

import boto3
from chalice import Chalice
from chalice.app import S3Event

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
S3_SOURCE_PREFIX = os.environ['S3_SOURCE_PREFIX']
S3_DESTINATION_PREFIX = os.environ['S3_DESTINATION_PREFIX']
PIXEL_RESIZE_TO = int(os.environ['PIXEL_RESIZE_TO'])
RESIZE_SCALE = PIXEL_RESIZE_TO, PIXEL_RESIZE_TO

ImageFile.LOAD_TRUNCATED_IMAGES = True


app = Chalice(app_name='emailImageResizer')
s3 = boto3.resource('s3')
s3_bucket = s3.Bucket(S3_BUCKET_NAME)


@app.on_s3_event(bucket=S3_BUCKET_NAME, prefix=S3_SOURCE_PREFIX)
def resize_image(event: S3Event) -> None:
    content = s3_bucket.Object(event.key).get()
    message = email.message_from_bytes(content['Body'].read())

    for m in message.get_payload():
        if not m.get_content_maintype() == 'image':
            continue

        src_image = io.BytesIO(m.get_payload(decode=True))
        dst_image = io.BytesIO()

        with Image.open(src_image) as img:
            img.thumbnail(RESIZE_SCALE)
            img.save(dst_image, format=img.format)

        s3_bucket.put_object(
            Key=f'{S3_DESTINATION_PREFIX}{m.get_filename()}',
            Body=dst_image.getvalue(),
            ContentType=m.get_content_type(),
        )
