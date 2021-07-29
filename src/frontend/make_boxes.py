import numpy as np
import cv2

size = (512,512,3)

colors = [
    (1,228,1),
    (0, 255, 255),
    (0, 127, 255),
    (0, 0, 255),
    (76, 1, 153)
]

def draw(aqi):
    img = np.zeros(size, np.uint8)

    if (aqi <= 50):
        c = colors[0]
    elif (aqi >= 51) and (aqi <= 100):
        c = colors[1] 
    elif (aqi >= 101) and (aqi <= 150):
        c = colors[2] 
    elif (aqi >= 151) and (aqi <= 200):
        c = colors[3] 
    elif (aqi >= 201):
        c = colors[4] 

    cv2.rectangle(img, (0, 0), size[:2], c, 10000)

    return img

cv2.imshow('mat', draw(78))
cv2.waitKey(0)