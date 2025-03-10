from dash import html, dcc
import dash_bootstrap_components as dbc
from .app_utils import CHICAGO_COLORS


def gen_header():
    # Header section with controls in one row
    header = html.Div(
        children=[
            dbc.Row(
                [
                    # Title Column (Takes 5 out of 12 columns)
                    dbc.Col(
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
                                "font-size": "32px",
                                "margin": "0",
                                "padding": "0",
                                "white-space": "nowrap",
                            },
                        ),
                        width=8,  # Takes 5 columns
                    ),
                    # Year Slider Column (Takes 4 out of 12 columns)
                    dbc.Col(
                        html.Div(
                            [
                                html.Label(
                                    "Select Year:",
                                    style={
                                        "font-weight": "bold",
                                        "font-size": "12px",
                                        "color": "#666666",
                                    },
                                ),
                                dcc.Slider(
                                    id="year-slider",
                                    min=2013,
                                    max=2023,
                                    step=5,
                                    marks={
                                        year: str(year) for year in range(2013, 2024, 5)
                                    },  # Includes 2023 label
                                    value=2023,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },  # Always show tooltip
                                    included=False,  # Ensures marks are independent of step values
                                    updatemode="drag",  # Update as user drags
                                ),
                            ],
                            style={
                                "width": "100%",
                                "textAlign": "right",
                            },  # Ensures right alignment
                        ),
                        width=2,  # Takes 3 columns
                    ),
                    # Crime Type Selector Column (Takes 3 out of 12 columns)
                    dbc.Col(
                        html.Div(
                            [
                                html.Label(
                                    "Select Crime Type:",
                                    style={
                                        "font-weight": "bold",
                                        "font-size": "12px",
                                        "color": "#666666",
                                    },
                                ),
                                dcc.RadioItems(
                                    id="crime-type",
                                    options=[
                                        {"label": "Total", "value": "total_crim_pc"},
                                        {"label": "Violent", "value": "violent_pc"},
                                        {
                                            "label": "Non-Violent",
                                            "value": "non-violen_pc",
                                        },
                                    ],
                                    value="total_crim_pc",
                                    inline=True,
                                    style={
                                        "color": "#888888",  # Lighter grey for text
                                        "font-size": "12px",
                                    },
                                ),
                            ],
                            style={
                                "width": "100%",
                                "textAlign": "right",
                            },  # Ensures right alignment
                        ),
                        width=2,
                        # Takes 3 columns
                    ),
                ],
                align="center",  # Align all items vertically in the center
                justify="end",  # Align to the right of the row
            ),
            html.Div(
                style={
                    "border-bottom": "1px solid #ccc",
                    "margin-top": "5px",
                    "margin-bottom": "20px",
                }
            ),
        ],
        style={
            "padding": "10px",
            "position": "sticky",  # Make the header sticky
            "top": 0,
            "zIndex": 9999,
            "backgroundColor": CHICAGO_COLORS["white"],
        },
    )

    return header
