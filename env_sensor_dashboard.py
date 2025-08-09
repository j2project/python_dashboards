import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Initialize the Dash app
app = dash.Dash(__name__)

# ============================================================================
# DATA SIMULATION
# ============================================================================

def generate_environmental_data():
    """
    Generate simulated environmental sensor data for three distinct locations
    with realistic parameter ranges for each environment.
    """
    
    # Define the three locations
    locations = ["Amazon Rainforest", "Great Barrier Reef", "Siberian Tundra"]
    
    # Generate timestamps (100 days of daily readings)
    start_date = datetime.now() - timedelta(days=99)
    timestamps = [start_date + timedelta(days=i) for i in range(100)]
    
    # Initialize empty list to store all data
    all_data = []
    
    # Define realistic parameter ranges for each location
    location_params = {
        "Amazon Rainforest": {
            "temperature": (22, 35),      # Tropical temperatures
            "salinity": (0, 0.5),         # Freshwater environment
            "dissolved_oxygen": (6, 9),   # High oxygen from vegetation
            "ph": (6.0, 7.5),            # Slightly acidic from organic matter
            "turbidity": (10, 50),        # Moderate turbidity from sediments
            "nitrate": (5, 25),           # Moderate levels from organic decomposition
            "phosphate": (1, 8),          # Low to moderate phosphate
            "chlorophyll": (15, 45),      # High from abundant plant life
            "organism": ["Jaguar", "Toucan", "Anaconda", "Poison Dart Frog", "Sloth"]
        },
        "Great Barrier Reef": {
            "temperature": (20, 30),      # Tropical marine temperatures
            "salinity": (34, 37),         # Marine salinity levels
            "dissolved_oxygen": (7, 10),  # Good oxygen levels
            "ph": (7.8, 8.3),            # Alkaline marine environment
            "turbidity": (1, 15),         # Clear marine water
            "nitrate": (0.5, 5),          # Low nitrate in healthy reef
            "phosphate": (0.1, 2),        # Very low phosphate levels
            "chlorophyll": (0.5, 5),      # Lower chlorophyll in clear water
            "organism": ["Clownfish", "Sea Turtle", "Coral", "Whale Shark", "Manta Ray"]
        },
        "Siberian Tundra": {
            "temperature": (-25, 5),      # Cold arctic temperatures
            "salinity": (0, 1),           # Freshwater/brackish
            "dissolved_oxygen": (10, 14), # High oxygen in cold water
            "ph": (6.5, 8.0),            # Variable pH
            "turbidity": (2, 20),         # Low to moderate turbidity
            "nitrate": (1, 15),           # Low to moderate nitrate
            "phosphate": (0.5, 5),        # Low phosphate levels
            "chlorophyll": (1, 10),       # Low chlorophyll due to cold
            "organism": ["Siberian Tiger", "Arctic Fox", "Reindeer", "Snowy Owl", "Polar Bear"]
        }
    }
    
    # Generate data for each location
    for location in locations:
        params = location_params[location]
        
        for i, timestamp in enumerate(timestamps):
            # Add some seasonal variation and random noise
            season_factor = np.sin(2 * np.pi * i / 365) * 0.3 + 1
            
            data_point = {
                'Timestamp': timestamp,
                'Location': location,
                'Temperature (°C)': round(random.uniform(*params["temperature"]) * season_factor, 1),
                'Salinity (PSU)': round(random.uniform(*params["salinity"]), 2),
                'Dissolved Oxygen (mg/L)': round(random.uniform(*params["dissolved_oxygen"]), 1),
                'pH': round(random.uniform(*params["ph"]), 2),
                'Turbidity (NTU)': round(random.uniform(*params["turbidity"]), 1),
                'Nitrate (µM)': round(random.uniform(*params["nitrate"]), 1),
                'Phosphate (µM)': round(random.uniform(*params["phosphate"]), 2),
                'Chlorophyll (µg/L)': round(random.uniform(*params["chlorophyll"]), 1),
                'Organism Presence': random.choice(params["organism"])
            }
            
            all_data.append(data_point)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    df = df.sort_values(['Location', 'Timestamp']).reset_index(drop=True)
    
    return df

# Generate the dataset
df = generate_environmental_data()

# ============================================================================
# DASHBOARD LAYOUT
# ============================================================================

