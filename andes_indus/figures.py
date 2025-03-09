import altair as alt
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .api_get import get_google_drive_files

def create_crime_map(
    gdf: gpd.GeoDataFrame, selected_crime: str, 
    selected_year: int, label_dict: dict, selected_level:str, level_label:str) -> alt.Chart:
    gdf = gdf[gdf["year"] == selected_year].copy()
    map = (
        alt.Chart(gdf)
        .mark_geoshape(stroke="white", strokeWidth=0.5)
        .encode(
            color=alt.Color(selected_crime, type="quantitative", title="Crime Rate"),
            tooltip=[
                alt.Tooltip(level_label, title=selected_level),
                alt.Tooltip("year", title="Year"),
                alt.Tooltip(selected_crime, title="Crime per 1000 hab."),
            ],
        )
        .project(type="mercator")
        .properties(
            width=500,
            height=500,
            title=f"{label_dict[selected_crime]} ocurrances per 1000 hab. for Year {selected_year} by {selected_level}",
        )
    )

    return map


def create_geo_chart(
    points_data,
    geo_data,
    selected_year,
    width=500,
    height=500,
    longitude_field="longitude",
    latitude_field="latitude",
    tooltip_fields=None,
    projection="mercator",
):
    if tooltip_fields is None:
        tooltip_fields = [longitude_field, latitude_field]

    points_data = points_data[points_data["Year"] == selected_year].copy()
    points_data = points_data[points_data["Latitude"].notna()]

    background_chart = (
        alt.Chart(geo_data)
        .mark_geoshape(fill="None", stroke="None")
        .properties(width=width, height=height)
        .project(projection)
    )

    points_chart = (
        alt.Chart(points_data)
        .mark_circle(size=30, color="gray")
        .encode(
            longitude=f"{longitude_field}:Q",
            latitude=f"{latitude_field}:Q",
            tooltip=tooltip_fields,
        )
    )

    final_chart = background_chart + points_chart
    return final_chart


def point_data_chart(
    points_data,
    selected_year,
    longitude_field="longitude",
    latitude_field="latitude",
    tooltip_fields=None,
):
    # Filter data for the selected year and remove NaN latitude values
    points_data = points_data[points_data["Year"] == selected_year].copy()
    points_data = points_data[points_data["Latitude"].notna()]

    # Create Altair chart
    points_chart = (
        alt.Chart(points_data)
        .mark_circle(color="gray")
        .encode(
            longitude=alt.X(f"{longitude_field}:Q"),
            latitude=alt.Y(f"{latitude_field}:Q"),
            size=alt.Size("DropoutRate:Q", title="DropoutRate"),
            tooltip=tooltip_fields,
        )
    )

    return points_chart


def create_interactive_bar(dff, select, stroke_width, selected_year, highlight):
    # Create the bar chart sorted descending by attendance_rate_high
    bar = (
        alt.Chart(dff)
        .mark_bar(fill="#0099cc", stroke="black", cursor="pointer")
        .encode(
            x=alt.X(
                "puma_label",
                axis=alt.Axis(title="PUMA name"),
                sort=alt.EncodingSortField(
                    field="attendance_rate_high", op="sum", order="descending"
                ),
            ),
            y=alt.Y(
                "attendance_rate_high",
                axis=alt.Axis(title="Attendance rate - high school"),
            ),
            fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
            strokeWidth=stroke_width,
        )
        .properties(
            title=f"Attendance Rate for Year {selected_year} - High School (self reported)"
        )
        .add_params(select, highlight)
    )

    return bar


