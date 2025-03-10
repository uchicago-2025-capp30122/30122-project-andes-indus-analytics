from dash import html, dcc
import dash_bootstrap_components as dbc
from .app_utils import CHICAGO_COLORS

def gen_first_row():

    # Main Content: Two columns (Left: Charts & Controls, Right: Cards)
    first_row = dbc.Row([
        # Left Column (75% Width) - Graphs and Controls
        dbc.Col(
            [
  
        html.Div(
                children=[
                    html.H1(
                        [
                            html.Span(
                                f"Spatial Distribution of Crimes in Chicago",
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
                    html.Div(
                        [
                            "The Chicago Area has long been recognized for its high crime rates compared to other major U.S. cities, "
                            "with persistent challenges related to gun violence, gang activity, and socio-economic disparities. "
                            "While crime rates fluctuate year to year, Chicago consistently ranks among the cities with the highest "
                            "violent crime rates, particularly in specific neighborhoods on the South and West sides." ,
                            ],
                            style={
                                "color": "#000000",
                                "font-weight": "normal",
                                "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
                                "padding": "3px",
                                "marginBottom": "10px"
                            },
                    ),
                ],
                       style={"padding": "10px"},
            ),
        html.Div(id="crime_heatmap", style={"marginBottom": "0 px"}),    
        # Info Box - "Who is impacted?"
        html.Div(
            style={
                "width": "100%",
                "backgroundColor": CHICAGO_COLORS["white"],
                "padding": "0px",
                "borderRadius": "8px",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "left",
                "marginBottom": "10px"
            },
        ),
    ],
    width=9  # Moves width property to the correct place
    ),


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
                                placement='bottom',
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
                                "from economically disadvantaged households. ",
                                target="school-text",
                                placement="bottom",
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
                            dbc.Tooltip(
                                "Refers to the theoretical school age population aged between 5–18. ",
                                target="school-age-pop",
                                placement="bottom",
                            ),
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
                            dbc.Tooltip(
                                "The Chicago Police Department maintains a comprehensive database of reported "
                                "crimes across the city. For this analysis, we focused on data from the years "
                                "2013, 2018, and 2023, totaling nearly one million records. To categorize each "
                                "incident as either violent or non-violent crime, we followed the FBI's Uniform "
                                "Crime Reporting (UCR) Program guidelines. According to the UCR, violent crimes "
                                "include four primary offenses: murder, forcible rape, robbery, and aggravated assault. ",
                                target="crimes-text",
                                placement="bottom",
                            ),
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
    style={"marginBottom": "3px"})

    return first_row

def gen_second_row():
    second_row = dbc.Row([
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
    ])
    return second_row

def gen_third_row():
    third_row = dbc.Row([
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
    ])

    return third_row

def gen_fourth_row():
    fourt_row = dbc.Row([
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
        ])
    return fourt_row

def gen_fifth_row():
    fifth_row = dbc.Row([
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
    ])
    return fifth_row
