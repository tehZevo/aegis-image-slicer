import os
import cv2
import numpy as np
from protopost import ProtoPost

from utils import b64_to_img, img_to_b64

PORT = int(os.getenv("PORT", 80))

#assumes boxes are in pixel coordinates (TODO: allow for 0..1-ranged coords too?)
def do_slice(data):
  img = data["image"]
  boxes = data["boxes"]
  #load image from base 64
  img = b64_to_img(img)
  ih, iw = img.shape[0:2]

  slices = []
  for x, y, w, h in boxes:
    #convert to x/y
    x1, y1, x2, y2 = [x, y, x+w, y+h]
    #check bounds
    x1, x2 = np.clip([x1, x2], 0, iw)
    y1, y2 = np.clip([y1, y2], 0, ih)
    #crop
    slices.append(img[y1:y2, x1:x2])

  #b64 encode each
  slices = [img_to_b64(s) for s in slices]

  return slices

routes = {
  "": do_slice
}

ProtoPost(routes).start(PORT)
