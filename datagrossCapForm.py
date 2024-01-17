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

# Initialize session state
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None

# Sidebar for country selection
country_options = list(data_long['Country Name'].unique())
initial_option = ['Select'] if st.session_state.selected_country is None else []
country = st.sidebar.selectbox('Select a Country', initial_option + country_options)

# Update session state
if country != 'Select':
    st.session_state.selected_country = country

# Create the figure
fig = make_subplots(rows=1, cols=1)

# Add the traces for each country to the figure
for country_name in data_long['Country Name'].unique():
    country_data = data_long[data_long['Country Name'] == country_name]
    fig.add_trace(
        go.Scatter(
            x=country_data['Year'],
            y=country_data['Gross Capital Formation (% of GDP)'],
            name=country_name,
            visible=(country_name == st.session_state.selected_country),  # Only show the selected country
            line=dict(color='black'),
            connectgaps=False,
            hovertemplate='Year: %{x}<br>Value: %{y:.2f}<extra></extra>'
        )
    )

# Update the layout of the figure if a country has been selected
if st.session_state.selected_country:
    fig.update_layout(
        title=f"Gross Capital Formation (% of GDP) for {st.session_state.selected_country}",
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
