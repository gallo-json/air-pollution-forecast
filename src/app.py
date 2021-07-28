import streamlit as st
import pydeck as pdk
import numpy as np
import pandas as pd

import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )

def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

if not _RELEASE:
    st.subheader("Leaflet - return coords on click")
    clicked_coords = my_component()
    if type(clicked_coords) is int:
        print(clicked_coords)
    else:
        print(clicked_coords['lat'], clicked_coords['lng'])
