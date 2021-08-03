import streamlit as st
import pydeck as pdk


#Defining mapping functions, for individual directions & both incoming and outgoing directions
#First, we define colors for our arcs

GREEN_RGB = [204, 245, 175]
DARK_GREEN_RGB =[4, 118, 52]
GREY_RGB= [128,128,128]
RED_RGB= [250, 0, 41]
COPPER_RGB=[238, 97, 35]

#Now onto the map functions 
# Using pydeck integration here to easily visualize our arcs from origin to destination 
#We also need to define the initial viewstate for our map, to set the camera position when the user first sees the map
view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=8, bearing=15, pitch=45, controller=True)

def map(dataframe, color):
    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=dataframe,
            get_width="Tonnage/10000",
            get_source_position=["SA_lng", "SA_lat"],
            get_target_position=["f_lng", "f_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=color,
            get_target_color=color,
            pickable=True,
            opacity=0.6,
            auto_highlight=True,
        ), 
    ],
    tooltip= {
        "text":"Material : {Material}\n Coming from :{SA_address}\n Going to:{facility_name}\n Weight in tons: {Tonnage}\n Destiny: {Destiny}"
    }
))

def map_landfill(dataframe):
    df_incoming= dataframe.loc[dataframe['Direction']=='Incoming']
    df_outgoing= dataframe.loc[dataframe['Direction']=='Outgoing']
    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=df_outgoing,
            get_width="Tonnage/10000",
            get_source_position=["f_lng", "f_lat"],
            get_target_position=["SA_lng", "SA_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=RED_RGB,
            get_target_color=RED_RGB,
            pickable=True,
            opacity=0.7,
            auto_highlight=True,
        ),
        pdk.Layer(
            "ArcLayer",
            data=df_incoming,
            get_width="Tonnage/10000",
            get_source_position=["SA_lng", "SA_lat"],
            get_target_position=["f_lng", "f_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=GREY_RGB,
            get_target_color=GREY_RGB,
            pickable=True,
            opacity=0.5,
            auto_highlight=True,
        ),
    ],
    tooltip= {
        "text":"Material : {Material}\n Coming from :{SA_address}\n Going to:{facility_name}\n Weight in tons: {Tonnage}\n Destiny: {Destiny}"
    }
))

def dual_map(dataframe_in, dataframe_out, color_1, color_2):
    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=dataframe_in,
            get_width="Tonnage/10000",
            get_source_position=["SA_lng", "SA_lat"],
            get_target_position=["f_lng", "f_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=color_1,
            get_target_color=color_1,
            pickable=True,
            opacity=0.9,
            auto_highlight=True,
        ),
        pdk.Layer(
            "ArcLayer",
            data=dataframe_out,
            get_width="Tonnage/10000",
            get_source_position=["SA_lng", "SA_lat"],
            get_target_position=["f_lng", "f_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=color_2,
            get_target_color=color_2,
            pickable=True,
            opacity=0.9,
            auto_highlight=True,
        ),
    ],
    tooltip= {
        "text":"Material : {Material}\n Coming from :{SA_address}\n Going to:{facility_name}\n Weight in tons: {Tonnage}\n Destiny: {Destiny}"
    }
))

view_state_2= pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=6, bearing=15, pitch=45, controller=True)
def column_map(dataframe):
    df_columns= dataframe.loc[dataframe['Direction']=='Not Applicable']
    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=view_state_2,
    layers=[
        pdk.Layer(
            "ColumnLayer",
            data=df_columns,
            get_position= ['f_lng, f_lat'],
            pickable=True,
            opacity=0.9,
            auto_highlight=True,
            get_elevation="Tonnage",
            get_fill_color= RED_RGB,
            elevation_scale= 100, 
            radius=2000
        ),
    ],
    tooltip= {
        "text": "{Tonnage} tons of {Material} coming from :{SA_address}\n Used locally at {facility_name} as: {Destiny}"
    }
))
