import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from streamlit_lottie import st_lottie


PROJ_ROOT = os.path.join(os.pardir)


@st.cache
def get_choroplethmap_data():
    long_data_path=os.path.join(PROJ_ROOT, "data", "processed", "streamlit_data_choroplethmap.csv")
    return pd.read_csv(long_data_path)

@st.cache
def get_scatterplot_data():
    long_data_path=os.path.join(PROJ_ROOT, "data", "processed", "streamlit_data_scatterplot.csv")
    return pd.read_csv(long_data_path)

@st.cache
def get_linechart_data():
    main_data_path=os.path.join(PROJ_ROOT, "data", "processed", "streamlit_data_linechart.csv")
    data=pd.read_csv(main_data_path,dtype='string', index_col='Unnamed: 0')
    data.index=pd.to_datetime(data.index)
    data.index=data.index.strftime('%b-%Y')
    data=data.astype(float)
    return data

@st.cache
def get_cities_data():
    cities_path=os.path.join(PROJ_ROOT, "data", "processed", "Canadian_cities_info.csv")
    return pd.read_csv(cities_path,dtype='string', index_col='Unnamed: 0')

@st.cache
def get_map_data():
    provinces_geojson=os.path.join(PROJ_ROOT, "data", "external", "Canada_Provinces_Geojson", "canada_provinces.geojson")
    with open(provinces_geojson, "r") as geo:
        map = json.load(geo)
    map['features'][5]['properties']['name']='Québec'
    return map

def get_lottie_gifs():
    fuel_pump_gif=os.path.join(PROJ_ROOT, "data", "external", "fuel_pump.json")
    with open(fuel_pump_gif, "r") as pump:
        fuel_pump = json.load(pump)
    return fuel_pump



map_data=get_map_data()
cities_data=get_cities_data()
choropleth_data= get_choroplethmap_data()
scatterplot_data= get_scatterplot_data()
linechart_data= get_linechart_data()



def calculate_max_and_min_values_from_long_data(data_long):
    """
    Returns the rounded formats for the max and min of the data in cents

    """
    max_cents=round(data_long['cents'].max())+10
    min_cents=round(data_long['cents'].min())-10

    return(max_cents, min_cents)

lottie_fuelpump=get_lottie_gifs()
st_lottie(lottie_fuelpump, speed=1, height=200, key="initial")



st.title("Canadian Gas Prices 🍁.....through the Years")
st.markdown("This application is a Streamlit dashboard that can be used to explore historical trends in Canadian gas"
            " prices. There are a few plot types highlighted that can be used to find various unique insigts "
            "for each city and province through the years. All data was retrieved from [Stats Canada](https://www.statcan.gc.ca/en/subjects-start/population_and_demography)."
            " In this analysis, I go through the pros and cons of each chart type highlighting each plot type's strengths"
            "and weaknesses. Each chart has been created using the [Plotly API](https://plotly.com/python-api-reference/).  Plotly allows the user to create dynamic interactive"
            " plots which can be used to gain deeper insights (I was not paid to say that and I have no affiliation with plotly at all...).  I especially liked using "
            " their API because of their animation feature. It proves to be very handy when exploring time series data."
            " Below each chart you can view the data used to create it."
            "\n"
            "*All monetary values are in CAD and have been adjusted to their present day dollar value (real dollars)"
            )
            
st.markdown('***')
###############################################################################################################
####################################################LINE CHART#################################################
###############################################################################################################
st.subheader('Linechart')
################################################################################################################
fig = go.Figure()

for _index, _abbrev in cities_data['Abbreviation'].items():
    
    fig.add_trace(
        go.Scatter(x=pd.to_datetime(linechart_data.index), 
                   y=linechart_data[_index], 
                   name=_abbrev,
                   hovertemplate="Month: %{x}<br>" +
                                 "Cents per Litre: %{y:.1f}"))

fig.update_layout(title_text="Canadian Monthly Gas Prices (1990-Present)")

date_buttons = [
{'count': 1, 'label': '1 Month', 'step': "month", 'stepmode': "backward"},
{'count': 6, 'label': '6 Months', 'step': "month", 'stepmode': "backward"},
{'count': 1, 'label': '1 Year', 'step': "year", 'stepmode': "backward"},
{'count': 5, 'label': '5 Years', 'step': "year", 'stepmode': "backward"},
{'count': 10, 'label': '10 Years', 'step': "year", 'stepmode': "backward"},
{'count': 20, 'label': '20 Years', 'step': "year", 'stepmode': "backward"},
{'label':'All Years','step':'all'}]


