import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import base64 
from maps import *
from utils import *
from annotated_text import annotated_text

#Loading some dataset for beta expander
categories= pd.read_csv('data/categories.csv')
regions= pd.read_csv('data/regions.csv')

#Setting page to wide config mode
st.set_page_config(layout='wide')
st.title('Mapping Construction+Demolition Waste Flows for Recovered C+DW Use in NYC’s Capital Program')
st.write("Welcome! This is a tool created by a team of MS students at NYU Center for Urban Sciences & Progress to visualize CDW Waste in NYC. The dataset used for these visualizations was extracted from handwritten forms provided by NYS DEP, and converted into machine readable format by the team over a period of 3 months.")
st.write("The dataset used is easily explored through the sidepane.Please choose the desired view checkbox to display the visualization, and uncheck to clear the view.")
def first_decision():
    sidebar_chosen= st.checkbox("Yes!")
    desc_chosen= st.checkbox("Not yet, I want to learn more about this project.")
    return sidebar_chosen,desc_chosen

s_chosen, desc_chosen= first_decision()

#Selecting whether or not to display sidebar config controls


data_dir= 'data/' #Input own directory if needed
#Loading the data
datafile= 'dataset_snake_v2.csv'
df= pd.read_csv(data_dir + datafile)
df= df.drop(columns=['Unnamed: 0'], axis=1)

df_capacities= pd.read_csv('data/LF_caps.csv')
#Separating into Transfers and Landfills

df_transfers= df.loc[df['Facility Type']=='Transfer Facility']
df_landfills= df.loc[df['Facility Type']=='Landfill']

#Defining filter functions and map functions
def filter_data(dataframe, year, material):
    df1= dataframe.loc[dataframe['Year']==year]
    df1= df1.loc[df1['Material']==material]
    df_in= df1.loc[df1['Direction']=='Incoming']
    df_out= df1.loc[df1['Direction']=='Outgoing']

    return df_in, df_out


#Defining sidebar panel
if s_chosen:
    st.sidebar.subheader('Please check the box on the dataset you wish to visualize')
    data_chosen= st.sidebar.radio('We currently provide exploration of only one type', ['Transfer Facility', 'Landfills'])
        
    if data_chosen:

        st.sidebar.subheader('How would you like to explore the dataset?')

        tab_view= st.sidebar.checkbox('Tabular View') #Defining views for the page to display
        map_view= st.sidebar.checkbox('Map View') #Bool variable for Mapping view
        stat_view= st.sidebar.checkbox('Statistical Visualizations') #Exploratory dataframe analysis to be implemented

        st.sidebar.subheader('Please choose year of interest')
        year_chosen = st.sidebar.radio(
                    'Please select year of interest:',
                    (2019, 2020))
        if tab_view:
            #Allow data downloading
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings
            linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download Dataset file</a>'
            st.markdown(linko, unsafe_allow_html=True)

            csv_monthly= df_monthly.to_csv(index=False)
            b64 = base64.b64encode(csv_monthly.encode()).decode()  # some strings
            linko_monthly= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download Monthly Breakdown file</a>'
            st.markdown(linko_monthly, unsafe_allow_html=True)

            
            csv_capacities= df_capacities.to_csv(index=False)
            b64 = base64.b64encode(csv_capacities.encode()).decode()  # some strings
            linko_capacities= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download Remaining Landfill Capacities file</a>'
            st.markdown(linko_capacities, unsafe_allow_html=True)


            if data_chosen=='Transfer Facility':
                st.subheader('Dataframe of the Transfer facilities dataset')
                st.write(df_transfers)


            if data_chosen=='Landfills':
                st.subheader('Dataframe of the Landfills dataset')
                st.write(df_landfills)


        if map_view:

            direction_chosen= st.sidebar.selectbox(
                'Please choose the type of CDW flows to visualize:',
                ('Incoming', 'Outgoing', 'Both')
            )
            

            st.write("This map is fully interactive. You can zoom in and out, pan by holding the right mouse click and get information about each trip by hovering over the arc.")


            if data_chosen=='Transfer Facility':
                st.subheader('Map of Incoming Construction & Demolition Waste to Transfer Facilities')
                annotated_text(
                    "Legend:",
                    ("Incoming", "To Transfer Facility", "#ee6123"),
                    ("Outgoing", "From Transfer Facility", "#047634" )
                )
                material_chosen= st.sidebar.selectbox(
                    'Please choose the material of interest:',
                    (df_transfers['Material'].unique()))
                
                df_in, df_out= filter_data(df_transfers, year_chosen, material_chosen)

                if direction_chosen=='Incoming':
                    map(df_in,COPPER_RGB)
                elif direction_chosen=='Outgoing':
                    map(df_out, DARK_GREEN_RGB)
                elif direction_chosen=='Both':
                    dual_map(df_in, df_out, COPPER_RGB, DARK_GREEN_RGB)

            elif data_chosen=='Landfills':
                st.subheader('Map of Incoming Construction & Demolition Waste to Landfills')
                annotated_text(
                    "Legend:",
                    ("Incoming",),
                    ("RECYCLED","FROM LANDFILL", "#f50029" )
                )
                material_chosen= st.sidebar.selectbox(
                'Please choose the material of interest:',
                (df_landfills['Material'].dropna().unique()))

                df_landfill_filtered= df_landfills.loc[df_landfills['Material']==material_chosen]
                map_landfill(df_landfill_filtered)
                st.subheader("Map of Materials reused onsite Landfills")
                column_map(df_landfill_filtered)

        if stat_view:

            st.sidebar.subheader('We provide two different visualizations for this data')
            st.sidebar.write('Please choose the graph types below: ')

            monthly= st.sidebar.checkbox('Monthly CDW breakdown')
            sankey= st.sidebar.checkbox('Regional Material Flows')

            if monthly:
                if data_chosen: 
                    st.subheader('Monthly Breakdown of CDW')
                    st.write('The graph is fully interactive, please feel free to select/deselect relevant materials')
                    st.plotly_chart(timeline_2020(df_monthly, material_list, region_list, year_chosen),  use_container_width=True)
                    if year_chosen==2020:
                        st.subheader('Monthly Breakdown of Other Waste')
                        st.write('Please check disclaimer section for all materials included under the category: Other')
                        st.plotly_chart(timeline_2020(df_monthly,['Other'], region_list, year_chosen), use_container_width=True)

            if sankey:
                if data_chosen=='Transfer Facility':
                    region_chosen= st.sidebar.selectbox('Please choose the region of interest:', [1,2,8])
                    st.subheader('Regional Flow Graph of CDW For Transfer Facilities')
                    st.plotly_chart(sankey_destiny_2(df_transfers, region_chosen,year_chosen,data_chosen ),  use_container_width=True)   
                else:
                    region_chosen= st.sidebar.selectbox('Please choose the region of interest:', (df_landfills['facility_region'].unique()))
                    st.subheader('Regional Flow Graph of CDW For Landfills')
                    st.plotly_chart(sankey_destiny_2(df_landfills, region_chosen,2020,'Landfill' ),  use_container_width=True)
                
        
