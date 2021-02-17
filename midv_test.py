import os
import sys
import timeit

from PIL import Image
import numpy as np
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image

from midv500models.pre_trained_models import create_model


start = timeit.default_timer()

model = create_model('Unet_resnet34_2020-05-19')
model.eval()

image = load_rgb(sys.argv[1])
# im = Image.fromarray(image)
# im.save()

transform = albu.Compose([albu.Normalize(p=1)], p=1)
padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
x = transform(image=padded_image)['image']
x = torch.unsqueeze(tensor_from_rgb_image(x), 0)

with torch.no_grad():
    prediction = model(x)[0][0]

mask = (prediction > 0).cpu().numpy().astype(np.uint8)
mask = unpad(mask, pads)
# im = Image.fromarray(mask)
# im.save()

dst = cv2.addWeighted(image, 1, (cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * (0, 255, 0)).astype(np.uint8), 0.5, 0)
# im = Image.fromarray(dst)
# im.save()

combinedImages = (np.hstack([image, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * 255, dst]))
im = Image.fromarray(combinedImages)
im.save('all_' + os.path.basename(sys.argv[1]))

stop = timeit.default_timer()
print('Time: ', stop - start)
