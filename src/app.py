import streamlit as st
import pydeck as pdk
from forecast import load_data
from pandas import DataFrame

forecasts = load_data()

def map():
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": 29,
            "longitude": -95,
            "zoom": 50,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=forecasts,
                get_position=["longitude", "latitude"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

map()