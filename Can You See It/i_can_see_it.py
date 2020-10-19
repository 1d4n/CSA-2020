import cv2
import time

start_time = time.time()
cap = cv2.VideoCapture('can_you_see_it.mp4')
f = open("flag.txt", "w")

while cap.isOpened():
    print('working... please wait...')
    for i in range(1438):
        ret, frame = cap.read()
        if ret:
            pixel = str(frame[0, 0])
            is_white = int(pixel == '[250 253 251]')
            if pixel == '[95 98 96]':
                continue
            else:
                f.write(str(is_white))
        else:
            cap.release()
            break
    f.write('\n')

f.close()
finish_time = time.time()
print(finish_time - start_time, "seconds")  # ~ 40 secs
