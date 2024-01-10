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

# Create a button for each country
buttons = []
for i, country in enumerate(data_long['Country Name'].unique()):
    buttons.append(
        dict(
            label=country,
            method="update",
            args=[{"visible": [j == i for j in range(len(data_long['Country Name'].unique()))]},
                  {"title": f"Gross Capital Formation (% of GDP) for {country}"}],
        )
    )

# Update the layout of the figure to include the dropdown and set text color
fig.update_layout(
    updatemenus=[{
        'type': 'dropdown',
        'buttons': buttons,
        'direction': 'down',
        'active': -1,  # No country is selected by default
        'pad': {'r': 10, 't': 10},
        'x': 0.01,
        'xanchor': 'left',
        'y': 1.15,
        'yanchor': 'top'
    }],
    title="Select a country to display the data",  # Default title
    title_font_color='black',
    xaxis=dict(
        title='',
        showgrid=False,
        zeroline=False,
        tickfont=dict(color='black'),
    ),
    yaxis=dict(
        title='',
        showgrid=False,
        zeroline=False,
        tickfont=dict(color='black'),
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='black',
    autosize=True
)

# Use Streamlit to render the figure
st.plotly_chart(fig, use_container_width=True)
