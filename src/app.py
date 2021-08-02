from forecast import coords_df, forecast_AQI
from frontend.make_boxes import make_box

import streamlit as st
from scipy.spatial import KDTree
from datetime import datetime
import streamlit.components.v1 as components

date_now = datetime.now()

_component_func = components.declare_component(
    "my_component",
    url="http://localhost:3001",
)

def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

st.title("Houston 3 Day Air Quality Forecast")
st.header("Please select the area closest to your location")

clicked_coords = my_component()

if type(clicked_coords) is dict:
    tree = KDTree(coords_df[['latitude', 'longitude']].values)
    idx = int(tree.query([clicked_coords['lat'], clicked_coords['lng']])[1])

    selected_region = coords_df['region'].iloc[idx].replace('/', '-')
    preds = forecast_AQI(selected_region)

    st.header("Three day forecast for " + selected_region)

    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.header(date_now.strftime("%a") + ' ' + date_now.strftime("%b") + ' ' + str(int(date_now.strftime("%d"))))
        st.image(make_box(preds[0]))

    with col2:
        st.header(date_now.strftime("%a") + ' ' + date_now.strftime("%b") + ' ' + str(int(date_now.strftime("%d")) + 1))
        st.image(make_box(preds[1]))

    with col3:
        st.header(date_now.strftime("%a") + ' ' + date_now.strftime("%b") + ' ' + str(int(date_now.strftime("%d")) + 2))
        st.image(make_box(preds[2]))