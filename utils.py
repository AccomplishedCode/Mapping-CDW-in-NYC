import pandas as pd
import plotly.express as px
import math
import plotly.graph_objs as go


material_list = ['Concrete', 'Masonry', 'Asphalt and Road Material', 'Sand', 'Soil', 'Yard Waste', 'General C&D Debris', 'Fill', 'Wood', 'Metals', 
                 'Old Corrugated Containers', 'Rock, Stone, and Gravel','Asphalt Roofing Shingles', 'Residue', 'Gypsum','Tires', 'Asphalt Roofing Shingles',
                 'Auto Fluff','Asbestos', 'Ash & Cement Alternatives',]

region_list = [1,2,3,4,5,6,7,8,9]

df_monthly= pd.read_csv('data/monthly_CDW.csv')

def timeline_2020(df,mat_list, regions):
  df = df[df.Year == 2020][df.Material.isin(mat_list)][df.Region.isin(regions)]\
                                  [['Material','Region','January (tons)', 'February (tons)', 'March (tons)', 'April (tons)', 'May (tons)', 'June (tons)',
                                    'July (tons)', 'August (tons)', 'September (tons)', 'October (tons)', 'November (tons)', 'December (tons)']]\
                                    .groupby(['Material']).sum().drop(columns=['Region']).reset_index()
  df = pd.melt(df,id_vars='Material',value_vars=list(df.columns[1:]), var_name='Months', value_name='Total Quantities')
  fig = px.bar(df, x="Months", y="Total Quantities", color='Material')
  #fig.show()
  return fig
  
def label_(df):
  destiny_range = list(range(1,len(df.Destiny.unique())+1))
  destiny_list = list(df.Destiny.unique())
  destiny_dict = dict(zip(destiny_range, destiny_list))
  df['label'] = ''
  for i in df.index:
    for key in destiny_dict:
      if df['Destiny'][i] in (destiny_dict[key]):
        df['label'][i] = key
  return(df)

def label_regional(df,type_):
  incoming_range = list(range(len(df[df.Direction=='Incoming']['SA Region'].unique())))
  incoming_list = list(df[df.Direction=='Incoming']['SA Region'].unique())
  incoming_dict = dict(zip(incoming_range,incoming_list))
  facility_region_label = max(incoming_range)+1

  if type_ == 'Transfer Facility':
    direction_ = ['Outgoing']
  else:
    direction_ = ['Outgoing','Not Applicable']
  outgoing_range = list(range(facility_region_label+1,len(df[df.Direction in direction_]['SA Region'].unique())))
  outgoing_list = list(df[df.Direction in direction_]['SA Region'].unique())
  outgoing_dict = dict(zip(outgoing_range,outgoing_list))

  destiny_range = list(range(max(outgoing_range)+1,len(df[df.Direction in direction_]['Destiny'].unique())))
  destiny_list = list(df[df.Direction in direction_]['Destiny'].unique())
  destiny_dict = dict(zip(destiny_range,destiny_list))

  df['label'] = ''
  df['label_2'] = ''
  for i in df.index:
    if df['Direction'][i] == 'Incoming':
      df['label'][i] = incoming_dict[df['SA Region'][i]].key()
    else:
      df['label'][i] = outgoing_dict[df['SA Region'][i]].key()
      df['label_2'][i] = destiny_dict[df['Destiny'][i]].key()
  return(df)

