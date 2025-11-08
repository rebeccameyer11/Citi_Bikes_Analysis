################################################ CITI BIKES DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import seaborn as sns


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'New York Citi Bikes Analysis Dashboard', layout='wide')
st.title("New York Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Analysis Selector")
page = st.sidebar.selectbox('Select an analysis page',
  ["Intro Page","Weather and Bike Usage",
   "Most Popular Stations",
    "Interactive Map", "Ride Patterns", "Recommendations"])


########################## Import data ###########################################################################################

df = pd.read_csv('reduced_ny_data_to_plot_7.csv')
top20 = pd.read_csv('newyork_top20.csv', index_col = 0)


######################################### DEFINE THE PAGES #####################################################################



### Intro Page
if page == "Intro Page":
    st.markdown("#### This dashboard provides a descriptive analysis of Citi Bike usage patterns in New York City to help the Business Strategy Team uncover actionable insights. The goal is to anticipate availability issues and strengthen Citi Bike’s position as a leader in eco-friendly transportation solutions.")
    st.markdown("#### Purpose")
    st.markdown("The analysis aims to evaluate user behavior and bike distribution logistics across the city. By examining key trends and relationships, the team can assess current operations and identify potential expansion opportunities to optimize service availability.")
    st.markdown("#### Dashboard Overview")
    st.markdown("The dashboard is organized into five main sections:")
    st.markdown("1. Weather and Bike Usage – Explores how weather conditions influence ridership patterns.")
    st.markdown("2. Most Popular Stations – Identifies the most popular bike stations.") 
    st.markdown("3. Interactive Map – Visualizes aggregated bike trips across New York City.")
    st.markdown("4. Ride Patterns – Compares ride type usage and examines how ridership differs on weekdays vs weekends.")
    st.markdown("5. Recommendations – Summarizes actionable findings for strategic decision-making.")
    st.markdown("Use the ‘Analysis Selector’ dropdown menu on the left to navigate between sections and explore each component of the analysis.")

    myImage = Image.open("girlandbikes.jpg") #source: https://www.freepik.com/search?format=search&last_filter=query&last_value=bike+ride+in+nyc&query=bike+ride+in+nyc
    st.image(myImage)
    st.markdown("Image Source: Freepik (https://www.freepik.com/search?format=search&last_filter=query&last_value=bike+ride+in+nyc&query=bike+ride+in+nyc)")


### Weather and Bike Usage ###

### Create the dual axis line chart page ###
    
elif page == 'Weather and Bike Usage':

    
# Ensure date is datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

