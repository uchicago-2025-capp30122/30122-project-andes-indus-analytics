from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import altair as alt
import pandas as pd
import geopandas as gpd
from figures import create_crime_map, create_interactive_bar, create_crime_heat_map, create_stacked_chart_gender, create_stacked_chart_race
from join_data import lower_colnames
import pathlib
from figures import create_crime_map, create_geo_chart, point_data_chart
from crime_utils import load_crimes_shp

# Load data
pumas_shp = lower_colnames(gpd.read_file('data/shapefiles/data_pumas.shp'))
neighborhood_shp = gpd.read_file('data/shapefiles/data_neighborhoods.shp')
df_c = pd.read_csv("data/census_df.csv")
df_c_long = pd.read_csv("data/census_df_long.csv")
crimes_shp = gpd.GeoDataFrame(load_crimes_shp())

# Create the crime map by puma and neighborhood

for var in ["total_crim", "violent", "non-violen"]:
    pumas_shp[f"{var}_pc"] = pumas_shp[f"{var}"] / pumas_shp["pwgtp"] * 1000

pumas_df = pd.read_csv("data/data_pumas.csv")
pumas_df = pumas_df.rename(
    columns={
        "total_crimes": "total_crim",
        "Violent": "violent",
        "Non-violent": "non-violen",
    }
)
for var in ["total_crim", "violent", "non-violen"]:
    pumas_df[f"{var}_pc"] = pumas_df[f"{var}"] / pumas_df["pwgtp"] * 1000

pumas_path = pathlib.Path("data/shapefiles/pumas/chicago_pumas.shp")
pumas = gpd.read_file(pumas_path)


schools_csv_path = pathlib.Path(
    "data/merged_school_data.csv"
)  # update with your CSV path
schools_df = pd.read_csv(schools_csv_path)


df_c = pd.read_csv("data/census_df.csv")
df_c_long = pd.read_csv("data/census_df_long.csv")
df_e = pd.read_csv("data/merged_school_data.csv")

crime_labels = {
    "total_crim_pc": "Total Crime",
    "violent_pc": "Violent Crime",
    "non-violen_pc": "Non Violent Crime",
    "Violent": "Violent Crime",
    "Non-violent": "Non Violent Crime",
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"background": "#111188", "text": "#7FDBFF"}