def sankey_destiny(df, region, year, type_):

  if type_ == 'Transfer Facility':
    direction_ = ['Outgoing']
  else:
    direction_ = ['Outgoing','Not Applicable']
  df = df[df['Facility Type']==type_]
  df = df[df.Year == year][df.Direction.isin(direction_)][df['Facility Region'] == region]\
                          [['Material','Facility Region','Amount/tons','Destiny']].groupby(['Facility Region','Material','Destiny']).sum().reset_index()\
                          .drop(columns = ['Facility Region'])

  list_mats= ['Concrete', 'Masonry', 'Asphalt and Road Material', 'Sand', 'Soil', 'Yard Waste', 'General C&D Debris', 'Fill', 'Wood', 'Metals',
              'Old Corrugated Containers', 'Rock, Stone, and Gravel','Asphalt Roofing Shingles', 'Residue', 'Gypsum','Tires', 'Asphalt Roofing Shingles',
              'Auto Fluff','Asbestos', 'Ash & Cement Alternatives', 'Other']
  colors_links= ['#E59866', '#BA4A00', '#9B59B6','#8E44AD', '#2980B9','#3498DB', '#BDC3C7', '#45B39D','#52BE80', '#008080','#0000FF', '#000080', '#FF00FF',
                '#800080', '#9FE2BF', '#6495ED','#CCCCFF', '#FFBF00','#FF7F50', '#F39C12', '#884EA0']

  df = label_(df)

  color_dict=dict(zip(list_mats, colors_links))
  x= pd.DataFrame(list(color_dict.items()), columns=['Material', 'Color'])
  df_colored= df.merge(x, on="Material", how="left")

  fig = go.Figure(data=[go.Sankey(
      node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ['Region '+str(region)]+list((df.Destiny.unique())),
        color = "light grey"
      ),
      link = dict(
        source = list(map(int,(list(('0'*len(df)))))), 
        target = list(df.label),
        value = [float(i) for i in list(df['Amount/tons'])],
        color=list(df_colored.Color),
        label= list(df.Material.unique())
    ))])

  fig.update_layout(title_text="Region "+str(region)+ " C+DW Flows", font_size=10)
  #fig.show()
  #print(df.drop(columns=['label']))
  return fig

def sankey_destiny_2(df, region, year, type_):

  if type_ == 'Transfer Facility':
    direction_ = ['Outgoing']
  else:
    direction_ = ['Outgoing','Not Applicable']
  df = df[df['Facility Type']==type_]
  df = df[df.Year == year][df.Direction.isin(direction_)][df['facility_region'] == region]\
                          [['Material','facility_region','Tonnage','Destiny']].groupby(['facility_region','Material','Destiny']).sum().reset_index()\
                          .drop(columns = ['facility_region'])

  list_mats= ['Concrete', 'Masonry', 'Asphalt and Road Material', 'Sand', 'Soil', 'Yard Waste', 'General C&D Debris', 'Fill', 'Wood', 'Metals',
              'Old Corrugated Containers', 'Rock, Stone, and Gravel','Asphalt Roofing Shingles', 'Residue', 'Gypsum','Tires', 'Asphalt Roofing Shingles',
              'Auto Fluff','Asbestos', 'Ash & Cement Alternatives', 'Other']
  colors_links= ['#E59866', '#BA4A00', '#9B59B6','#8E44AD', '#2980B9','#3498DB', '#BDC3C7', '#45B39D','#52BE80', '#008080','#0000FF', '#000080', '#FF00FF',
                '#800080', '#9FE2BF', '#6495ED','#CCCCFF', '#FFBF00','#FF7F50', '#F39C12', '#884EA0']

  df = label_(df)

  color_dict=dict(zip(list_mats, colors_links))
  x= pd.DataFrame(list(color_dict.items()), columns=['Material', 'Color'])
  df_colored= df.merge(x, on="Material", how="left")

  fig = go.Figure(data=[go.Sankey(
      node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ['Region '+str(region)]+list((df.Destiny.unique())),
        color = "light grey"
      ),
      link = dict(
        source = list(map(int,(list(('0'*len(df)))))), 
        target = list(df.label),
        value = [float(i) for i in list(df['Tonnage'])],
        color=list(df_colored.Color),
        label= list(df.Material.unique())
    ))])

  fig.update_layout(title_text="Region "+str(region)+ " C+DW Flows", font_size=10)
  #fig.show()
  #print(df.drop(columns=['label']))
  return fig