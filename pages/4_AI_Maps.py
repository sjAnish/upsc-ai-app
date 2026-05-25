import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium

# LOAD GLOBAL CSS
def load_css():

    with open(".streamlit/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )

load_css()

# PAGE CONFIG
st.set_page_config(
    page_title="AI Maps",
    page_icon="assets/ashoka_logo.jpg",
    layout="wide"
)

hide_streamlit_style = """

<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

</style>

"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

# TITLE
st.title("🗺️ UPSC AI Maps")

st.markdown("""
Interactive UPSC Geography Revision System
""")

# SIDEBAR
st.sidebar.header("🌍 Filters")

# DATASET SELECTOR
dataset = st.sidebar.selectbox(

    "Select Dataset",

    [
        "National Parks",
        "Ramsar Sites",
        "Tiger Reserves",
        "Rivers",
        "Mountains"
    ]
)

# LOAD DATASETS
if dataset == "National Parks":

    df = pd.read_csv(
        "data/national_parks.csv"
    )

    marker_color = "green"
    marker_icon = "tree"

elif dataset == "Ramsar Sites":

    df = pd.read_csv(
        "data/ramsar_sites.csv"
    )

    marker_color = "blue"
    marker_icon = "tint"

elif dataset == "Tiger Reserves":

    df = pd.read_csv(
        "data/tiger_reserves.csv"
    )

    marker_color = "orange"
    marker_icon = "paw"

elif dataset == "Rivers":

    df = pd.read_csv(
        "data/rivers.csv"
    )

    marker_color = "cadetblue"
    marker_icon = "water"

elif dataset == "Mountains":

    df = pd.read_csv(
        "data/mountains.csv"
    )

    marker_color = "red"
    marker_icon = "triangle-up"

# STATE FILTER
selected_state = st.sidebar.selectbox(

    "Select State",

    ["All"] + sorted(df["state"].unique())
)

# FILTER DATA
filtered_df = df.copy()

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["state"] == selected_state
    ]

# MAP
m = folium.Map(

    location=[22.5, 80.9],

    zoom_start=5,

    tiles="CartoDB positron"
)

# MARKERS
for _, row in filtered_df.iterrows():

    popup_text = f"""
    <div style="
    width:260px;
    padding:14px;
    font-family:Arial;
    ">

    <h3 style="
    margin-bottom:10px;
    color:#1e3a8a;
    ">
    📍 {row['name']}
    </h3>

    <p><b>📍 State:</b> {row['state']}</p>

    <p><b>⭐ Famous For:</b> {row['famous_for']}</p>

    <p><b>🌊 River:</b> {row['river']}</p>

    <p><b>📝 PYQ:</b> {row['pyq']}</p>

    <hr>

    <p style="font-size:13px;">
    <b>📚 My Notes:</b><br>
    {row['my_notes']}
    </p>

    </div>
    """

    folium.Marker(

        location=[
            row["latitude"],
            row["longitude"]
        ],

        popup=folium.Popup(
            popup_text,
            max_width=300
        ),

        tooltip=row["name"],

        icon=folium.Icon(
            color=marker_color,
            icon=marker_icon,
            prefix="fa"
        )

    ).add_to(m)

# DISPLAY MAP
st_folium(

    m,

    width="100%",

    height=700
)

# TABLE
st.subheader("📚 Location Database")

st.dataframe(

    filtered_df,

    use_container_width=True
)