# Layout with two columns
app.layout = html.Div(
    [
        # "Header" section
        html.Div(
            children=[
                html.H1(
                    [
                        # "Michelin Guide to France" in black
                        html.Span(
                            "Understanding School Attendance and Crime in",
                            style={"color": "#000000", "font-weight": "normal"},
                        ),
                        " ",  # space
                        # "chicago in blue"
                        html.Span(
                            "Chicago",
                            style={"color": "#00bfff", "font-weight": "normal"},
                        ),
                    ],
                    style={
                        "font-family": "Times New Roman, serif",
                        "font-size": "36px",
                        "margin": "0",  # remove default H1 margin
                        "padding": "0",
                    },
                ),
                # A thin border line below the header
                html.Div(
                    style={
                        "border-bottom": "1px solid #ccc",
                        "margin-top": "5px",
                        "margin-bottom": "20px",
                    }
                ),
            ],
            style={
                "padding": "10px"  # some padding around the "header"
            },
        ),
        dbc.Row(
            [
                # Card 1
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "18",
                                            className="card-title",
                                            style={"margin": 0},
                                        ),
                                        html.I(
                                            className="fas fa-chart-bar",
                                            style={"fontSize": "1.8rem"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                        "justifyContent": "center",
                                    },
                                ),
                                html.P(
                                    "Pumas",
                                    className="card-text",
                                    style={"marginTop": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "textAlign": "center",
                            "borderLeft": "10px solid #37526f",
                        },
                    ),
                    md=2,
                ),
                # Card 2
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "178",
                                            className="card-title",
                                            style={"margin": 0},
                                        ),
                                        html.I(
                                            className="fas fa-file-alt",
                                            style={"fontSize": "1.8rem"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                        "justifyContent": "center",
                                    },
                                ),
                                html.P(
                                    "Neighborhoods",
                                    className="card-text",
                                    style={"marginTop": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "textAlign": "center",
                            "borderLeft": "10px solid #3b6d92",
                        },
                    ),
                    md=2,
                ),
                # Card 3
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "644",
                                            className="card-title",
                                            style={"margin": 0},
                                        ),
                                        html.I(
                                            className="fas fa-calendar-check",
                                            style={"fontSize": "1.8rem"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                        "justifyContent": "center",
                                    },
                                ),
                                html.P(
                                    "Public Schools in 2023",
                                    className="card-text",
                                    style={"marginTop": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "textAlign": "center",
                            "borderLeft": "10px solid #3f88b4",
                        },
                    ),
                    md=2,
                ),
                # Card 4
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "391K",
                                            className="card-title",
                                            style={"margin": 0},
                                        ),
                                        html.I(
                                            className="fas fa-download",
                                            style={"fontSize": "1.8rem"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                        "justifyContent": "center",
                                    },
                                ),
                                html.P(
                                    "School-age population",
                                    className="card-text",
                                    style={"marginTop": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "textAlign": "center",
                            "borderLeft": "10px solid #eb9b44",
                        },
                    ),
                    md=2,
                ),
                # Card 5
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "260K",
                                            className="card-title",
                                            style={"margin": 0},
                                        ),
                                        html.I(
                                            className="fas fa-download",
                                            style={"fontSize": "1.8rem"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                        "justifyContent": "center",
                                    },
                                ),
                                html.P(
                                    "Total crimes in 2023",
                                    className="card-text",
                                    style={"marginTop": "10px"},
                                ),
                            ]
                        ),
                        style={
                            "textAlign": "center",
                            "borderLeft": "10px solid #ba9873",
                        },
                    ),
                    md=2,
                ),
            ],
            justify="center",  # horizontally center the row
            style={"marginBottom": "10px", "fontFamily": "Times New Roman, serif"},
        ),
        html.Div(
            style={"display": "flex", "fontFamily": "Times New Roman, serif"},
            children=[
                # Left column: text and controls
                html.Div(
                    style={"width": "50%", "padding": "20px"},
                    children=[
                        html.P("This is a paragraph with background info."),
                        html.Label("Select Year:"),
                        dcc.Dropdown(
                            options=[
                                {"label": str(year), "value": year}
                                for year in sorted(df_c["year"].unique())
                            ],
                            value=sorted(df_c["year"].unique())[0],
                            id="dropdown-year",
                        ),
                        html.P(
                            "Story or problem we are tackling. "
                            "Use this space for any narrative or instructions."
                        ),
                    ],
                ),
                # Right column: the graphs
                html.Div(
                    style={"width": "50%", "padding": "20px"},
                    children=[
                        html.Div(id="stacked-graph-container"),
                        html.Div(id="stacked2-graph-container"),
                        html.Div(id="scatter-graph-container"),
                        html.Div(id="bar-graph-container"),
                        html.Div(id="crime_map"),
                        html.Div(id="schools_locations"),
                        html.Div(id="crime_heatmap"),
                    ],
                ),
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
            ],
        ),
    ]
)


# Callback updates the containers with iframes that embed the Altair charts.
@callback(
    Output("stacked-graph-container", "children"),
    Output("stacked2-graph-container", "children"),
    Output("scatter-graph-container", "children"),
    Output("bar-graph-container", "children"),
    Output("crime_map", "children"),
    Output("schools_locations", "children"),
    Output("crime_heatmap", "children"),
    Input("dropdown-year", "value"),
    Input("crime-type", "value"),
)
def update_charts(selected_year, selected_crime):
    # Filter data for the selected year
    dff = df_c[df_c["year"] == selected_year]

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
        "middle_w": "Middle",
        "high_school_w": "High School",
    }
    
    # Create a new column 'indicator_label' using the mapping
    df_c_long["indicator_label"] = (
        df_c_long["indicator"].map(indicator_map).fillna(df_c_long["indicator"])
    )

    

    
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
    
    fig_stacked = create_stacked_chart_gender(df_c_long)
    fig_stacked2 = create_stacked_chart_race(df_c_long)

    # Create the bar chart sorted descending by attendance_rate_high
    fig_bar = create_interactive_bar(
        dff, select, stroke_width, selected_year, highlight
    )

    # Creating a map
    crime_map = create_crime_map(pumas_shp, selected_crime, selected_year, crime_labels)

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
    helper_dict = {
        "violent_pc": "Violent",
        "non-violen_pc": "Non-violent",
        "total_crim_pc": "total_crim_pc",
    }
    crime_heatmap = create_crime_heat_map(
        crimes_shp, helper_dict[selected_crime], selected_year, crime_labels
    )

    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(
            srcDoc=fig_stacked.to_html(),
            style={"width": "100%", "height": "140px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=fig_stacked2.to_html(),
            style={"width": "100%", "height": "140px", "border": "0"},
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
            srcDoc=crime_heatmap.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=school_map.to_html(),
            style={"width": "100%", "height": "600px", "border": "0"},
        ),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