def create_crime_heat_map(
    gdf: gpd.GeoDataFrame, selected_crime: str, selected_year: int, label_dict: dict
):
    gdf = gdf[(gdf["year"] == selected_year)].copy()

    if selected_crime != "Non-violent" and selected_crime != "Violent":
        gdf = (
            gdf.groupby(["year", "block", "latitude", "longitude"])
            .agg(count=("count", "sum"))
            .reset_index()
        )
    else:
        gdf = gdf[(gdf["crime_type"] == selected_crime)].copy()

    # Heatmap (Plotly)
    fig = px.density_mapbox(
        gdf,
        lat="latitude",
        lon="longitude",
        z="count",
        radius=13,
        center={"lat": gdf["latitude"].mean(), "lon": gdf["longitude"].mean()},
        zoom=9,
        mapbox_style="carto-positron",
        color_continuous_scale="emrld",
    )

    fig.update_layout(
        title=f"Heatmap of {label_dict[selected_crime]} for Year {selected_year}",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
    )
    return fig


def creating_geo_chart(
    points_data,
    geo_data,
    width=500,
    height=300,
    background_fill="lightgray",
    background_stroke="white",
    circle_size=10,
    circle_color="steelblue",
    longitude_field="lon",
    latitude_field="lat",
    tooltip_fields=None,
):
    """
    Creates a Plotly map with a background layer (GeoJSON for Chicago PUMAs) and
    an overlay of points (e.g., schools).

    Parameters:
        points_data (pd.DataFrame): DataFrame containing point data (e.g., schools)
        geo_data (dict): GeoJSON FeatureCollection of your PUMA polygons
        width (int): Chart width in pixels.
        height (int): Chart height in pixels.
        background_fill (str): Fill color for the background polygons.
        background_stroke (str): Border color for the polygons.
        circle_size (int): Marker size for the points.
        circle_color (str): Marker color for the points.
        longitude_field (str): Name of the column in points_data for longitude.
        latitude_field (str): Name of the column in points_data for latitude.
        tooltip_fields (list of str): List of column names from points_data to include in hover info.
                                      The first field is used as the primary label.

    Returns:
        go.Figure: A Plotly Figure object representing the map.
    """
    # Create an empty Plotly Figure.
    fig = go.Figure()

    # --- Background Layer: Chicago PUMA Polygons ---
    # For the background, we use a Choroplethmapbox trace.
    # Create a list of feature IDs from the GeoJSON properties.
    puma_ids = [feature["properties"]["id"] for feature in geo_data["features"]]
    # Use dummy values as the z variable because we're only using the colorscale to set the fill.
    dummy_values = [1] * len(puma_ids)

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=geo_data,
            locations=puma_ids,
            z=dummy_values,
            colorscale=[[0, background_fill], [1, background_fill]],
            marker_line_color=background_stroke,
            marker_line_width=1,
            showscale=False,
            name="Chicago PUMAs",
        )
    )

    # --- Points Layer: School Locations ---
    # If no tooltip_fields are provided, default to the longitude and latitude fields.
    if tooltip_fields is None:
        tooltip_fields = [longitude_field, latitude_field]

    # Build a hover template. If more than one field is provided, use the first field as primary text,
    # and the others as additional info.
    if len(tooltip_fields) > 1:
        hover_template = "<b>%{text}</b><br>"
        for i, field in enumerate(tooltip_fields[1:]):
            hover_template += f"{field}: %{{customdata[{i}]}}<br>"
        hover_template += "<extra></extra>"
        # Create custom data from the additional tooltip fields.
        customdata = points_data[tooltip_fields[1:]].to_numpy()
        text_values = points_data[tooltip_fields[0]]
    else:
        hover_template = "<b>%{text}</b><extra></extra>"
        customdata = None
        text_values = points_data[tooltip_fields[0]]

    fig.add_trace(
        go.Scattermapbox(
            lat=points_data[latitude_field],
            lon=points_data[longitude_field],
            mode="markers",
            marker=go.scattermapbox.Marker(size=circle_size, color=circle_color),
            text=text_values,
            customdata=customdata,
            hovertemplate=hover_template,
            name="Schools",
        )
    )

    # --- Layout Settings ---
    # Center the map based on the mean of your points.
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(
                lat=points_data[latitude_field].mean(),
                lon=points_data[longitude_field].mean(),
            ),
            zoom=10,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        width=width,
        height=height,
        showlegend=True,
    )

    return fig


