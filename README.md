# Citi Bikes Analysis

## Project Summary
For this project, the goal was to analyze user behavior to help the business strategy department assess the current logistics model of bike distribution across the city, while also identify expansion opportunities. 

## Key Questions
<ul>
    <li>What are the most popular stations in the city?</li>
    <li>Which are the months with the most trips taken? Is there a weather component at play? How does temperature affect ridership numbers?</li>
    <li>What are the most popular trips between stations?</li>
    <li>Are the existing stations evenly distributed?</li>
    <li>How does weekday vs. weekend ridership differ?</li>
    <li>Are electric bikes more popular than classic bikes? </li>
</ul>

## Data Review
Two sets of data were used for this analysis: 
<ul>
    <li>Citi Bike database for the year 2022 - New York City</li>
    Source: https://s3.amazonaws.com/tripdata/index.html 
    <li>Weather data for the year 2022 using NOAA's API - New York’s LaGuardia Airport</li>
    Source: https://www.ncdc.noaa.gov/cdo-web/datatools/findstation 
</ul>

## Systems Used
<ul>
    <li>Python (including virtual environments via Anaconda)</li>
    <li>GitHub (repositories, SSH keys, version control workflows)</li>
    <li>Web Scraping Tools & Libraries (e.g., requests, BeautifulSoup)</li>
    <li>NLP & Text Mining Libraries (e.g., NLTK, spaCy, pandas)</li>
    <li>Visualization & Dashboard Tools (matplotlib, seaborn, Plotly, Streamlit, kepler.gl)</li>
    <li>APIs for Web Data Access</li>
</ul>

## Key Takeaways
<ul>
    <li>As the weather warms up, the number of trips increase, with June through October showing the highest ridership.</li>
    <li>The most popular station is Grove St PATH, followed by South Waterfront Walkway and Hoboken Terminal.</li>
    <li>Electric bikes and classic bikes have similar distributions for ridership and at bike stations.</li>
    <li>Members have the highest ridership during weekdays.</li>
</ul>

## Final Deliverable
- <a href="https://citibikesanalysis-qrqgtuhpdxhdd9g5eplksq.streamlit.app/">Streamlit Site</a><br>
- <a href="https://vimeo.com/1135090471?share=copy&fl=sv&fe=ci">Vimeo Presentation</a><br>

