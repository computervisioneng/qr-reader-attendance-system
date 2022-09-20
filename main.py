import os

import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np


input_dir = '/home/phillip/Desktop/todays_tutorial/10_qr_code_reader/code/data'

for j in sorted(os.listdir(input_dir)):
    img = cv2.imread(os.path.join(input_dir, j))

    qr_info = decode(img)

    for qr in qr_info:

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        print(data)
        print(rect)
        print(polygon)

        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                            (0, 255, 0), 5)

        img = cv2.polylines(img, [np.array(polygon)], True, (255, 0, 0), 5)

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()