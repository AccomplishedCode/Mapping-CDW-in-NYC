import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

#Setting page to wide config mode
st.set_page_config(layout='wide')
st.title('Mapping Construction+Demolition Waste Flows for Recovered C+DW Use in NYC’s Capital Program')
st.write("Welcome! This is a tool created by a team of MS students at NYU Center for Urban Sciences & Progress to visualize CDW Waste in NYC. The dataset used for these visualizations was extracted from handwritten forms provided by NYS DEP, and converted into machine readable format by the team over a period of 3 months.")
st.write("The dataset used is easily explored through the sidepane. For now, we have two views, tabular and map based. Please choose the checkbox for your usage.")
st.write("And it's that simple! Are you ready to see this data in action?")


def first_decision():
    sidebar_chosen= st.checkbox("Yes!")
    desc_chosen= st.checkbox("Not yet, I want to learn more about this project.")
    return sidebar_chosen,desc_chosen

s_chosen, desc_chosen= first_decision()
data_dir= 'data/' #Input own directory if needed
#Loading the data
datafile= 'cleaned_transfers.csv'
df= pd.read_csv(data_dir + datafile)

#Defining filter functions and map functions

def filter_data(dataframe, year, material):
    df1= dataframe.loc[dataframe['Year']==year]
    df1= df1.loc[df1['Material']==material]
    df_in= df1.loc[df1['Direction']=='Incoming']
    df_out= df1.loc[df1['Direction']=='Outgoing']

    return df_in, df_out

#Defining mapping functions, for individual directions & both incoming and outgoing directions
#First, we define colors for our arcs

GREEN_RGB = [0, 255, 0, 90]
RED_RGB = [255, 100, 0, 80]
BLUE_RGB= [0, 146, 255, 100]
VIOLET_RGB= [220, 0, 255, 90]

#We also need to define the initial viewstate for our map, to set the camera position when the user first sees the map
view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=7, bearing=15, pitch=45, controller=True)

#Now onto the map functions 
# Using pydeck integration here to easily visualize our arcs from origin to destination 
    
def map(dataframe):
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


#Defining sidebar panel
if s_chosen:
    st.sidebar.subheader('Which CDW dataset would you like to explore?')
    data_chosen= st.sidebar.checkbox('Transfer Facilities')
    if data_chosen:
        st.sidebar.subheader("How would you like to explore the  dataset?")
        tab_view= st.sidebar.checkbox('Tabular View') #Defining views for the page to display
        map_view= st.sidebar.checkbox('Map View')
        county_view= st.sidebar.checkbox('County Level Statistics (Coming soon, in progress!') #Exploratory dataframe analysis to be implemented

        if tab_view:
                st.subheader('Dataframe of the Transfer facilities dataset')
                st.write(df) #Currently Transfer Facilities but will change when Landfill data is added.

        if map_view:
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
            st.subheader('Map of Incoming Construction & Demolition Waste to Transfer Facilities')
            st.write("This map if fully interactive. You can zoom in and out, pan by holding the right mouse click and get information about each trip by hovering over the arc.")
            df_in, df_out= filter_data(df, year_chosen, material_chosen)
            if direction_chosen=='Incoming':
                map(df_in)
            elif direction_chosen=='Outgoing':
                map(df_out)
            elif direction_chosen=='Both':
                dual_map(df_in, df_out)

if desc_chosen:
    st.write("Thanks for clicking to learn more about our project. We believe that reuse of materials in the construction industry is critical in reducing Greenhouse Gas Emmissions, and it's important that there exist a secondary marketplace for recovered CDW materials. ")
    st.write("To read our Capstone Project Presentation, please click on the link below:")
    st.write("https://nyu0-my.sharepoint.com/:w:/g/personal/dw2759_nyu_edu/EQCu4Irca2JEozzEmqMOl5cBdDZYhJOxWSFROycdTdQR1Q?rtime=55Ubf7tH2Ug", unsafe_allow_html=True)














