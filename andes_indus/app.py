from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import altair as alt
import pandas as pd
import geopandas as gpd
from figures import (create_crime_map, 
                     create_interactive_bar, 
                     create_crime_heat_map, 
                     create_stacked_chart_gender, 
                     create_stacked_chart_race,
                     create_geo_chart,
                     point_data_chart,
                     load_crimes_shp,
                     create_graph_multiple,
                     create_chicago_school_visualization,
                     create_scatter_dynamic)
from join_data import lower_colnames
from pathlib import Path

# Loading data files - Puma level
pumas_shp = lower_colnames(gpd.read_file(Path('data/shapefiles/data_pumas.shp')))
pumas_shp = pumas_shp.rename(columns={'total_cr_1' : 'total_crim_pc', 
                                      'non-viol_1' : 'non_violent_pc'})

pumas_df = pd.read_csv(Path("data/data_pumas.csv"))
df_c = pd.read_csv(Path("data/census_df.csv"))
df_c_long = pd.read_csv(Path("data/census_df_long.csv"))

# Loading maps shapefiles
pumas = gpd.read_file(Path("data/shapefiles/pumas/chicago_pumas.shp"))
neighborhood_shp = gpd.read_file(Path('data/shapefiles/data_neighborhoods.shp'))
neighborhood_shp = neighborhood_shp.rename(columns={'total_cr_1' : 'total_crim_pc', 
                                      'non-viol_1' : 'non_violent_pc'})
crimes_shp = gpd.GeoDataFrame(load_crimes_shp())

# Loading school locations
schools_df = pd.read_csv(Path("data/merged_school_data.csv"))

# Labels for graphs 
crime_labels = {
    "total_crim_pc": "Total Crime",
    "violent_pc": "Violent Crime",
    "non-violen_pc": "Non Violent Crime"
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"background": "#111188", "text": "#7FDBFF"}