if desc_chosen:
    st.subheader(" A Bit About This Project")
    st.write("Thanks for clicking to learn more about our project! We believe that reuse of materials in the construction industry is critical in reducing Greenhouse Gas Emmissions, and it's important that there exist a way to track and map these material flows in order to create a market for secondary use. ")
    st.write("To read more about our Capstone Project and check out the code, please click on the link below:")
    st.write("https://github.com/AccomplishedCode/Mapping-CDW-in-NYC", unsafe_allow_html=True)

#Expander for disclaimers
st.subheader("A Few Pointers About the Data and the Maps")
with st.beta_expander("See important disclaimers about our maps and data"):
    st.write(
        """
        - This data has been aggregated by humans from handwritten, scanned PDF forms. 
        - The coordinate locations for transfer facilities and landfills were extracted using a mix of Google Maps API as well as other open source API's. Due to facility names being fluid due to change of ownership/new registrations, we've confirmed that the names listed on this dataset are the latest available as of April, 2021.
        - We rely on the level of spatial granularity that is provided in the reporting forms. In the cases where the “Service Area” refers to a state or county, our map portrays that where the respective end of the arc falls at the center of the town/county as per the NYS Municipal boundary map. In some cases (in and around Suffolk County, for example) that center could coincidentally lie in water. Please note the “Coming from/Going to” details as you hover over the arcs. 
        - This tool is just a visualization of the data we were able to gather. This does not aim to inculpate or put blame on any particular facility or region for their activities.  
        - The following table defines the final 21 material types by categorizing the numerous different types of reported materials: 
        """
    )
    st.dataframe(categories)
    st.write("""
        - The following table shows the available data in terms of facility type, region and year: 
        """)
    st.dataframe(regions)
    st.image('data/regions.jpg')
    st.write("Thank you for using our webapp! We really hope you liked it! Feel free to check out the dark theme if you'd like, it should automatically turn on if your system already has it. If not, you can change it in the settings on the top right! :-)")











