from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import altair as alt
import pandas as pd
import geopandas as gpd

# Load data
pumas_shp = gpd.read_file('data/shapefiles/data_pumas.shp')
#neighborhood_shp = gpd.read_file('data/shapefiles/data_neighborhoods.shp')
df_c = pd.read_csv("data/census_df.csv")

print(pumas_shp.info())
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111188',
    'text': '#7FDBFF'
}

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
                        # Top row: number + icon
                        html.Div([
                            html.H4("18", className="card-title", style={"margin": 0, "textAlign": "center"}),
                            html.I(className="fas fa-chart-bar", style={"fontSize": "1.8rem"})
                        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center","textAlign": "center"}),

                        html.P("PUMAS", className="card-text", style={"marginTop": "10px"})
                    ]),
                    style={"textAlign": "center"}
                ),
                width=2  # adjust column width as needed
            ),

            # Card 2
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.H4("178", className="card-title", style={"margin": 0}),
                            html.I(className="fas fa-file-alt", style={"fontSize": "1.8rem"})
                        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}),

                        html.P("Neighborhoods", className="card-text", style={"marginTop": "10px"}),
                    ]),
                    style={"textAlign": "center"}
                ),
                width=2
            ),

            # Card 3
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.H4("644", className="card-title", style={"margin": 0}),
                            html.I(className="fas fa-calendar-check", style={"fontSize": "1.8rem"})
                        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}),

                        html.P("Public Schools in 2023", className="card-text", style={"marginTop": "10px"}),
                    ]),
                    style={"textAlign": "center"}
                ),
                width=2
            ),

            # Card 4
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.H4("391K", className="card-title", style={"margin": 0}),
                            html.I(className="fas fa-download", style={"fontSize": "1.8rem"})
                        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}),

                        html.P("School-age population", className="card-text", style={"marginTop": "10px"}),
                    ]),
                    style={"textAlign": "center"}
                ),
                width=2
            ),
        ],
        justify="center",  # horizontally center the row
        style={"marginBottom": "10px"}
    ),

    html.Div(
        style={'display': 'flex'},
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
            )
        ]
    )
])

# Callback updates the containers with iframes that embed the Altair charts.
@callback(
    Output('scatter-graph-container', 'children'),
    Output('bar-graph-container', 'children'),
    Output('crime_map', 'children'),
    Input('dropdown-year', 'value')
)
def update_charts(selected_year):
    # Filter data for the selected year
    dff = df_c[df_c['year'] == selected_year]
    brush = alt.selection_interval()
    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)
    stroke_width = (
    alt.when(select).then(alt.value(2, empty=False))
    .when(highlight).then(alt.value(1))
    .otherwise(alt.value(0))
    )

   # Create the scatter plot with a brush selection
    fig_scatter = alt.Chart(dff).mark_point().encode(
        x='attendance_rate_high',
        y='atten_middle_women_w',
        color=alt.condition(brush, alt.value("steelblue"), alt.value("grey"))
    ).add_params(brush).properties(
        title=f"Scatter Plot for Year {selected_year}"
    )

    # Create the bar chart sorted descending by attendance_rate_high
    fig_bar = alt.Chart(dff).mark_bar(fill="#0099cc", stroke="black", cursor="pointer").encode(
        x=alt.X('puma_label',axis=alt.Axis(title='PUMA name'), sort=alt.EncodingSortField(field='attendance_rate_high', op='sum', order='descending')),
        y=alt.Y('attendance_rate_high', axis=alt.Axis(title='Attendance rate - high school')),
        fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
        strokeWidth=stroke_width,
    ).properties(
        title=f"Attendance Rate for Year {selected_year} - High School (self reported)"
    ).add_params(select, highlight)

    # Create the crime map by puma and neighborhood
    df_map = pumas_shp[pumas_shp['year'] == selected_year]
    df_map['total_crime_pc'] = df_map['total_crim'] / df_map['pwgtp'] * 1000
    crime_map = alt.Chart(df_map).mark_geoshape(
        stroke = 'white', strokeWidth = 0.5
        ).encode(color = 'total_crime_pc', tooltip = ['puma_label', 'year','total_crime_pc'] 
        ).project(
            type='mercator'
        ).properties(
            width=500,
            height=500,
            title=f"Crime ocurrances per 1000 hab. for Year {selected_year}"
        )

    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(srcDoc=fig_bar.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'}),
        html.Iframe(srcDoc=fig_scatter.to_html(), style={'width': '100%', 'height': '400px', 'border': '0'}),
        html.Iframe(srcDoc=crime_map.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'})
        
    )

if __name__ == '__main__':
    app.run_server(debug=True)