import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 5
font_thickness = 8

def get_center(img, text):
    text_size = cv2.getTextSize(text, font, font_size, font_thickness)[0]

    return int(img.shape[1] - text_size[0]) // 2, int(img.shape[0] + text_size[1]) // 2

def make_box(aqi):
    base_dir = 'src/frontend/box-templates/'

    if (aqi <= 50):
       img = cv2.imread(base_dir + 'good.png')
    elif (aqi >= 51) and (aqi <= 100):
        img = cv2.imread(base_dir + 'moderate.png')
    elif (aqi >= 101) and (aqi <= 150):
        img = cv2.imread(base_dir + 'unhealthy_orange.png')
    elif (aqi >= 151) and (aqi <= 200):
        img = cv2.imread(base_dir + 'unhealthy_red.png')
    else:
        img = cv2.imread(base_dir + 'very_unhealthy.png')
    
    x, y = get_center(img, str(aqi))
    cv2.putText(img, str(aqi), (x, y + 40), font, font_size, (0, 0, 0), font_thickness)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)