# Add range slider
fig.update_layout(
    width=1000,
    height=600,
    xaxis=dict(rangeselector=dict(buttons=date_buttons, buttondefaults=date_buttons[3]),
               rangeslider=dict(visible=True),
               type="date"))


fig.update_xaxes(
        title_text = "Year",
        title_font = {"size": 20},
        title_standoff = 25)

fig.update_yaxes(
        title_text = "Cents per Litre",
        title_font = {"size": 20},
        title_standoff = 5)

st.write(fig)
######################################################################################################################
if st.checkbox("Show Linechart Data", False):
    st.subheader('Linechart Data')
    st.write(linechart_data)
#######################################################################################################################
st.markdown(
    "**Data Details:** The data has been aggregated by city, and each province (except Nunavut) has atleast one city represented"
    " in the data.  Data is presented in wide format inorder to provide the index as a trace for each line."
            )
st.markdown(
    "**Pros:** Useful for representing and gaining intuition on continuous data, especially as change over time"
    "Estimates can be made as to the direction that the data is heading. Comparisons can be made between items "
    "to glean insights on relationships."
            )
st.markdown(
    "**Cons:** Alot is going on... too many lines, that have values that are too similar, can make comparing data difficult "
            )
st.markdown(
    "**Insights:** Generally, all cities seem to follow a similar trend. "
    "There are a few obvious dips in price, perhaps the most apparent can be explained by the 2008 Financial Crisis"
    "and the recent COVID-19 pandemic. Generally, prices have showed an increasing trend over the past few decades."
    "Main questions I  would ask looking at the data from this perspective are: "
            )
st.markdown("* What are the seasonal trends for increases and decreases in price?")
st.markdown("* Is there a time of year when it is ideal to do more driving?")
st.markdown("* How far into the future and with what accuracy can we predict the price of gas?")
########################################################################################################################




st.markdown('***')
###############################################################################################################
############################################_CHOROPLETH MAP_###################################################
###############################################################################################################

st.subheader('Choropleth Map')
################################################################################################################
MAX_CENTS, MIN_CENTS= calculate_max_and_min_values_from_long_data(choropleth_data)
# Create choropleth map
fig = px.choropleth(choropleth_data,
                    locations='province',
                    geojson=map_data,
                    featureidkey="properties.name",
                    color='cents',
                    projection="mercator",
                    animation_frame="Year",
                    animation_group="Year",
                    scope='north america',
                    title='Canadian Yearly Gas Prices (1990-Present)',
                    color_continuous_scale='YlOrRd',
                    range_color=[MIN_CENTS, MAX_CENTS],
                    labels={'cents' : 'Cents per Litre'},
                    hover_name='province',
                    hover_data={
                        'Year'  : True,
                        'cents' : ':.1f',
                        'province' : False,
                    },
                    height=1000,
                    width=1000,
                    locationmode='geojson-id',
                    )

# Adjust map layout stylings
fig.update_layout(dict(
    geo=dict(bgcolor='#FEFFFE', 
            showlakes=False,
            lakecolor='#73BFDC'),
    # margin={"r":0,"t":0,"l":0,"b":0},
                ))

# Adjust map geo options
fig.update_geos(showcountries=False, showcoastlines=False,
                showland=False, fitbounds="geojson",
                subunitcolor='white')
st.write(fig)
##############################################################################################################
if st.checkbox("Show Choropleth Map Data", False):
    st.subheader('Choropleth Map Data')
    st.write(choropleth_data)
########################################################################################################################
st.markdown(
    "**Data Details:** The data has been aggregated by the yearly mean for each province. Unfortunately, there"
    "was no data available for Nunavut. Rather than just leaving it at zero and skewing the colorbar's range,"
    " I decided to drop it altogether from the map.... sorry Nunavut"
            )
st.markdown(
    "**Pros:** Visually effective - can see a large amount of information and general patterns "
            )
st.markdown(
    "**Cons:** Since the choropleth map uses the mean price to represent defined provinces and territories, the viewer can not "
    "gain detailed information or perspective on any of the area's internal conditions."
    "Also, the gradient between colours is not distict enough to be able"
    "to adequately distingish differences in magnitude. "
            )
