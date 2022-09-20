import os
import datetime
import time

import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np


with open('./whitelist.txt', 'r') as f:
    authorized_users = [l[:-1] for l in f.readlines() if len(l) > 2]
    f.close()

log_path = './log.txt'

cap = cv2.VideoCapture(2)

most_recent_access = {}

time_between_logs_th = 5

while True:

    ret, frame = cap.read()

    qr_info = decode(frame)

    if len(qr_info) > 0:

        qr = qr_info[0]

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        if data.decode() in authorized_users:
            cv2.putText(frame, 'ACCESS GRANTED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            if data.decode() not in most_recent_access.keys() \
                    or time.time() - most_recent_access[data.decode()] > time_between_logs_th:
                most_recent_access[data.decode()] = time.time()
                with open(log_path, 'a') as f:
                    f.write('{},{}\n'.format(data.decode(), datetime.datetime.now()))
                    f.close()

        else:
            cv2.putText(frame, 'ACCESS DENIED', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                            (0, 255, 0), 5)

        frame = cv2.polylines(frame, [np.array(polygon)], True, (255, 0, 0), 5)

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
