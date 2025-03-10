from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import altair as alt
from app_layout.figures import (create_crime_map,
                                create_interactive_bar,
                                create_crime_heat_map, 
                                create_stacked_chart_gender, 
                                create_stacked_chart_race,
                                point_data_chart,
                                create_graph_multiple,
                                create_chicago_school_visualization,
                                create_scatter_dynamic)
from app_layout.final_section import gen_final_section
from app_layout.app_utils import crime_labels
from app_layout.header import gen_header
from app_layout.load_data import (pumas_shp, pumas_df_long, df_c, df_c_long, 
                                  schools_df, pumas, neighborhood_shp, crimes_shp)
from andes_indus.app_layout.main_content import gen_first_row

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout with two columns
app.layout = html.Div([
    # Header section
    gen_header(),

    gen_first_row(),

    # Second big Row
    dbc.Row([
        # Left Column (8 wide)
        dbc.Col([
            html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                f"Population by Education Level, Gender and Race/Ethnicity",
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
                       style={"padding": "10px",
                              "alignItems": "center",
                              "justifyContent": "center"},
            ),
                dbc.Row(  
                    dbc.Col(
                        html.Div(id="stacked-graph-container"),
                        width={"offset": 2},
                    ),
                    style={"marginBottom": "5px", "justifyContent": "center"}
                ),

                # Second Graph (Race)
                dbc.Row(  
                    dbc.Col(
                        html.Div(id="stacked2-graph-container"),
                        width={"offset": 2},
                    ),
                    style={"marginBottom": "100px", "justifyContent": "center"}
                ),

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
                            "margin-bottom": "5px",
                        }
                    ),
                ],
                style={"padding": "10px"},
            ),
            dbc.Row(  
                    dbc.Col(
                        html.Div(id="attendance_graph"),
                        width={"offset": 2},
                    ),
                    style={"marginBottom": "0px", "alignItems": "center","justifyContent": "center"}
                ),
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
                            "marginBottom": "30px",
                            "textAlign": "justify"
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
                            "marginBottom": "30px",
                            "textAlign": "justify"
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
                            "marginBottom": "20px",
                            "textAlign": "justify"
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
                    "marginBottom": "5px"
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
                            "textAlign": "justify"
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
                            "marginBottom": "5px"
                        },
                    ),
                ],
            ),


        ],
        width=4),
    ]),

    dbc.Row([
        # Left Column (8 wide)
        dbc.Col([
             html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                "High School Attendance Rate by location",
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
            dbc.Row(  
                    dbc.Col(
                        html.Div(id="bar-graph-container"),
                        width={"offset": 2},
                    ),
                    style={"marginBottom": "0px", "alignItems": "center","justifyContent": "center"}
                ),
            
        ],
        width=8),

        # Right Column (4 wide)
        dbc.Col([

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
                        "How does attendance to high school vary by location? ",
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
                            "When exploring high school attendance rates by Public Use Microdata Areas (PUMAs) "
                            "throughout Chicago, at first glance, certain PUMAs—particularly those in the northern or central parts of "
                            "the city—are clustered near the top, reporting attendance rates above 80%. Meanwhile, areas toward the bottom often sit closer to 60%."

                            "As you move through the data, imagine the real‐life implications for students in each PUMA—students in higher‐performing neighborhoods "
                            "may have easier access to safe transportation or well‐equipped school facilities, while those in lower‐attending areas may face additional hurdles,"
                            "from safety concerns to family obligations.",
                        ],
                        style={
                            "color": "#000000",
                            "font-weight": "normal",
                            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                            "padding": "3px",
                            "textAlign": "justify"
                        },
                    ),
                    html.Div(
                        [ 

                            "....can be crime related to this patterns?",
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

### new row - unique 

    dbc.Row([
            # Left Column
        dbc.Col(
                [
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
                                    "How does early school dropout rates vary by location? ",
                                    style={
                                        "color": "#000000",
                                        "font-weight": "bold",
                                        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                                        "padding": "10px",
                                    }
                             ),
                             html.Div(
                                [
                                    "Chicago is traditionally divided into distinct northern and southern regions, each "
                                    "characterized by unique socioeconomic dynamics that have been extensively examined "
                                    "in the literature ",
                                    html.A("(Burdick‑Will, 2016; ",
                                           href="https://doi.org/10.1093/sf/sow041",
                                           target="_blank",
                                           style={
                                               "color": "#007BFF",
                                               "textDecoration": "none",
                                               "font-weight": "bold"
                                               },
                                               ),
                                    html.A("Jankov & Caref, 2017).",
                                           href="https://doi.org/10.14507/epaa.25.2631",
                                           target="_blank",
                                           style={
                                               "color": "#007BFF",
                                               "textDecoration": "none",
                                               "font-weight": "bold"
                                               },
                                               ),
                                    "This interactive graph invites exploration into whether differences in dropout rates "
                                    "emerge as one transitions from the south side to the north. Initial observations of "
                                    "the density plot suggest that dropout rates in the northern region tend to cluster "
                                    "within a narrow range (approximately 0–10%), while in the southern region the distribution "
                                    "appears more varied. Furthermore, the graph investigates the spatial distribution of "
                                    "schools in these areas, raising questions about whether schools are dispersed evenly "
                                    "or concentrated in particular locations. These visual insights resonate with research "
                                    "findings indicating that factors such as neighborhood violence, resource allocation, "
                                    "and school segregation may influence educational outcomes differently across Chicago’s "
                                    "north and south ",
                                    html.A("(Hirschfield, 2009; ",
                                           href="https://doi.org/10.1177/003804070908200404",
                                           target="_blank",
                                           style={
                                               "color": "#007BFF",
                                               "textDecoration": "none",
                                               "font-weight": "bold"
                                               },
                                               ),
                                    html.A("Phillippo & Griffin, 2016). ",
                                           href="https://doi.org/10.1007/s11256-016-0373-x",
                                           target="_blank",
                                           style={
                                               "color": "#007BFF",
                                               "textDecoration": "none",
                                               "font-weight": "bold"
                                               },
                                               )
                                ],
                                    style={
                                        "color": "#000000",
                                        "font-weight": "normal",
                                        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                                        "padding": "3px",
                                        "textAlign": "center"
                                    },
                             ),
                        ],            
                    ),
                html.Div(
                        children=[
                            html.H1(
                                [
                                    html.Span(
                                        "High School Dropout Rates by location",
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
                                    "width": "40%"
                                }
                            ),
                        ],
                        style={"padding": "10px"},
                    ),
                    # Schools locations
                dbc.Row(
                    dbc.Col(
                        html.Div(id="School_droput_location"),
                        width={"offset": 1},
                        ),
                        style={"marginBottom": "0px", "alignItems": "center","justifyContent": "center"}
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
                                    "How does school attendance / dropouts correlate with crime? ",
                                    style={
                                        "color": "#000000",
                                        "font-weight": "bold",
                                        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                                        "padding": "10px",
                                    }
                             ),
                             html.Div(
                                [
                                    "From a high‐level perspective, this map of Chicago, organized by PUMAs, displays two key variables: "
                                    "the Crime Rate, shown through choropleth shading where darker shades indicate higher total crime "
                                    "occurrences per 1,000 inhabitants, and the Dropout Rate, represented by bubble size where larger "
                                    "circles reflect higher dropout percentages. A clear pattern emerges in areas with high crime and "
                                    "high dropout rates. Specifically, PUMAs on the city’s South Side and parts of the West Side are "
                                    "shaded in darker tones, signaling elevated crime rates. In these same areas, the map often features "
                                    "some of the largest bubbles, indicating higher dropout rates. In contrast, the northern portions of "
                                    "the city generally display lighter shading, signifying lower crime occurrences. Correspondingly, "
                                    "bubble sizes in these neighborhoods tend to be smaller, pointing to relatively lower dropout rates. \n "
                                    "School attendance and crime rates in Chicago exhibit nuanced patterns by education level and ethnicity. "
                                    "The scatter plots below illustrate the varying relationships between attendance rates and crime rates "
                                    "across all PUMAs. Throughout the entire period of analysis, middle school attendance rates show negative "
                                    "associations with both violent and non-violent crime rates for African Americans. In other words, in "
                                    "geographic areas where crime rates per 1,000 inhabitants are higher, attendance rates for African American "
                                    "students tend to be lower. This pattern is also observed in the relationship between high school attendance "
                                    "rates for African American students and violent crime rates."                           
                                ],
                                    style={
                                        "color": "#000000",
                                        "font-weight": "normal",
                                        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                                        "padding": "3px",
                                        "textAlign": "center"
                                    },
                             ),        
                        ],            
                    ),               
                ],
                width=12
                
            ),
        ]),

