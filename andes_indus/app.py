from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import altair as alt
import pandas as pd
import geopandas as gpd
from figures import create_crime_map

# Load data
pumas_shp = gpd.read_file('data/shapefiles/data_pumas.shp')
neighborhood_shp = gpd.read_file('data/shapefiles/data_neighborhoods.shp')

# Create the crime map by puma and neighborhood
for var in ['total_crim', 'Violent', 'Non-violen']: 
    pumas_shp[f'{var}_pc'] = pumas_shp[f'{var}'] / pumas_shp['pwgtp'] * 1000

pumas_df = pd.read_csv('data/data_pumas.csv')
pumas_df = pumas_df.rename(columns={'total_crimes': 'total_crim',
                                    'Violent': 'Violent',
                                    'Non-violent': 'Non-violen'})
for var in ['total_crim', 'Violent', 'Non-violen']: 
    pumas_df[f'{var}_pc'] = pumas_df[f'{var}'] / pumas_df['pwgtp'] * 1000



df_c = pd.read_csv("data/census_df.csv")

crime_labels = {
    'total_crim_pc': 'Total Crime',
    'Violent_pc': 'Violent Crime',
    'Non-violen_pc': 'Non Violent Crime'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111188',
    'text': '#7FDBFF'
}
s
# Layout with two columns
app.layout = html.Div([
    # "Header" section
    html.Div(
        children=[
            html.H1([
                # "Michelin Guide to France" in black
                html.Span("Understanding School Attendance and Crime in", 
                          style={"color": "#000000", 
                                 "font-weight": "normal"}),
                " ",  # space
                # "chicago in blue" 
                html.Span("Chicago", 
                          style={"color": "#00bfff", 
                                 "font-weight": "normal"})
            ], 
            style={
                "font-family": "Times New Roman, serif", 
                "font-size": "36px",
                "margin": "0",   # remove default H1 margin
                "padding": "0"
            }),

            # A thin border line below the header
            html.Div(style={
                "border-bottom": "1px solid #ccc",
                "margin-top": "5px",
                "margin-bottom": "20px"
            })
        ],
        style={
            "padding": "10px"  # some padding around the "header"
        }
    ),

dbc.Row(
        [
            # Card 1
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H4("18", className="card-title", style={"margin": 0}),
                        html.I(className="fas fa-chart-bar", style={"fontSize": "1.8rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "center"}),

                    html.P("Pumas", className="card-text", style={"marginTop": "10px"})
                ]),
                style={"textAlign": "center", "borderLeft": "10px solid #37526f"}
            ),
            md=2
        ),

            # Card 2
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H4("178", className="card-title", style={"margin": 0}),
                        html.I(className="fas fa-file-alt", style={"fontSize": "1.8rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "center"}),

                    html.P("Neighborhoods", className="card-text", style={"marginTop": "10px"})
                ]),
                style={"textAlign": "center", "borderLeft": "10px solid #3b6d92"}
            ),
            md=2
        ),

            # Card 3
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H4("644", className="card-title", style={"margin": 0}),
                        html.I(className="fas fa-calendar-check", style={"fontSize": "1.8rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "center"}),

                    html.P("Public Schools in 2023", className="card-text", style={"marginTop": "10px"})
                ]),
                style={"textAlign": "center", "borderLeft": "10px solid #3f88b4"}
            ),
            md=2
        ),

            # Card 4
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H4("391K", className="card-title", style={"margin": 0}),
                        html.I(className="fas fa-download", style={"fontSize": "1.8rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "center"}),

                    html.P("School-age population", className="card-text", style={"marginTop": "10px"})
                ]),
                style={"textAlign": "center", "borderLeft": "10px solid #eb9b44"}
            ),
            md=2
        ),
        # Card 5
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H4("260K", className="card-title", style={"margin": 0}),
                        html.I(className="fas fa-download", style={"fontSize": "1.8rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "center"}),

                    html.P("Total crimes in 2023", className="card-text", style={"marginTop": "10px"})
                ]),
                style={"textAlign": "center", "borderLeft": "10px solid #ba9873"}
            ),
            md=2
        ),
        ],
        justify="center",  # horizontally center the row
        style={"marginBottom": "10px", "fontFamily": "Times New Roman, serif"}
    ),

    html.Div(
        style={'display': 'flex', "fontFamily": "Times New Roman, serif"},
        children=[
            # Left column: text and controls
            html.Div(
                style={'width': '50%', 'padding': '20px'},
                children=[
                    html.P("This is a paragraph with background info."),
                    html.Label("Select Year:"),
                    dcc.Dropdown(
                        options=[{'label': str(year), 'value': year} for year in sorted(df_c['year'].unique())],
                        value=sorted(df_c['year'].unique())[0],
                        id='dropdown-year'
                    ),
                    html.P(
                        "Story or problem we are tackling. "
                        "Use this space for any narrative or instructions."
                    )
                ]
            ),
            # Right column: the graphs
            html.Div(
                style={'width': '50%', 'padding': '20px'},
                children=[
                    html.Div(id='scatter-graph-container'),
                    html.Div(id='bar-graph-container'),
                    html.Div(id='crime_map')
                ]
            ),
            dcc.RadioItems(
                    id='crime-type',
                    options=[
                        {'label': 'Total Crime', 'value': 'total_crim_pc'},
                        {'label': 'Violent Crime', 'value': 'Violent_pc'},
                        {'label': 'Non Violent Crime', 'value': 'Non-violen_pc'}
                        ],
                        value='total_crim_pc',
                        inline=True)
        ]
    )
])