st.markdown(
    "**Insights:** The Yukon and Northwest Territories seem to constantly experience a greater relative "
    "to the other provinces. I would presume that generally, prices in the territories reach higher levels because of the transportation costs involved" 
    " This perspecitve of the data raises questions about what effects geography play on price."
            )
st.markdown("* How strongly does a city's longitude or latidue correlate with it's fuel price?")
st.markdown("* Does the distance between a city and an oil refinery play a roll in how much people in the city will pay?")
st.markdown("* Does the number of refineries in a province play a roll in the amount people in the province pay?")
########################################################################################################################



st.markdown('***')
################################################################################################################
##################################################_SCATTERPLOT_#################################################
################################################################################################################
st.subheader('Scatterplot')
################################################################################################################
MAX_CENTS, MIN_CENTS= calculate_max_and_min_values_from_long_data(scatterplot_data)

unique_colours=['darkslategray',
                'saddlebrown',
                'forestgreen',
                'navy',
                'red',
                'gold',
                'chartreuse',
                'aqua',
                'fuchsia',
                'dodgerblue',
                'rebeccapurple',
                'hotpink']

fig =px.scatter(scatterplot_data, 
                           x="cents",
                           y="population", 
                           color="province",
                           animation_frame="Year", 
                           animation_group="city",
                           size="vehicles", 
                           size_max=150,
                           range_x=[MIN_CENTS,MAX_CENTS],
                           log_y=True,
                           color_discrete_sequence=unique_colours,
                           labels={'cents' : 'Cents per Litre',
                                   'population' : 'City Population',
                                   'vehicles': 'Estimated Vehicles',
                                   'province': 'Province'},
                           hover_name="city",
                           hover_data={ 'cents' : ':.1f', 
                                        'population': True,
                                        'vehicles': True,
                                        'province' : False,
                                        'Year':False
                                        },
                           height=1200,
                           width=1000,
                           title='Canadian Yearly Gas Prices (1990-Present)',
                           )

fig.update_xaxes(title_font_size=22,
                    tickfont_size=15)       

fig.update_yaxes(title_font_size=22,
                    tickfont_size=20)

fig.update_layout(legend=dict(font=dict(size=15,
                                        color='black')))

fig.update_traces(hovertemplate= "<b>%{hovertext}</b><br>" + 
                                 "Cents per Litre: %{x:.1f}<br>" +
                                 "City Population: %{y}<br>" +
                                 "Estimated Vehicles: %{marker.size}")                    

st.write(fig) 
###############################################################################################################
if st.checkbox("Show Scatterplot Data", False):
    st.subheader('Scatterplot Data')
    st.write(scatterplot_data)
########################################################################################################################
st.markdown(
    "**Data Details:** The data has been subsected by the yearly mean for each city. City population data for each year"
    " was also added from [Stats Canada](https://www.statcan.gc.ca/en/subjects-start/population_and_demography). From the"
    " popluation, I also created a new data point 'Estimated number of Vehicles' which is simpy half the population size."
            )
st.markdown(
    "**Pros:** They can show large quantities of data and make it easy to see correlations between variables and clustering effects."
    "As a quick overview and analytical tool, scatterplots are invaluable and work with almost any continuous scale data."
    "It's quite simple to distinguish differences between maxima and minima."        
            )
st.markdown(
    "**Cons:** It can be confusing to track all the variables being dsiplayed and it's easy to get lost in"
    " what is going on with each marker. Also, the differences population magnitudes are quite apparent in the data. To account, "
    "for the large variances in scale, a log axis was used.  "
            )
st.markdown(
    "**Insights:** The addition of city population metric initally made me ask questions about price differences between "
    " cities within a province."
            )
st.markdown("* How does the price of gas deviate in large cities comapred to smaller ones?")
st.markdown("* If the deviation is large enough, will I save more money fueling up at a small town just outside the city?")
st.markdown("* With increaseing options of non-fuel based transportation alternatives, how much will the price deviate?")
########################################################################################################################


st.markdown('***')

st.header("Contacts")

"""
[![MAIL Badge](https://img.shields.io/badge/-jrkagumba@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:e.pogrebnyak@gmail.com)](mailto:e.pogrebnyak@gmail.com)
\n
Thanks for exploring this dataset with me!
If you happen to have a good idea or comment about the dataset, please send me a message.
I appreciate the feedback and look forward to hearing about any other data 
use-cases, project development stories and any future applications of this dataset. 
\n
(C) Joe Kagumba, 2022
"""
