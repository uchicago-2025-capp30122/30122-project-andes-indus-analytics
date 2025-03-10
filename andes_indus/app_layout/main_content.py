from dash import html
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
    pass

def gen_third_row():
    pass

def gen_fourth_row():
    pass

def gen_fifth_row():
    pass

def gen_sixth_row():
    pass