from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import altair as alt
from andes_indus.app_layout.figures import (
    create_crime_map,
    create_interactive_bar,
    create_crime_heat_map,
    create_stacked_chart_gender,
    create_stacked_chart_race,
    point_data_chart,
    create_graph_multiple,
    create_chicago_school_visualization,
    create_scatter_dynamic,
)
from andes_indus.app_layout.final_section import gen_final_section
from andes_indus.app_layout.app_utils import crime_labels
from andes_indus.app_layout.header import gen_header
from andes_indus.app_layout.load_data import (
    pumas_shp,
    pumas_df_long,
    df_c,
    df_c_long,
    schools_df,
    pumas,
    neighborhood_shp,
    crimes_shp,
)
from andes_indus.app_layout.main_content import (
    gen_first_row,
    gen_second_row,
    gen_third_row,
    gen_fourth_row,
    gen_fifth_row,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout with two columns
app.layout = html.Div(
    [
        gen_header(),
        gen_first_row(),
        gen_second_row(),
        gen_third_row(),
        gen_fourth_row(),
        gen_fifth_row(),
        gen_final_section(),
    ]
)


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
    Output("school-age-pop-subtext", "children"),
    Output("school-text", "children"),
    Output("crimes-text", "children"),
    Output("crimes-subtext", "children"),
    Output("schools-subtext", "children"),
    Input("year-slider", "value"),
    Input("crime-type", "value"),
    Input("level-map", "value"),
    Input("dropdown-level", "value"),
)
def update_charts(selected_year, selected_crime, selected_level, level_educ):
    # cards
    pumas_count = len(
        df_c_long[(df_c_long["year"] == selected_year) & (df_c_long["PUMA"] != 9999)][
            "PUMA"
        ].unique()
    )

    community_text = "77"

    schools_text = "634"
    schools_sub_text = f"Number of Public Schools in {selected_year}"

    school_age = (
        df_c[df_c["PUMA"] == 9999][
            ["elementary_w", "high_school_w", "middle_w", "year"]
        ]
        .set_index("year")
        .sum(axis=1)
    )

    school_age_pop = f"{int(round(school_age[selected_year] / 1000, 0))}K"
    school_age_pop_text = f"School age population {selected_year}"

    n_crimes = crimes_shp.groupby(["year"]).agg(count=("count", "sum")).reset_index()
    crimes_count = int(
        round(n_crimes[n_crimes["year"] == selected_year].iloc[0, 1] / 1000, 0)
    )
    crimes_count = f"{crimes_count}K"

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
    level_dic = {"middle": "Middle", "high": "High School", "elementary": "Elementary"}
    race_dic = {
        "black": "Black",
        "hispanic": "Hispanic",
        "non_black_non_hispanic": "Non Black, Non Hispanic",
    }

    fig_scatter = create_scatter_dynamic(
        pumas_df_long,
        selected_year,
        selected_crime,
        crime_labels,
        level_educ,
        level_dic,
    )

    # Create a new column 'indicator_label' using the mapping
    df_c_long["indicator_label"] = (
        df_c_long["indicator"].map(indicator_map).fillna(df_c_long["indicator"])
    )

    # Filter data for the selected year
    dff = df_c[df_c["year"] == selected_year]

    fig_stacked = create_stacked_chart_gender(df_c_long, selected_year=selected_year)
    fig_stacked2 = create_stacked_chart_race(df_c_long, selected_year=selected_year)

    # multiple graph for attendance
    attendance_graph = create_graph_multiple(df_c_long)

    # Create the bar chart sorted descending by attendance_rate_high
    fig_bar = create_interactive_bar(
        dff, select, stroke_width, selected_year, highlight
    )

    # Creating a map
    if selected_level == "Puma":
        crime_map = create_crime_map(
            pumas_shp,
            selected_crime,
            selected_year,
            crime_labels,
            selected_level,
            "puma_label",
        )
    else:
        crime_map = create_crime_map(
            neighborhood_shp,
            selected_crime,
            selected_year,
            crime_labels,
            selected_level,
            "DISTITLE",
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

    # Creating Location and Dropout
    School_droput_location = create_chicago_school_visualization(
        pumas, schools_df, selected_year
    )

    # Return iframes that embed the Altair charts via their HTML representation
    return (
        html.Iframe(
            srcDoc=crime_heatmap.to_html(),
            style={"width": "100%", "height": "500px", "border": "0"},
        ),
        html.Iframe(
            srcDoc=fig_stacked.to_html(),
            style={
                "width": "100%",
                "height": "210px",
                "border": "5",
                "alignItems": "center",
            },
        ),
        html.Iframe(
            srcDoc=fig_stacked2.to_html(),
            style={
                "width": "100%",
                "height": "210px",
                "border": "5",
                "alignItems": "center",
            },
        ),
        html.Iframe(
            srcDoc=attendance_graph.to_html(),
            style={
                "width": "100%",
                "height": "600px",
                "border": "0",
                "justifyContent": "center",
            },
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
        schools_sub_text,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