app.layout = html.Div([
    # Main title
    html.H1("Multi-Location Environmental Sensor Dashboard", 
            style={'textAlign': 'center', 'marginBottom': 30, 'color': '#2c3e50'}),
    
    # Controls section
    html.Div([
        html.Label("Select Location:", style={'fontSize': 16, 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='location-dropdown',
            options=[
                {'label': 'All Locations', 'value': 'All'},
                {'label': 'Amazon Rainforest', 'value': 'Amazon Rainforest'},
                {'label': 'Great Barrier Reef', 'value': 'Great Barrier Reef'},
                {'label': 'Siberian Tundra', 'value': 'Siberian Tundra'}
            ],
            value='All',
            style={'marginBottom': 20}
        )
    ], style={'width': '300px', 'margin': '0 auto'}),
    
    # Organism presence indicator
    html.Div(id='organism-indicator', style={
        'textAlign': 'center', 
        'fontSize': 18, 
        'fontWeight': 'bold',
        'marginBottom': 20,
        'padding': 10,
        'backgroundColor': '#ecf0f1',
        'borderRadius': 5
    }),
    
    # Time series plots section
    html.H2("Environmental Parameters Over Time", 
            style={'textAlign': 'center', 'marginTop': 30, 'color': '#34495e'}),
    
    html.Div([
        # Temperature plot
        html.Div([
            dcc.Graph(id='temperature-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
        
        # Salinity plot
        html.Div([
            dcc.Graph(id='salinity-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
    ]),
    
    html.Div([
        # Dissolved Oxygen plot
        html.Div([
            dcc.Graph(id='oxygen-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
        
        # pH plot
        html.Div([
            dcc.Graph(id='ph-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
    ]),
    
    html.Div([
        # Turbidity plot
        html.Div([
            dcc.Graph(id='turbidity-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
        
        # Placeholder for symmetry
        html.Div([
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
    ]),
    
    # Nutrient and chlorophyll analysis section
    html.H2("Nutrient Analysis and Chlorophyll Distribution", 
            style={'textAlign': 'center', 'marginTop': 30, 'color': '#34495e'}),
    
    html.Div([
        # Nutrient bar chart
        html.Div([
            dcc.Graph(id='nutrient-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
        
        # Chlorophyll pie chart
        html.Div([
            dcc.Graph(id='chlorophyll-pie')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': 10}),
    ])
    
], style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'})

# ============================================================================
# CALLBACK FUNCTIONS
# ============================================================================

@callback(
    [Output('temperature-plot', 'figure'),
     Output('salinity-plot', 'figure'),
     Output('oxygen-plot', 'figure'),
     Output('ph-plot', 'figure'),
     Output('turbidity-plot', 'figure'),
     Output('nutrient-chart', 'figure'),
     Output('chlorophyll-pie', 'figure'),
     Output('organism-indicator', 'children')],
    [Input('location-dropdown', 'value')]
)
def update_dashboard(selected_location):
    """
    Update all dashboard components based on the selected location.
    """
    
    # Filter data based on selection
    if selected_location == 'All':
        filtered_df = df.copy()
        show_all_locations = True
    else:
        filtered_df = df[df['Location'] == selected_location].copy()
        show_all_locations = False
    
    # Color mapping for locations
    color_map = {
        'Amazon Rainforest': '#27ae60',  # Green
        'Great Barrier Reef': '#3498db', # Blue
        'Siberian Tundra': '#95a5a6'     # Gray
    }
    
    # ========================================================================
    # TIME SERIES PLOTS
    # ========================================================================
    
    def create_time_series_plot(y_column, title, y_label):
        """Helper function to create consistent time series plots"""
        if show_all_locations:
            fig = px.line(filtered_df, x='Timestamp', y=y_column, 
                         color='Location', title=title,
                         color_discrete_map=color_map)
        else:
            fig = px.line(filtered_df, x='Timestamp', y=y_column, 
                         title=title, color_discrete_sequence=[color_map.get(selected_location, '#34495e')])
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=y_label,
            hovermode='x unified',
            template='plotly_white'
        )
        return fig
    
    # Create individual time series plots
    temp_fig = create_time_series_plot('Temperature (°C)', 
                                      'Temperature Over Time', 'Temperature (°C)')
    
    salinity_fig = create_time_series_plot('Salinity (PSU)', 
                                          'Salinity Over Time', 'Salinity (PSU)')
    
    oxygen_fig = create_time_series_plot('Dissolved Oxygen (mg/L)', 
                                        'Dissolved Oxygen Over Time', 'Dissolved Oxygen (mg/L)')
    
    ph_fig = create_time_series_plot('pH', 
                                    'pH Over Time', 'pH')
    
    turbidity_fig = create_time_series_plot('Turbidity (NTU)', 
                                           'Turbidity Over Time', 'Turbidity (NTU)')
    
    # ========================================================================
    # NUTRIENT BAR CHART
    # ========================================================================
    
    if show_all_locations:
        # Calculate average nutrient levels for all locations
        nutrient_data = filtered_df.groupby('Location')[['Nitrate (µM)', 'Phosphate (µM)']].mean().reset_index()
        
        # Reshape data for grouped bar chart
        nutrient_melted = nutrient_data.melt(id_vars=['Location'], 
                                           value_vars=['Nitrate (µM)', 'Phosphate (µM)'],
                                           var_name='Nutrient', 
                                           value_name='Concentration')
        
        nutrient_fig = px.bar(nutrient_melted, x='Location', y='Concentration', 
                             color='Nutrient', barmode='group',
                             title='Average Nutrient Levels by Location',
                             color_discrete_map={
                                 'Nitrate (µM)': '#e74c3c',
                                 'Phosphate (µM)': '#f39c12'
                             })
    else:
        # Show nutrient levels for selected location only
        nutrient_avg = filtered_df[['Nitrate (µM)', 'Phosphate (µM)']].mean()
        
        nutrient_fig = go.Figure(data=[
            go.Bar(name='Nitrate (µM)', x=['Nitrate'], y=[nutrient_avg['Nitrate (µM)']], 
                   marker_color='#e74c3c'),
            go.Bar(name='Phosphate (µM)', x=['Phosphate'], y=[nutrient_avg['Phosphate (µM)']], 
                   marker_color='#f39c12')
        ])
        
        nutrient_fig.update_layout(
            title=f'Average Nutrient Levels - {selected_location}',
            xaxis_title='Nutrient Type',
            yaxis_title='Concentration (µM)',
            template='plotly_white'
        )
    
    # ========================================================================
    # CHLOROPHYLL PIE CHART
    # ========================================================================
    
    if show_all_locations:
        # Calculate total chlorophyll by location
        chlorophyll_data = filtered_df.groupby('Location')['Chlorophyll (µg/L)'].sum().reset_index()
        
        chlorophyll_fig = px.pie(chlorophyll_data, 
                                values='Chlorophyll (µg/L)', 
                                names='Location',
                                title='Chlorophyll Distribution by Location',
                                color='Location',
                                color_discrete_map=color_map)
    else:
        # Show chlorophyll distribution over time for selected location
        chlorophyll_fig = px.histogram(filtered_df, x='Chlorophyll (µg/L)', 
                                      title=f'Chlorophyll Distribution - {selected_location}',
                                      nbins=20,
                                      color_discrete_sequence=[color_map.get(selected_location, '#34495e')])
        chlorophyll_fig.update_layout(
            xaxis_title='Chlorophyll (µg/L)',
            yaxis_title='Frequency',
            template='plotly_white'
        )
    
    # ========================================================================
    # ORGANISM PRESENCE INDICATOR
    # ========================================================================
    
    if show_all_locations:
        # Show most recent organism from each location
        recent_organisms = []
        for location in df['Location'].unique():
            latest_organism = df[df['Location'] == location]['Organism Presence'].iloc[-1]
            recent_organisms.append(f"{location}: {latest_organism}")
        
        organism_text = html.Div([
            html.H4("Most Recent Organism Sightings:"),
            html.Ul([html.Li(org) for org in recent_organisms])
        ])
    else:
        # Show most recent organism for selected location
        latest_organism = filtered_df['Organism Presence'].iloc[-1]
        organism_text = html.Div([
            html.H4(f"Most Recent Organism Sighting in {selected_location}:"),
            html.P(f"🦎 {latest_organism}", style={'fontSize': 20, 'color': '#e67e22'})
        ])
    
    return (temp_fig, salinity_fig, oxygen_fig, ph_fig, turbidity_fig, 
            nutrient_fig, chlorophyll_fig, organism_text)

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run_server(debug=True, host='127.0.0.1', port=8050)
    
    print("\n" + "="*60)
    print("Environmental Sensor Dashboard is running!")
    print("Open your browser and go to: http://127.0.0.1:8050")
    print("="*60)