# Layout with two columns
app.layout = html.Div([
    # Header section
    html.Div(
        children=[
            html.H1(
                [
                    html.Span(
                        "Understanding Crime and School Attendance in",
                        style={"color": "#000000", "font-weight": "normal"},
                    ),
                    " ",  # space
                    html.Span(
                        "Chicago",
                        style={"color": "#00bfff", "font-weight": "normal"},
                    ),
                ],
                style={
                    "font-family": "Times New Roman, serif",
                    "font-size": "36px",
                    "margin": "0",
                    "padding": "0",
                },
            ),
            html.Div(
                style={
                    "border-bottom": "1px solid #ccc",
                    "margin-top": "5px",
                    "margin-bottom": "20px",
                }
            ),
        ],
        style={"padding": "10px"},
    ),

    # Main Content: Two columns (Left: Charts & Controls, Right: Cards)
    dbc.Row([
        # Left Column (75% Width) - Graphs and Controls
        dbc.Col([
            html.Label("Select Year:"),
            dcc.Dropdown(
                options=[
                    {"label": str(year), "value": year}
                    for year in sorted(df_c["year"].unique())
                ],
                value=sorted(df_c["year"].unique())[0],
                id="dropdown-year",
            ),
            html.P(""),
            dcc.RadioItems(
                id="crime-type",
                options=[
                    {"label": "Total Crime", "value": "total_crim_pc"},
                    {"label": "Violent Crime", "value": "violent_pc"},
                    {"label": "Non Violent Crime", "value": "non-violen_pc"},
                ],
                value="total_crim_pc",
                inline=True,
            ),
            # Graphs ordered:
            html.Div(id="crime_heatmap", style={"marginBottom": "20px"}),  # Crime Heatmap
        ],
        width=9),  # Takes 75% of space

        # Right Column (25% Width) - Cards inside Light Grey Box
        dbc.Col([
            html.Div(
                style={
                    "width": "100%",
                    "backgroundColor": "#f0f0f0",  # Light grey background
                    "padding": "15px",
                    "borderRadius": "10px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "marginBottom": "110px"
                },
                children=[
                    html.Span(
                        "What are we analyzing?",
                        style={
                            "color": "#000000",
                            "font-weight": "bold",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "10px",
                        }
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(
                                    id="pumas-text",
                                    className="card-title",
                                    style={"margin": 0, "textAlign": "center"}
                                ),
                                html.I(
                                    className="fas fa-chart-bar",
                                    style={"fontSize": "1.5rem"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "justifyContent": "center"
                            }),
                            html.P("Pumas", className="card-text"),
                            dbc.Tooltip(
                                "PUMAs refer to the Public Use Microdata Areas that are non-overlapping, "
                                "statistical geographic areas that partition each state or equivalent entity "
                                "into geographic areas containing no fewer than 100,000 people each.",
                                target="pumas-text",
                                placement="top",
                            ),
                        ]),
                        style={
                            "width": "90%",
                            "textAlign": "center",
                            "borderLeft": "6px solid #37526f",
                            "marginBottom": "10px"
                        },
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(
                                    id="community-text",
                                    className="card-title",
                                    style={"margin": 0, "textAlign": "center"}
                                ),
                                html.I(
                                    className="fas fa-file-alt",
                                    style={"fontSize": "1.5rem", "textAlign": "center"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "justifyContent": "center"
                            }),
                            html.P("Community areas", className="card-text"),
                            dbc.Tooltip(
                                "Chicago community areas are distinct geographical areas that the city uses "
                                "to track social and physical characteristics. The University of Chicago "
                                "established the community areas in the 1920s with the idea that the boundaries "
                                "have roughly the same population. ",
                                target='community-text',
                                placement='top',
                            )
                        ]),
                        style={
                            "width": "90%",
                            "textAlign": "center",
                            "borderLeft": "6px solid #3b6d92",
                            "marginBottom": "10px"
                        },
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(
                                    id="school-text",
                                    className="card-title",
                                    style={"margin": 0, "textAlign": "center"}
                                ),
                                html.I(
                                    className="fas fa-calendar-check",
                                    style={"fontSize": "1.5rem"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "justifyContent": "center"
                            }),
                            html.P(id="schools-subtext", className="card-text"),
                            dbc.Tooltip(
                                "Chicago Public Schools (CPS) is the fourth-largest U.S. school district, "
                                "serving 323,251 students across 634 schools. In 2023, it had a graduation "
                                r"rate of 84%, with over 80% of students being Hispanic or Black and 63.8% "
                                "from economically disadvantaged households. Despite leading in test score"
                                " improvements, CPS faces challenges like declining enrollment and school closures. ",
                                target="school-text",
                                placement="top",
                            ),
                        ]),
                        style={
                            "width": "90%",
                            "textAlign": "center",
                            "borderLeft": "6px solid #3f88b4",
                            "marginBottom": "10px"
                        },
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(
                                    id="school-age-pop",
                                    className="card-title",
                                    style={"margin": 0, "textAlign": "center"}
                                ),
                                html.I(
                                    className="fas fa-download",
                                    style={"fontSize": "1.5rem"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "justifyContent": "center"
                            }),
                            html.P(id="school-age-pop-subtext", className="card-text"),
                        ]),
                        style={
                            "width": "90%",
                            "textAlign": "center",
                            "borderLeft": "6px solid #eb9b44",
                            "marginBottom": "10px"
                        },
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(
                                    id="crimes-text",
                                    className="card-title",
                                    style={"margin": 0, "textAlign": "center"}
                                ),
                                html.I(
                                    className="fas fa-download",
                                    style={"fontSize": "1.5rem"}
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "justifyContent": "center"
                            }),
                            html.P(id="crimes-subtext", className="card-text"),
                        ]),
                        style={
                            "width": "90%",
                            "textAlign": "center",
                            "borderLeft": "6px solid #ba9873",
                            "marginBottom": "10px"
                        },
                    ),
                ],
            ),
        ],
        width=3),  # Takes 25% of space
    ],
    style={"marginBottom": "3px"}),

    # Second big Row
    dbc.Row([
        # Left Column (8 wide)
        dbc.Col([
            html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                f"Population by Education Level, Gender and Race/Ethnicity {"year"}",
                                style={"color": "#000000", "font-weight": "normal"},
                            ),
                        ],
                        style={
                            "font-size": "20px",
                            "margin": "0",
                            "padding": "0",
                        },
                    ),
                    html.Div(
                        style={
                            "border-bottom": "1px solid #ccc",
                            "margin-top": "5px",
                            "margin-bottom": "5px",
                        }
                    ),
                ],
                       style={"padding": "10px"},
            ),
            html.Div(id="stacked-graph-container", style={"marginBottom": "5px"}),   # Stacked Chart (Gender)
            html.Div(id="stacked2-graph-container", style={"marginBottom": "150px"}), # Stacked Chart (Race)

            html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                "School Attendance Rate by Education Level and Race/Ethnicity",
                                style={"color": "#000000", "font-weight": "normal"},
                            ),
                        ],
                        style={
                            "font-size": "20px",
                            "margin": "0",
                            "padding": "0",
                        },
                    ),
                    html.Div(
                        style={
                            "border-bottom": "1px solid #ccc",
                            "margin-top": "10px",
                            "margin-bottom": "10px",
                        }
                    ),
                ],
                style={"padding": "10px"},
            ),


            html.Div(id="attendance_graph", style={"marginBottom": "0px", "alignItems": "center","justifyContent": "center"}), 

             html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                "High School Attendance Rate by location (PUMA)",
                                style={"color": "#000000", "font-weight": "normal"},
                            ),
                        ],
                        style={
                            "font-size": "20px",
                            "margin": "0",
                            "padding": "0",
                        },
                    ),
                    html.Div(
                        style={
                            "border-bottom": "1px solid #ccc",
                            "margin-top": "0px",
                            "margin-bottom": "10px",
                        }
                    ),
                ],
                style={"padding": "10px"},
            ),
                                                                                    # Attendance Graph
            html.Div(id="bar-graph-container", style={"marginBottom": "10px"}),      # Bar Chart
            html.Div(id="scatter-graph-container", style={"marginBottom": "20px"}),  # Scatter Plot

            dcc.RadioItems(
                id="level-map",
                options=[
                    {"label": "Puma level", "value": "Puma"},
                    {"label": "Neighborhood level", "value": "Neighborhood"}
                ],
                value="Puma",
                inline=True,
            ),
            html.Div(id="crime_map", style={"marginBottom": "20px"}),    # Crime Map
            html.Div(id="schools_locations", style={"marginBottom": "20px"}),  # Schools Locations
            html.Div(id='School_droput_location', style={"marginBottom": "20px"})
        ],
        width=8),

        # Right Column (4 wide)
        dbc.Col([
            # 1) First info box: "Who is impacted?"
            html.Div(
                style={
                    "width": "100%",
                    "backgroundColor": "#f0f0f0",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "marginBottom": "100px"
                },
                children=[
                    html.Span(
                        "Who is impacted?",
                        style={
                            "color": "#000000",
                            "font-weight": "bold",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "10px",
                        }
                    ),
                    html.Div(
                        [
                            "Living or studying in a violent neighborhood can influence the stress levels, "
                            "community interactions and might generate cumulative educational disadvantage ",
                            html.A(
                                "(Burdick-Will, 2017)",
                                href="https://doi.org/10.1086/691424",
                                target="_blank",
                                style={
                                    "color": "#007BFF",
                                    "textDecoration": "none",
                                    "font-weight": "bold"
                                },
                            ),
                            ". School age population might face particular risks when surounded by high crime rates."
                            "but... who is this population?",
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                            "marginBottom": "30px"
                        },
                    ),
                    html.Div(
                        [r"In 2023, in the Chicago area, there were 390 thousand school-age children (5–18 years old)."
                        r"Of those, 42% were between 5 and 12 (elementary school age), 19% were between 11 and 13 (middle school age),"
                        r"and 39% were between 14 and 18 (high school age)."],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                            "marginBottom": "30px"
                        },
                    ),
                    html.Div(
                        ["While the school-age population in Chicago is evenly distributed by sex,"
                         "two out of five of the school-age population are Hispanic,"
                         "2 out of five are African American, and only one out of five are neither Hispanic nor African American."
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                            "marginBottom": "20px"
                        },
                    ),

                ],
            ),

            # 2) Second info box: "How is Characterized School Attendance...?"
            html.Div(
                style={
                    "width": "100%",
                    "backgroundColor": "#f0f0f0",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "marginBottom": "30px"
                },
                children=[
                    html.Span(
                        "How is Characterized School Attendance in the Chicago Area?",
                        style={
                            "color": "#000000",
                            "font-weight": "bold",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "10px",
                        }
                    ),
                    html.Div(
                        [
                            "School attendance rates vary across education levels and population characteristics.  "
                            "Although attendance rates in elementary school are nearly universal, attendance in middle and high school varies significantly across race and ethnicity."
                            "For non–African American or non–Hispanic groups, high school attendance is around 80%, whereas for the Hispanic population, it does not surpass 73%. ",
                            
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                        },
                    ),
                    html.Div(
                        [ 
                            "Adolescents between the ages of 14 and 18 (high school age) often find themselves at a critical crossroads in their development, making them more"
                            "vulnerable to early school dropout and more susceptible to the effects of high crime rates in their surroundings.",
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "30px",
                            "marginBottom": "10px"
                        },
                    ),
                ],
            ),

            html.Div(
                style={
                    "width": "100%",
                    "backgroundColor": "#f0f0f0",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "marginBottom": "30px"
                },
                children=[
                    html.Span(
                        "How does attendance to highschool vary by location? ",
                        style={
                            "color": "#000000",
                            "font-weight": "bold",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "10px",
                        }
                    ),
                    html.Div(
                        [
                            "School attendance rates vary across education levels and population characteristics.  "
                            "Although attendance rates in elementary school are nearly universal, attendance in middle and high school varies significantly across race and ethnicity."
                            "For non–African American or non–Hispanic groups, high school attendance is around 80%, whereas for the Hispanic population, it does not surpass 73%. ",
                            
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                        },
                    ),
                    html.Div(
                        [ 
                            "Adolescents between the ages of 14 and 18 (high school age) often find themselves at a critical crossroads in their development, making them more"
                            "vulnerable to early school dropout and more susceptible to the effects of high crime rates in their surroundings.",
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                        },
                    ),
                ],
            ),


        ],
        width=4),
    ]),
])

      