# Dual Axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['bike_rides_daily'], 
            name='Daily Trips',
            line_shape='spline'
        ),
        secondary_y=False
    )

    fig2.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['avgTemp'], 
            name='Daily Temperature',
            line_shape='spline'
        ),
        secondary_y=True
    )

    fig2.update_layout(
        title='Daily Trips vs Temperature',
        xaxis_title='Date',
        yaxis_title='Trips',
        yaxis2_title='Temperature (°F)',
        template='plotly_white'
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("#### Weather and Bike Usage Analysis:")
    st.markdown("There is a clear positive correlation between temperature and ridership — as the weather warms up, the number of trips increase. Warmer months such as June through October show the highest ridership, coinciding with comfortable summer and early fall conditions that encourage outdoor activity. Conversely, during the colder months (November through February), ridership declines significantly, suggesting that temperature plays a key role in bike usage behavior. This trend highlights the seasonal nature of demand, which can help guide bike redistribution and promotional strategies — for example, allocating more bikes to high-demand stations during warmer months and focusing on maintenance or marketing incentives during the off-season.")


### Most Popular Stations page

    # Create the season variable

elif page == 'Most Popular Stations':
    
   # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City',
    xaxis_title = 'Start Stations',
    yaxis_title ='Sum of Trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### Most Popular Citi Bike Stations Analysis:")
    st.markdown("This bar chart highlights the top 20 most popular Citi Bike stations across New York City. The Grove St PATH station stands out as the most popular station, recording significantly higher trip counts compared to other stations. This suggests it serves as a major commuter hub, due to its proximity to key transit connections and large residential and/or business areas. Following Grove St PATH, stations such as South Waterfront Walkway, Hoboken Terminal, and City Hall show slightly lower but still substantial usage. The gradual decline among the remaining stations indicates that while demand is distributed across the network, a small number of high-traffic stations account for a large share of total rides. These insights can help prioritize bike redistribution and maintenance efforts around these high-demand stations to reduce shortages and improve rider experience.")

    
### Interactive Map page

elif page == 'Interactive Map': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips across New York City")
    with open("New York Citi Bikes Bike Trips Aggregated_small.html", "r", encoding="utf-8") as f:
        html_data = f.read()


    # Display map
    st.components.v1.html(html_data, height=900, scrolling=True)
 
    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.markdown("#### Interactive Map of Bike Trips in New York City Analysis:")
    st.markdown("Using the filter on the left hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("This interactive map visualizes aggregated Citi Bike trips across New York City and surrounding areas, showing the spatial flow of bike usage between major start and end stations. Each line represents a connection between stations, and areas with denser lines indicate higher trip volumes. The map highlights the most popular bike trips — particularly between Jersey City, Journal Square, and Hoboken — suggesting these neighborhoods serve as key hubs within the Citi Bike network. This visualization allows users to explore travel patterns geographically, which highlight high travel density that may require additional bikes or docks.")


### Ride Patterns page
elif page == 'Ride Patterns':

    ### Create boxplot ###
    fig, ax = plt.subplots(figsize=(6,3.5))

    sns.boxplot(
        x='rideable_type',
        y='bike_rides_daily',
        data=df,
        hue='rideable_type',
        palette={
            'electric_bike': 'royalblue',
            'classic_bike': 'orange',
            'docked_bike': 'gray'
        },
        legend=False,
        ax=ax
    )

    ax.set_title("Most Popular Ride Type on Daily Rides")
    st.pyplot(fig)

    st.markdown("#### Box Plot of Ride Type Analysis:")
    st.markdown("The box plot shows that electric bikes and classic bikes have similar distributions, with comparable box and whisker lengths. Classic bikes are slightly shifted upward, suggesting higher daily usage overall. Both bike types are left-skewed, with high median values, indicating that most days experience relatively high ride counts, while a few days see lower activity. Docked bikes were excluded from this analysis, as they are typically unused, and the focus was on comparing popular ride types.")
    st.markdown("Considerations: The similar usage may reflect an even distribution of electric and classic bikes at stations or riders simply taking whichever bike is available. Additionally, some users may not utilize the electric features when choosing an electric bike, effectively riding it as a classic bike.")

 ### Create FacetGrid ###

    # FacetGrid

    grid = sns.FacetGrid(df, col="day_type")
    grid.map(sns.histplot, "member_casual", bins=15)

    st.pyplot(grid.fig)


    st.markdown("#### FacetGrid Day Type and Member Type Analysis:")
    st.markdown("This comparison was generally in line with expectations, but I was surprised that casual rides — those by non-members — were not higher on weekends. I anticipated that member rides would peak during weekdays, likely reflecting commuting or regular activities, while casual rides would increase on weekends as people explore the city or take economical trips. Interestingly, casual rides were higher during weekdays, which could reflect last-minute commuting needs, extracurricular trips, or tourists visiting midweek.")
    st.markdown("Recommendations: To encourage more weekend usage, consider special pricing or promotions. Additionally, further analysis could explore the factors driving weekday versus weekend rides and examine ride duration across user types to better understand behavior patterns.")



### Recommendations page

else:
    
    st.header("Insights and Recommendations")
    st.markdown("#### Insights:")
    st.markdown("As the weather warms up, the number of trips increase, with June through October showing the highest ridership.")
    st.markdown("The most popular station is Grove St PATH, followed by South Waterfront Walkway and Hoboken Terminal.")
    st.markdown("Electric bikes and classic bikes have similar distributions for ridership and at bike stations.")
    st.markdown("Members have the highest ridership during weekdays.")
    st.markdown("#### Recommendations:")
    st.markdown("#### Plan Seasonally Adjusted Operations")
    st.markdown("Ridership increases significantly during warmer months (June–October) and declines in winter. Adjust maintenance schedules, bike distribution, and staffing accordingly — prioritize maintenance and redistribution during low-demand months, and scale up availability and marketing during peak seasons.")
    st.markdown("#### Enhance Service in Key Travel Areas")
    st.markdown("The interactive map highlights strong cycling activity between Jersey City, Hoboken, and Journal Square. Consider adding stations or expanding capacity in these areas to support high connectivity and meet commuter demand.")
    st.markdown("#### Identify Expansion Opportunities")
    st.markdown("Explore underutilized areas visible on the map for potential network growth. Conduct targeted promotions or partnerships to encourage ridership in neighborhoods with good infrastructure but lower trip density.")
    st.markdown("#### Support Sustainability and Community Goals")
    st.markdown("Continue leveraging Citi Bike’s role in eco-friendly travel around New York City. Encourage usage through seasonal membership campaigns and community engagement events to strengthen brand loyalty.")
    bikes = Image.open("recommendations.jpg")
    st.image(bikes)
    st.markdown("Image source: https://www.freepik.com/search?format=search&last_filter=query&last_value=recommendations&query=recommendations")