def create_stacked_chart_gender(df_c_long):
    
    # Then filter the DataFrame
    df_filtered = df_c_long[
        (df_c_long['PUMA'] == 9999)
        & (df_c_long['indicator_label'].isin(['High School', 'Middle', 'Elementary']))
        & (df_c_long['cut_name'].isin(['women', 'men']))
    ]

    color_scale = alt.Scale(
        domain=['men', 'women'],
        range=['#1f77b4', '#eb9b44']
    )

    indicator_order = ['Elementary', 'Middle', 'High School']

    # -- Gender selection (bound to legend) --
    gender_selection = alt.selection_point(
        fields=['cut_name'],
        bind='legend'
    )

    # -- Year selection (bound to a dropdown) --
    unique_years = sorted(df_filtered['year'].unique())
    #year_dropdown = alt.binding_select(options=unique_years, name='Select year')

    # IMPORTANT: selection_point is valid in Altair 5+
    year_selection = alt.selection_point(
        fields=['year'],
        #bind=year_dropdown,
        #init={'year': unique_years[-1]}  # pick the last year initially
    )

    bar = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X('sum(value):Q', stack='zero', title='Population'),
            y=alt.Y('indicator_label:N', sort=indicator_order, title='Education level'),
            color=alt.Color('cut_name:N', scale=color_scale),
            # Opacity is based on whether 'cut_name' is selected
            opacity=alt.condition(gender_selection, alt.value(0.9), alt.value(0.2)),
            tooltip=[
                alt.Tooltip('year', title='Year'),
                alt.Tooltip('puma_label', title='Puma'),
                alt.Tooltip('value', title='Population number')
            ]
        )
        # Add both parameters to the chart
        .add_params(gender_selection, year_selection)
        # Filter the data by selected year
        .transform_filter(year_selection)
    )

    return bar

def create_stacked_chart_race(df_c_long):
    
    # Then filter using the updated column
    df_filtered2 = df_c_long[
        (df_c_long['PUMA'] == 9999) &
        (df_c_long['indicator_label'].isin(['High School', 'Middle', 'Elementary'])) &
        (df_c_long['cut_name'].isin(['afroamerican', 'nonafroamerican']))    ]

    color_scale2 = alt.Scale(
        domain=['afroamerican', 'nonafroamerican'],        # The categories in cut_name
        range=['#1f77b4', '#eb9b44']    
    )
 
    indicator_order = ['Elementary', 'Middle', 'High School']
    # Define selection
    selection = alt.selection_point(fields=['cut_name'], bind='legend')
    # Create stacked bar chart
    bar = alt.Chart(df_filtered2).mark_bar().encode(
    x=alt.X('sum(value):Q', stack='zero', axis=alt.Axis(title='Population')),
    y=alt.Y('indicator_label:N', sort=indicator_order, axis=alt.Axis(title='Education level')),
    color=alt.Color('cut_name:N', scale=color_scale2),
    opacity=alt.condition(selection, alt.value(0.9), alt.value(0.2)),
    tooltip=[alt.Tooltip('year', title='Year'), alt.Tooltip('value', title='Population number')]
    ).add_params(selection)

    return bar


def load_crimes_shp():
    path = 'https://drive.usercontent.google.com/download?id=17lrQgaXcTAQTM4kMqt19RYvC4gtF9wCn&export=download&authuser=0&confirm=t&uuid=f69248de-b684-4c5f-976b-63576e8c9741&at=AEz70l53DiY7nTnR_fRZmhZYPvOx:1741223440221'

    # Saved to a DataFrame
    data = get_google_drive_files(path)
    
    block_data = data.groupby(['block', 'year','crime_type']).agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            count=("case_number", "count"),
        ).reset_index()

    return block_data
