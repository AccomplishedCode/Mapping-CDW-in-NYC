import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

#Setting page to wide config mode
st.set_page_config(layout='wide')
st.title('Mapping Construction & Demolition Waste Flows in NYC')

#Loading the data
#data_dir= None #Input own directory if needed
datafile= 'trips_v2.csv'

year_chosen = st.sidebar.selectbox(
        'Please select year of interest:',
        (2019, 2020)
    )

material_chosen= st.sidebar.selectbox(
    'Please choose the material of interest:',
    ('Concrete','Masonry','Aspahlt and Road Material', 'Sand', 'Bulk Metal (from C&D Debris)','Construction & Demolition (C&D) Debris','Soil','Fill','RCA','Scrap Metal','General C&D Debris') #to be updated
)

direction_chosen= st.sidebar.selectbox(
    'Which transfer facility flow would you like to visualize?',
    ('Incoming', 'Outgoing', 'Both')
)
map_check= st.sidebar.checkbox('Do you want to see the map?')

#@st.cache
def load_data(file_path):
    data= pd.read_csv(file_path)
    return data

#Text element to let users know that the data is loading
data_load_state= st.text('Loading data...')

#Load the data
df= load_data(datafile)

temp_df= df.drop(columns=['Facility_ID','Destiny'], axis=1)
temp_df= temp_df.dropna()

temp_df.reset_index(drop=True)

if st.checkbox('Show Raw Data'):
    st.subheader('An overview of the dataframe we are working with')

    st.write(temp_df)

MAPBOX_API_KEY= 'pk.eyJ1IjoiYWNjb21wbGlzaGVkY29kZSIsImEiOiJja3B1ODNhYWMwMmNwMm90NWJtdThra3IwIn0.uEQt7PISQS8Ek91YuSzPNg'
st.subheader('Map of Incoming Construction & Demolition Waste to Transfer Facilities')

#Define map function 
view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=10, bearing=15, pitch=0, controller=True)


GREEN_RGB = [0, 255, 0, 90]
RED_RGB = [255, 100, 0, 80]
BLUE_RGB= [0, 146, 255, 100]
VIOLET_RGB= [220, 0, 255, 90]

def map(dataframe):
    

    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=temp_df,
            get_width="Tonnage/10000",
            get_source_position=["SA_lng", "SA_lat"],
            get_target_position=["f_lng", "f_lat"],
            get_tilt=15,
            width_min_pixels= 5,
            get_source_color=RED_RGB,
            get_target_color=BLUE_RGB,
            pickable=True,
            opacity=0.9,
            auto_highlight=True,
        ),
    ],
    tooltip= {
        "text":"Material : {Material}\n Coming from :{SA_address}\n Going to:{facility_name}\n Weight in tons: {Tonnage}\n Destiny: {Destiny}"
    }
))

def dual_map(dataframe_in, dataframe_out):
    st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
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
            get_source_color=RED_RGB,
            get_target_color=BLUE_RGB,
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
            get_source_color=VIOLET_RGB,
            get_target_color=GREEN_RGB,
            pickable=True,
            opacity=0.9,
            auto_highlight=True,
        ),
    ],
    tooltip= {
        "text":"Material : {Material}\n Coming from :{SA_address}\n Going to:{facility_name}\n Weight in tons: {Tonnage}\n Destiny: {Destiny}"
    }
))





def filter_data(dataframe, year, material):
    df1= dataframe.loc[dataframe['Year']==year]
    df1= df1.loc[df1['Material']==material]
    df_in= df1.loc[df1['Direction']=='Incoming']
    df_out= df1.loc[df1['Direction']=='Outgoing']

    return df_in, df_out


if map_check:
    #st.write(temp_df.columns)
    st.write(temp_df.isnull().sum())
    df_in, df_out= filter_data(temp_df, year_chosen, material_chosen)
    if direction_chosen=='Incoming':
        map(df_in)
    elif direction_chosen=='Outgoing':
        map(df_out)
    else:
        dual_map(df_in, df_out)
   
