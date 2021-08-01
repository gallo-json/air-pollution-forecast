from PIL import Image, ImageDraw, ImageFont

size = (512,512)

colors = [
    (1,228,1),
    (255, 255, 0),
    (255, 127, 0),
    (255, 0, 0),
    (153, 1, 76)
]


def make_box(aqi):

    if (aqi <= 50):
        img = Image.new(mode='RGB', size=size, color=colors[0])
        draw = ImageDraw.Draw(img)

        text = [
            # (text, font_size, y_pos from center)
            ("GOOD", 20, -200),
            ("AQI", 20, -100),
            (str(aqi), 20, 0),
            ("Air quality is satisfactory.", 20, 100),
            ("It is safe to go outside.", 20, 200)
        ]
    elif (aqi >= 51) and (aqi <= 100):
        img = Image.new(mode='RGB', size=size, color=colors[1])
        draw = ImageDraw.Draw(img)

        text = [
            # (text, font_size, y_pos from center)
            ("GOOD", 20, -200),
            ("AQI", 20, -100),
            (str(aqi), 20, 0),
            ("Air quality is satisfactory.", 20, 100),
            ("It is safe to go outside.", 20, 200)
        ]
    elif (aqi >= 101) and (aqi <= 150):
        img = Image.new(mode='RGB', size=size, color=colors[2])
        draw = ImageDraw.Draw(img)

        text = [
            # (text, font_size, y_pos from center)
            ("GOOD", 20, -200),
            ("AQI", 20, -100),
            (str(aqi), 20, 0),
            ("Air quality is satisfactory.", 20, 100),
            ("It is safe to go outside.", 20, 200)
        ]

    elif (aqi >= 151) and (aqi <= 200):
        img = Image.new(mode='RGB', size=size, color=colors[3])
        draw = ImageDraw.Draw(img)

        text = [
            # (text, font_size, y_pos from center)
            ("GOOD", 20, -200),
            ("AQI", 20, -100),
            (str(aqi), 20, 0),
            ("Air quality is satisfactory.", 20, 100),
            ("It is safe to go outside.", 20, 200)
        ]

    else:
        img = Image.new(mode='RGB', size=size, color=colors[4])
        draw = ImageDraw.Draw(img)

        text = [
            # (text, font_size, y_pos from center)
            ("GOOD", 20, -200),
            ("AQI", 20, -100),
            (str(aqi), 20, 0),
            ("Air quality is satisfactory.", 20, 100),
            ("It is safe to go outside.", 20, 200)
        ]

    for t in text:
        font = ImageFont.truetype('src/frontend/Comfortaa-Regular.ttf', t[1])
        x, y = draw.textsize(t[0], font=font)
        draw.text(((size[0] - x) / 2, (size[1] - y) / 2  + t[2]), t[0], fill='black', font=font)

    return img