import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Assuming your CSV has the correct format, this should work as expected.
data = pd.read_csv('data/cleaned_grossCapitalFormation.csv')

data_long = data.melt(id_vars=["Country Name", "Country Code"],
                      var_name="Year",
                      value_name="Gross Capital Formation (% of GDP)")

data_long['Year'] = pd.to_numeric(data_long['Year'], errors='coerce')
data_long.dropna(subset=['Year'], inplace=True)
data_long['Year'] = data_long['Year'].astype(int)

fig = make_subplots(rows=1, cols=1)

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
            hovertemplate='Year: %{x}<br>Value: %{y:.2f}<extra></extra>'  # Custom hover info without country name
        )
    )

buttons = [dict(label='Select', method='update', 
                args=[{'visible': [False]*len(data_long['Country Name'].unique())},
                      {'title': 'Select a country to display the data'}])]

for i, country in enumerate(data_long['Country Name'].unique()):
    buttons.append(
        dict(
            label=country,
            method="update",
            args=[{"visible": [j == i for j in range(len(data_long['Country Name'].unique()))]},
                  {"title": f"Gross Capital Formation (% of GDP) for {country}"}],
        )
    )

# Adjust the 'y' parameter here to move the dropdown menu to a suitable location
fig.update_layout(
    updatemenus=[{
        'type': 'dropdown',
        'buttons': buttons,
        'showactive': True,  # Show which button is active
        'direction': 'down',
        'active': 0,  # No country is selected by default
        'pad': {'r': 10, 't': 10},
        'x': 0.01,  # You may adjust this for horizontal positioning
        'xanchor': 'left',
        # Adjust the vertical position of the dropdown to avoid overlap with the chart
        'y': 0.5,  # This value may need adjustment
        'yanchor': 'bottom'
    }],
    title="Select a country to display the data",
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
