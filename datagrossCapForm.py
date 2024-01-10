# Create the 'Select' option button
buttons = [dict(label='Select', method='update', 
                args=[{'visible': [False]*len(data_long['Country Name'].unique())},
                      {'title': 'Select a country to display the data'}])]

# Create a button for each country
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
        'showactive': False,  # Prevents showing the active selection
        'active': -1,  # Ensures no button is selected initially
        'buttons': buttons,
        'direction': 'down',
        'pad': {'r': 10, 't': 10},
        'x': 0.01,  # Adjust the position of the dropdown menu
        'xanchor': 'left',
        'y': 1.15,  # Adjust the position of the dropdown menu
        'yanchor': 'top'
    }],
    # ... other layout configurations
)

# Rest of the code for setting layout and displaying the plot using Streamlit
# ...