## new row two columns for correlations

    dbc.Row([
        # Left Column (8 wide)
        dbc.Col([
             html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                "High School Attendance Rate and crime by location",
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
                                dcc.RadioItems(
                                id="level-map",
                                options=[
                                    {"label": "Puma level", "value": "Puma"},
                                    {"label": "Neighborhood level", "value": "Neighborhood"},
                                ],
                                value="Puma",
                                inline=True,
                            ),

                            # Crime Map
                            html.Div(id="crime_map", style={"marginBottom": "20px"}),  

            
        ],
        width=6),

        # Right Column (4 wide)
        dbc.Col([

               html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                "High School Attendance Rate and crime by ethnicity",
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
                    # Scatter Plot Chart
                    dcc.Dropdown(
                        options=[
                            {"label": 'Elementary School', 'value': 'elementary'},
                            {"label": 'Middle School', 'value': 'middle'},
                            {"label": 'High School', 'value': 'high'}
                        ],
                        value='high',
                        id="dropdown-level",
                    ),
                    html.Div(id="scatter-graph-container", style={"marginBottom": "20px"}),
        ],
        width=6),
    ]),
    
    # Final section
    gen_final_section()

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
    Input("year-slider", "value"),
    Input("crime-type", "value"),
    Input("level-map" , "value"),
    Input("dropdown-level", 'value'),
)
def update_charts(selected_year, selected_crime, selected_level, level_educ):
   
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
    level_dic = {'middle': 'Middle',
                 'high' : 'High School',
                 'elementary' : 'Elementary'}
    race_dic = {'black': 'Black',
                'hispanic' : 'Hispanic',
                'non_black_non_hispanic' : 'Non Black, Non Hispanic'}

    fig_scatter = create_scatter_dynamic(pumas_df_long, selected_year, selected_crime, crime_labels, level_educ, level_dic)

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
    School_droput_location = create_chicago_school_visualization(pumas, schools_df, selected_year)

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
            style={"width": "100%", "height": "210px", "border": "5", "alignItems": "center"},
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
