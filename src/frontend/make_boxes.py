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

font = cv2.FONT_HERSHEY_SIMPLEX

def get_center(text, font_size, font_thickness):
    text_size = cv2.getTextSize(text, font, font_size, font_thickness)[0]

    return int(size[1] - text_size[0]) // 2, int(size[0] + text_size[1]) // 2

def draw(aqi):
    img = np.zeros(size, np.uint8)

    if (aqi <= 50):
        cv2.rectangle(img, (0, 0), size[:2], colors[0], 10000)

        text = [
            # (text, font_size, font_thickness, y_pos from center)
            ("GOOD", 4, 5, -200),
            ("AQI", 2, 5, -100),
            (str(aqi), 4, 5, 0),
            ("Air quality is satisfactory.", 2, 2, 100),
            ("It is safe to go outside.", 2, 2, 200)
        ]

        for t in text:
            x, y = get_center(t[0], t[1], t[2])
            cv2.putText(img, t[0], (x, y + t[3]), font, t[1], (0, 0, 0), t[2])
    elif (aqi >= 51) and (aqi <= 100):
        cv2.rectangle(img, (0, 0), size[:2], colors[1], 10000)
    elif (aqi >= 101) and (aqi <= 150):
        cv2.rectangle(img, (0, 0), size[:2], colors[2], 10000)
    elif (aqi >= 151) and (aqi <= 200):
        cv2.rectangle(img, (0, 0), size[:2], colors[3], 10000)
    else:
        cv2.rectangle(img, (0, 0), size[:2], colors[4], 10000)

    return img


cv2.imshow('mat', draw(8))
cv2.waitKey(0)