# Callback updates the containers with iframes that embed the Altair charts.
@callback(
    Output("crime_heatmap", "children"),
    Output("stacked-graph-container", "children"),
    Output("stacked2-graph-container", "children"),
    Output("attendance_graph", "children"),
    Output("bar-graph-container", "children"),
    Output("scatter-graph-container", "children"),
    Output("crime_map", "children"),    
    Output("schools_locations", "children"),
    Output("School_droput_location", "children"),

    # for the cards
    Output("pumas-text", "children"),
    Output("community-text", "children"),
    Output("school-age-pop", "children"),
    Output("school-age-pop-subtext", 'children'),
    Output("school-text", "children"),
    Output('crimes-text', 'children'),
    Output('crimes-subtext', 'children'),
    Output('schools-subtext', 'children'),
    Input("dropdown-year", "value"),
    Input("crime-type", "value"),
    Input("level-map" , "value")
)
def update_charts(selected_year, selected_crime, selected_level):
   
   # cards
    pumas_count = len(
        df_c_long[
            (df_c_long["year"] == selected_year) 
            & (df_c_long["PUMA"] != 9999)
        ]["PUMA"].unique()
    )
    
    community_text = '77'
    
    schools_text = '634'
    schools_sub_text = f'Number of Public Schools in {selected_year}'

    school_age =  df_c[df_c['PUMA']==9999][['elementary_w',
                                            'high_school_w',
                                            'middle_w','year']].set_index('year'
                                                                          ).sum(axis=1)
    
    school_age_pop = f'{int(round(school_age[selected_year]/1000,0))}K'
    school_age_pop_text = f'School age population {selected_year}'

    n_crimes = crimes_shp.groupby(['year']).agg(count = ('count','sum')).reset_index()
    crimes_count = int(round(n_crimes[n_crimes['year'] == selected_year].iloc[0,1] / 1000, 0))
    crimes_count = f'{crimes_count}K'
    
    crimes_sub_text = f"Total crimes in {selected_year}"

    # for the interactive barchart
    brush = alt.selection_interval()
    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)
    stroke_width = (
        alt.when(select)
        .then(alt.value(2, empty=False))
        .when(highlight)
        .then(alt.value(1))
        .otherwise(alt.value(0))
    )

    indicator_map = {
        "elementary_w": "Elementary",
        "attendance_rate_elementary": "Elementary",
        "middle_w": "Middle",
        "attendance_rate_middle": "Middle",
        "attendance_rate_high": "High School",
        "high_school_w": "High School",
    }
    

   # Create the scatter plot with a brush selection
    
    brush = alt.selection_interval()
    df_scatter = pumas_df[pumas_df["year"] == selected_year]
    scatter = (
        alt.Chart(df_scatter)
        .mark_point()
        .encode(
            x=alt.X(f"{selected_crime}:Q", title=crime_labels[selected_crime]).scale(
                zero=False, domainMid=10
            ),
            y=alt.X(
                "attendance_rate_high_black:Q", title="Attendance Rate - High School"
            ).scale(zero=False, domainMid=10),
            color=alt.condition(brush, alt.value("steelblue"), alt.value("grey")),
        )
        .add_params(brush)
        .properties(title=f"Scatter Plot for Year {selected_year}")
    )

    regression_line = (
        alt.Chart(df_scatter)
        .transform_regression(selected_crime, "attendance_rate_high_black")
        .mark_line(color="red")
        .encode(x=alt.X(f"{selected_crime}:Q"), y=alt.Y("attendance_rate_high_black:Q"))
    )

    fig_scatter = (scatter + regression_line).properties(
        title=f"Scatter Plot for Year {selected_year}")

    # Create a new column 'indicator_label' using the mapping
    df_c_long["indicator_label"] = (
        df_c_long["indicator"].map(indicator_map).fillna(df_c_long["indicator"])
    )

     # Filter data for the selected year
    dff = df_c[df_c["year"] == selected_year]

    fig_stacked =  create_stacked_chart_gender(df_c_long, selected_year = selected_year)
    fig_stacked2 = create_stacked_chart_race(df_c_long, selected_year=selected_year)

        # multiple graph for attendance 
    attendance_graph = create_graph_multiple(df_c_long)


    # Create the bar chart sorted descending by attendance_rate_high
    fig_bar = create_interactive_bar(
        dff, select, stroke_width, selected_year, highlight
    )

    # Creating a map
    if selected_level == "Puma":
        crime_map = create_crime_map(pumas_shp, selected_crime, selected_year, crime_labels, selected_level, "puma_label")
    else:
        crime_map = create_crime_map(neighborhood_shp, selected_crime, selected_year, crime_labels, selected_level, "DISTITLE")

    # Creating a school map
    school_map = create_geo_chart(
        points_data=schools_df,
        geo_data=pumas,
        selected_year=2012,
        longitude_field="Longitude",  # Use the column name from your DataFrame for longitude
        latitude_field="Latitude",  # Use the column name for latitude
        tooltip_fields=[
            "School Name_x",
            "Student Count",
        ],  # Customize tooltips as needed
    )
    crime_map = crime_map + point_data_chart(
        schools_df,
        2023,
        longitude_field="Longitude",
        latitude_field="Latitude",
        tooltip_fields=["School Name_x", "DropoutRate", "Student Count"],
    )

    # Creating a heatmap
    crime_heatmap = create_crime_heat_map(
        crimes_shp, selected_crime, selected_year, crime_labels
    )

    #Creating Location and Dropout
    School_droput_location = create_chicago_school_visualization(pumas, schools_df)

    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(
            srcDoc=crime_heatmap.to_html(),
            style={"width": "100%", "height": "500px", "border": "0"},
        ),

        html.Iframe(
            srcDoc=fig_stacked.to_html(),
            style={"width": "100%", "height": "210px", "border": "5", "alignItems": "center"},
        ),
        html.Iframe(
            srcDoc=fig_stacked2.to_html(),
            style={"width": "100%", "height": "230", "border": "5", "alignItems": "center"},
        ),

        html.Iframe(
            srcDoc=attendance_graph.to_html(),
            style={"width": "100%", "height": "600px", "border": "0", "justifyContent": "center" },
        ),

        html.Iframe(
            srcDoc=fig_bar.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=fig_scatter.to_html(),
            style={"width": "100%", "height": "400px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=crime_map.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=school_map.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=School_droput_location.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
        # for the cards
        str(pumas_count),
        community_text,
        school_age_pop,
        school_age_pop_text,
        schools_text,
        crimes_count,
        crimes_sub_text,
        schools_sub_text
    )


if __name__ == "__main__":
    app.run_server(debug=True)
