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

    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 4
    font_thickness = 2

    if (aqi <= 50):
        c = colors[0]
        text = [
            "GOOD",
            "Air quality is satisfactory.",
            "It is safe to go outside."
        ]
    elif (aqi >= 51) and (aqi <= 100):
        c = colors[1] 
        text = [
            "MODERATE",
            "No restrictions for general public.",
            "It is safe to go outside."
        ]
    elif (aqi >= 101) and (aqi <= 150):
        c = colors[2] 
        text = [
            "UNHEALTHY FOR SENSITIVE GROUPS",
            "Sensitive groups may experience health effects.",
            "General public may not be affected."
        ]
    elif (aqi >= 151) and (aqi <= 200):
        c = colors[3] 
        text = [
            "UNHEALTHY",
            "Anyone may experience health effects.",
            "It is NOT safe for the general public to go outside."
        ]
    else:
        c = colors[4] 
        text = [
            "VERY UNHEALTHY",
            "Anyone may experience more serious health effects.",
            "It is NOT safe for the general public to go outside."
        ]

    cv2.rectangle(img, (0, 0), size[:2], c, 10000)

    text_sizes = []

    for t in text:
        text_size = cv2.getTextSize(t, font, font_scale, font_thickness)[0]

        text_sizes.append([int(img.shape[1] - text_size[0]) // 2, int(img.shape[0] + text_size[1]) // 2])
    
    cv2.putText(img, header, (header_x, header_y), font, font_scale, (0,0,0), font_thickness)

    return img

cv2.imshow('mat', draw(78))
cv2.waitKey(0)
