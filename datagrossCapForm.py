import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load the cleaned dataset with the correct relative path
data = pd.read_csv('data/cleaned_grossCapitalFormation.csv')

# Convert the dataset from wide to long format for easier plotting
data_long = data.melt(id_vars=["Country Name", "Country Code"],
                      var_name="Year",
                      value_name="Gross Capital Formation (% of GDP)")

# Convert 'Year' to integers
data_long['Year'] = pd.to_numeric(data_long['Year'], errors='coerce')
data_long.dropna(subset=['Year'], inplace=True)
data_long['Year'] = data_long['Year'].astype(int)

# Initialize a figure with subplots
fig = make_subplots(rows=1, cols=1)

# Add a trace for each country with the specified line color
for country in data_long['Country Name'].unique():
    country_data = data_long[data_long['Country Name'] == country]
    fig.add_trace(
        go.Scatter(
            x=country_data['Year'],
            y=country_data['Gross Capital Formation (% of GDP)'],
            name=country,
            visible=False,  # Hide all traces initially
            line=dict(color='black'),  # Set the line color to black
            connectgaps=False,  # Don't connect gaps
            hovertemplate='Year: %{x}<br>Value: %{y:.2f}'  # Custom hover info
        )
    )

# Create a button for each country, including a 'Select' option
buttons = [dict(label='Select', method='update', args=[{'visible': [False]*len(data_long['Country Name'].unique())}, {'title': 'Select a country'}])]
for i, country in enumerate(data_long['Country Name'].unique()):
    buttons.append(
        dict(
            label=country,
            method="update",
            args=[{"visible": [j == i for j in range(len(data_long['Country Name'].unique()))]},
                  {"title": f"Gross Capital Formation (% of GDP) for {country}"}],
        )
    )

# Add a dropdown to the figure and set the initial layout
fig.update_layout(
    updatemenus=[dict(active=-1, buttons=buttons)],
    title="Gross Capital Formation (% of GDP) by Country and Year",
    xaxis=dict(
        title='',  # Remove x-axis label
        showgrid=False,  # Remove x-axis grid lines
        zeroline=False  # Remove the x-axis zero line
    ),
    yaxis=dict(
        title='',  # Remove y-axis label
        showgrid=False,  # Remove y-axis grid lines
        zeroline=False  # Remove the y-axis zero line
    ),
    plot_bgcolor='white',  # Set background color to white
    paper_bgcolor='white',  # Ensure that the background around the plot is white
    autosize=True  # Auto-adjust the size to fit the container
)

# Use Streamlit to render the figure
st.plotly_chart(fig, use_container_width=True)
