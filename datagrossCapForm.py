import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load your data
data = pd.read_csv('data/cleaned_grossCapitalFormation.csv')

# Transform your data
data_long = data.melt(id_vars=["Country Name", "Country Code"],
                      var_name="Year",
                      value_name="Gross Capital Formation (% of GDP)")
data_long['Year'] = pd.to_numeric(data_long['Year'], errors='coerce')
data_long.dropna(subset=['Year'], inplace=True)
data_long['Year'] = data_long['Year'].astype(int)

# Create the figure
fig = make_subplots(rows=1, cols=1)

# Add the traces for each country to the figure
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

# Sidebar for country selection
country = st.sidebar.selectbox('Select a Country', data_long['Country Name'].unique())

# Update the visibility of the trace corresponding to the selected country
for i, trace in enumerate(fig['data']):
    if trace.name == country:
        fig['data'][i]['visible'] = True

# Update the layout of the figure
fig.update_layout(
    title=f"Gross Capital Formation (% of GDP) for {country}",
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

# Render the plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
