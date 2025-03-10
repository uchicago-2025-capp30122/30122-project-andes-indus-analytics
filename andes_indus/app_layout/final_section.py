from dash import html
import dash_bootstrap_components as dbc
from pathlib import Path
from .app_utils import CHICAGO_COLORS

# Team member information (names, photos, GitHub links)
team_members = [
    {
        "name": "Angela Lopez",
        "photo": "https://avatars.githubusercontent.com/u/53953448?v=4",
        "github": "https://github.com/AngelaLop"
    },
    {
        "name": "Shahzaib Jamali",
        "photo": "https://avatars.githubusercontent.com/u/175346564?v=4",
        "github": "https://github.com/Shahzaib-Jamali"
    },
    {
        "name": "César Núñez",
        "photo": "https://avatars.githubusercontent.com/u/75745356?v=4",
        "github": "https://github.com/cesarnunezh"
    }
]

# GitHub logo path
github_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/1024px-Octicons-mark-github.svg.png"

# Team logo
logo_path = "../images/andes-indus.png"

# Final Section
def gen_final_section():
    final_section = dbc.Row(
        html.Div(
            children=[
                # Team Logo
                html.Div(
                children=[
                    html.H3("Team members", style={"fontWeight": "bold", "textAlign": "center", "marginBottom": "20px"})
                ]
                ),

                # Team Members
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.Img(src=member["photo"], style={"width": "100px", "height": "100px", "borderRadius": "50%"}),
                                html.H5(member["name"], style={"textAlign": "center"}),
                                html.A(
                                    children=[
                                        html.Img(src=github_logo, style={"width": "20px", "height": "20px", "marginRight": "5px"}),
                                        "GitHub"
                                    ],
                                    href=member["github"], target="_blank", style={"color": "#ffffff", "textDecoration": "none", "display": "flex", "alignItems": "center"}
                                )
                            ],
                            width={"size": 3, "offset": 1},  # 4 columns each, evenly distributed
                            style={"textAlign": "center", "padding": "10px"}
                        ) for member in team_members
                    ],
                    justify="between"  # Distribute members evenly across the row
                )
            ],
            style={
                "width": "100%",
                "backgroundColor": CHICAGO_COLORS['sky'],
                "padding": "15px",
                "borderRadius": "8px",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "marginBottom": "30px"
            }
        )
    )
    return final_section