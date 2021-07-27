import streamlit as st
import pydeck as pdk
from forecast import forecast_AQI, coords_df
import numpy as np
import pandas as pd

ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"


icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}
locations = coords_df()

#@st.cache
#def cache_wrapper(region): return forecast_AQI(region)

locations["icon_data"] = None
for i in locations.index:
    locations["icon_data"][i] = icon_data



view_state = pdk.data_utils.compute_view(locations[["longitude", "latitude"]], 0.1)


icon_layer = pdk.Layer(
    type="IconLayer",
    data=locations,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["longitude", "latitude"],
    pickable=True,
)

st.write(pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{region}"}))