# Callback updates the containers with iframes that embed the Altair charts.
@callback(
    # Output('pyramid-graph-container','children'),
    Output('scatter-graph-container', 'children'),
    Output('bar-graph-container', 'children'),
    Output('crime_map', 'children'),
    Input('dropdown-year', 'value'),
    Input('crime-type', 'value')
)
def update_charts(selected_year, selected_crime):
    # Filter data for the selected year
    dff = df_c[df_c['year'] == selected_year]

    # for the pyramid 
    slider = alt.binding_range(min=1850, max=2000, step=10)
    select_year = alt.selection_point(name='year', fields=['year'],
                                   bind=slider, value=2023)
    
    # for the interactive barchart 
    brush = alt.selection_interval()
    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)
    stroke_width = (
    alt.when(select).then(alt.value(2, empty=False))
    .when(highlight).then(alt.value(1))
    .otherwise(alt.value(0))
    )



    # create a pyramid with the school age population per sex and race 
    
    selection = alt.selection_point(fields=['site'], bind='legend')
    fig_pyramid = alt.Chart(dff).mark_bar().transform_calculate(
    site_order=f"if({selection.name}.site && indexof({selection.name}.site, datum.site) !== -1, 0, 1)"
).encode(
    x='sum(yield):Q',
    y='variety:N',
    color='site:N',
    order='site_order:N',
    opacity=alt.when(selection).then(alt.value(0.9)).otherwise(alt.value(0.2))
).add_params(
    selection
)
    
   # Create the scatter plot with a brush selection
    brush = alt.selection_interval()
    df_scatter = pumas_df[pumas_df['year'] == selected_year]
    scatter = alt.Chart(df_scatter).mark_point().encode(
        x=alt.X(f'{selected_crime}:Q', title=crime_labels[selected_crime]).scale(zero=False, domainMid=10),
        y=alt.X('attendance_rate_high_black:Q', title = "Attendance Rate - High School").scale(zero=False, domainMid=10),
        color=alt.condition(brush, alt.value("steelblue"), alt.value("grey"))
    ).add_params(brush).properties(
        title=f"Scatter Plot for Year {selected_year}"
    )

    regression_line = alt.Chart(df_scatter).transform_regression(
        selected_crime, 'attendance_rate_high_black'
        ).mark_line(color='red'
        ).encode(
            x=alt.X(f"{selected_crime}:Q"),
            y=alt.Y("attendance_rate_high_black:Q")
)

    fig_scatter = (scatter + regression_line).properties(
        title=f"Scatter Plot for Year {selected_year}")

    # Create the bar chart sorted descending by attendance_rate_high
    fig_bar = alt.Chart(dff).mark_bar(fill="#0099cc", stroke="black", cursor="pointer").encode(
        x=alt.X('puma_label',axis=alt.Axis(title='PUMA name'), sort=alt.EncodingSortField(field='attendance_rate_high', op='sum', order='descending')),
        y=alt.Y('attendance_rate_high', axis=alt.Axis(title='Attendance rate - high school')),
        fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
        strokeWidth=stroke_width,
    ).properties(
        title=f"Attendance Rate for Year {selected_year} - High School (self reported)"
    ).add_params(select, highlight)

    # Creating a map
    crime_map = create_crime_map(pumas_shp, selected_crime, selected_year, crime_labels)
    
    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(srcDoc=fig_bar.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'}),
        html.Iframe(srcDoc=fig_scatter.to_html(), style={'width': '100%', 'height': '400px', 'border': '0'}),
        html.Iframe(srcDoc=crime_map.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'})
    )

if __name__ == '__main__':
    app.run_server(debug=True)
