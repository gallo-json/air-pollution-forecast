import streamlit as st
from scipy.spatial import KDTree
from datetime import datetime
from forecast import coords_df, find_region, forecast_AQI

import streamlit.components.v1 as components

date_now = datetime.now()

_component_func = components.declare_component(
    "my_component",
    url="http://localhost:3001",
)

def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

st.header("Houston 3 Day Air Quality Forecast")
st.subheader("Click on your area in Houston")

clicked_coords = my_component()

if type(clicked_coords) is dict:
    tree = KDTree(coords_df[['latitude', 'longitude']].values)
    idx = int(tree.query([clicked_coords['lat'], clicked_coords['lng']])[1])
    preds = forecast_AQI(coords_df['region'].iloc[idx])

    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.header(date_now.strftime("%b") + ' ' + date_now.strftime("%d"))

    with col2:
        st.header(date_now.strftime("%b") + ' ' + str(int(date_now.strftime("%d")) + 1))

    with col3:
        st.header(date_now.strftime("%b") + ' ' + str(int(date_now.strftime("%d")) + 2))
