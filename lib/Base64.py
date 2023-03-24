import base64
import re
from PIL import Image
from io import BytesIO
import numpy as np
import cv2


def url_to_img(url):
    result=re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", url, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        img = result.groupdict().get("data")
        img=base64.b64decode(img)
        return img,ext
    return 'Not Found'


def path_to_base64(img_path):
    with open(img_path, 'rb') as f:
        img = f.read()
        base64_str = base64.b64encode(img)  # base64编码
    return str(base64_str, 'utf-8')
    
