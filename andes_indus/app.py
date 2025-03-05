from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import altair as alt
import pandas as pd
import geopandas as gpd

# Load data
pumas_shp = gpd.read_file('data/shapefiles/data_pumas.shp')
pumas_df = pd.read_csv('data/data_pumas.csv')
#neighborhood_shp = gpd.read_file('data/shapefiles/data_neighborhoods.shp')
df_c = pd.read_csv("data/census_df.csv")
df_c_long = pd.read_csv("data/census_df_long.csv")

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
                    html.Div(id='stacked-graph-container'),
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
    Output('stacked-graph-container','children'),
    Output('scatter-graph-container', 'children'),
    Output('bar-graph-container', 'children'),
    Output('crime_map', 'children'),
    Input('dropdown-year', 'value'),
    Input('crime-type', 'value')
)
def update_charts(selected_year, selected_crime):
    # Filter data for the selected year
    dff = df_c[df_c['year'] == selected_year]

    # for the interactive barchart 
    brush = alt.selection_interval()
    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)
    stroke_width = (
    alt.when(select).then(alt.value(2, empty=False))
    .when(highlight).then(alt.value(1))
    .otherwise(alt.value(0))
    )

    # Create the staxked plot with 
    df_filtered = df_c_long[
    (df_c_long['PUMA'] == 9999) &
    (df_c_long['indicator'].isin(['high_school_w','middle_w','elementary_w'])) &
    (df_c_long['cut_name'].isin(['women', 'men']))
]
    # Define selection
    selection = alt.selection_point(fields=['cut_name'], bind='legend')
    # Create stacked bar chart
    fig_stacked = alt.Chart(df_filtered).mark_bar().encode(
    x='sum(value)',
    y='indicator',
    color='cut_name',
    opacity=alt.condition(selection, alt.value(0.9), alt.value(0.2))
    ).add_params(selection)

   # Create the scatter plot with a brush selection
    brush = alt.selection_interval()
    df_scatter = pumas_df[pumas_df['year'] == selected_year]
    fig_scatter = alt.Chart(df_scatter).mark_point().encode(
        x='total_crimes',
        y='attendance_rate_high', 
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

    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(srcDoc=fig_stacked.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'}),
        html.Iframe(srcDoc=fig_bar.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'}),
        html.Iframe(srcDoc=fig_scatter.to_html(), style={'width': '100%', 'height': '400px', 'border': '0'}),
        html.Div()
        #html.Iframe(srcDoc=crime_map.to_html(), style={'width': '100%', 'height': '600px', 'border': '0'}),
        
    )

if __name__ == '__main__':
    app.run_server(debug=True)