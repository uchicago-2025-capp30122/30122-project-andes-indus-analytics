import altair as alt
import json
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api_get import get_google_drive_files

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
            # Swap 'puma_label' to the y-axis
            y=alt.Y(
                "puma_label",
                axis=alt.Axis(title="PUMA name"),
                sort=alt.EncodingSortField(
                    field="attendance_rate_high", op="sum", order="descending"
                ),
            ),
            # Swap 'attendance_rate_high' to the x-axis
            x=alt.X(
                "attendance_rate_high",
                axis=alt.Axis(title="Attendance rate - high school"),
            ),
            fillOpacity=alt.condition(select, alt.value(1), alt.value(0.3)),
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


def create_chicago_school_visualization(gdf_chicago, df_schools, selected_year):
    """
    Creates an interactive Altair chart combining a Chicago PUMAs map with school data,
    with a density plot that shows the distribution of dropout rates for schools 
    within the brushed area (and only considering valid dropout rates).
    
    Parameters:
        gdf_chicago (GeoDataFrame): A GeoDataFrame containing the Chicago PUMAs shapefile data.
        df_schools (DataFrame): A DataFrame containing school data with columns such as 
                                "Longitude", "Latitude", "Year", "School Name_x", 
                                "Student Count", "DropoutRate", etc.
    
    Returns:
        alt.Chart: An Altair chart that concatenates a map and a density plot.
    """
    # Convert school DataFrame to GeoDataFrame (if not already one)
    if not hasattr(df_schools, "geometry"):
        gdf_schools = gpd.GeoDataFrame(
            df_schools,
            geometry=gpd.points_from_xy(df_schools["Longitude"], df_schools["Latitude"]),
            crs="EPSG:4326"
        )
    else:
        gdf_schools = df_schools.copy()

    # Ensure both datasets are in EPSG:4326
    gdf_chicago = gdf_chicago.to_crs("EPSG:4326")
    gdf_schools = gdf_schools.to_crs("EPSG:4326")
    
    # Convert Chicago GeoDataFrame to GeoJSON for Altair
    chicago_geojson = json.loads(gdf_chicago.to_json())
    chicago_data = alt.Data(values=chicago_geojson["features"])
    
    # Define an interactive brush based on latitude (vertical slice)
    brush = alt.selection_interval(
        encodings=["latitude"],
        empty=False,
        value={"latitude": [41.80, 41.90]}
    )
    
    # Prepare the school data: treat Year as string and filter to 2013 and 2023
    gdf_schools["Year"] = gdf_schools["Year"].astype(str)
    gdf_schools = gdf_schools[gdf_schools["Year"] == str(selected_year)]
    
    # Create the Chicago map layer
    chicago_map = alt.Chart(chicago_data).mark_geoshape(
        fill="lightgray", stroke="white", strokeWidth=0.1
    ).properties(width=600, height=400)
    
    # Create the school points layer (filter by year)
    schools = alt.Chart(gdf_schools).mark_circle(opacity=0.7).encode(
        longitude="Longitude:Q",
        latitude="Latitude:Q",
        tooltip=["School Name_x", "Student Count:Q", "Year"],
        color=alt.condition(brush, alt.value("goldenrod"), alt.value("royalblue")),
        size=alt.Size("Student Count:Q", scale=alt.Scale(range=[10, 200]), title="Student Count")
    ).add_params(brush)
    
    # Combine the map and school layers with Mercator projection
    left_map = alt.layer(chicago_map, schools).project(type="mercator").properties(width=600, height=400)
    
    # Ensure DropoutRate is numeric (if not already)
    gdf_schools["DropoutRate"] = pd.to_numeric(gdf_schools["DropoutRate"], errors="coerce")
    
    # Create a density (KDE) plot based solely on the brushed area,
    # filtering out records with missing dropout rates.
    density_plot = (
        alt.Chart(gdf_schools)
        .transform_filter(brush)
        .transform_filter("datum.DropoutRate != null")
        .transform_density(
            density="DropoutRate",
            as_=["DropoutRate", "density"],
            extent=[0, 60]  # Adjust extent based on your data range
        )
        .mark_area(opacity=0.7, color="goldenrod")
        .encode(
            x=alt.X("DropoutRate:Q", title="Dropout Rate (%)"),
            y=alt.Y("density:Q", title="Density", scale=alt.Scale(domain =[0,0.2]))
        )
        .properties(width=400, height=400)
    )
    
    # Concatenate the map and the density plot side by side
    final_chart = left_map | density_plot
    
    return final_chart

def create_stacked_chart_gender(df_c_long, selected_year):
    
    # Then filter the DataFrame
    df_filtered = df_c_long[
        (df_c_long['PUMA'] == 9999)
        & (df_c_long['indicator_label'].isin(['High School', 'Middle', 'Elementary']))
        & (df_c_long['cut_name'].isin(['women', 'men']))
    ]

    df_filtered = df_filtered[df_filtered['year'] == selected_year]

    color_scale = alt.Scale(
        domain=['men', 'women'],
        range=['#005A9C', '#A8D0E6' ] 
    )

    indicator_order = ['Elementary', 'Middle', 'High School']

    # -- Gender selection (bound to legend) --
    gender_selection = alt.selection_point(
        fields=['cut_name'],
        bind='legend'
    )

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
            x=alt.X('sum(value):Q', stack='zero', axis=alt.Axis(title='Population', 
                                                        titleFontSize=14, 
                                                        labelFontSize=12)),

            y=alt.Y('indicator_label:N', sort=indicator_order, title=""),
           
            color=alt.Color('cut_name:N', scale=color_scale, title="Cut"),
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
        .properties(
            width=500,  #  Increase width
            height=100,  # Increase height
            title="Gender"
        )
    )

    return bar

def create_stacked_chart_race(df_c_long, selected_year):
    
    # Then filter using the updated column
    df_filtered2 = df_c_long[
        (df_c_long['PUMA'] == 9999) &
        (df_c_long['indicator_label'].isin(['High School', 'Middle', 'Elementary'])) &
        (df_c_long['cut_name'].isin(['hispanic', 'afroamerican', 'nonafroamerican_hispanic']))    ]

    df_filtered2 = df_filtered2[df_filtered2['year'] == selected_year]

    color_scale2 = alt.Scale(
        domain=['afroamerican',"hispanic", 'nonafroamerican_hispanic'],        # The categories in cut_name
        range=['#005A9C', '#A8D0E6', '#E57373' ]    
    )
 
    indicator_order = ['Elementary', 'Middle', 'High School']
   
    # -- race selection (bound to legend) --
    race_selection = alt.selection_point(
        fields=['cut_name'],
        bind='legend'
    )

    year_selection = alt.selection_point(
        fields=['year'],
    )
       # Create stacked bar chart
    bar = alt.Chart(df_filtered2).mark_bar().encode(

    x=alt.X('sum(value):Q', stack='zero', axis=alt.Axis(title='Population', 
                                                        titleFontSize=14, 
                                                        labelFontSize=12)),

    y=alt.Y('indicator_label:N', sort=indicator_order, title=""),
   
    color=alt.Color('cut_name:N', scale=color_scale2, title="Cut"),
    opacity=alt.condition(race_selection, alt.value(0.9), alt.value(0.2)),
    tooltip=[alt.Tooltip('year', title='Year'), alt.Tooltip('value', title='Population number')]
    ).add_params(race_selection, year_selection).properties(
            width=500,  #  Increase width
            height=100,  # Increase height
            title="Race/Ethnicity"
        ).transform_filter(year_selection)

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

def create_graph_multiple(df_c_long):
        
    # Then filter using the updated column
    df_filtered2 = df_c_long[
        (df_c_long['PUMA'] == 9999) &
        (df_c_long['indicator'].isin(['attendance_rate_elementary', 'attendance_rate_middle', 'attendance_rate_high'])) &
        (df_c_long['cut_name'].isin(['afroamerican', 'nonafroamerican_hispanic',"Total","hispanic"])) ]
    
    indicator_order = ['Elementary', 'Middle', 'High School']

    graph = alt.Chart(df_filtered2).mark_point().encode(
    alt.X("value", scale=alt.Scale(domain=[60,100],zero=False), axis=alt.Axis(title='Percentage', titleFontSize=14, labelFontSize=12) ),
    y=alt.X("year:N",axis=alt.Axis(title='Year', titleFontSize=14, labelFontSize=12)),
    color=alt.Color(
                "cut_name:N",
                legend=alt.Legend(
                    title="Cut",
                    titleFontSize=14,
                    labelFontSize=12
                )),
    facet=alt.Facet("indicator_label:O", columns=1, title="", sort=indicator_order),
    ).properties(
    width=450,
    height=100,
    )
    
    return graph

def create_scatter_dynamic(df:pd.DataFrame, 
                           selected_year, 
                           selected_crime, 
                           crime_labels,
                           selected_level,
                           level_labels):

    def split_attendance_info(cat):
        parts = cat.replace('attendance_rate_', '').split('_')
        level = parts[0]  # elementary, middle, high
        race = '_'.join(parts[1:]) if len(parts) > 1 else 'total'
        return pd.Series([level, race])

    df[['level', 'race']] = df['attendance_category'].apply(split_attendance_info)

    # Drop the original category column if you want
    df = df.drop(columns=['attendance_category'])
    df_scatter = df[(df["year"] == selected_year) & 
                    (df["level"] == selected_level) ]
    
    # Base scatterplot chart
    base = alt.Chart(df_scatter).mark_point(filled=True).encode(
        x=alt.X(f'{selected_crime}:Q', title=crime_labels[selected_crime]),
        y=alt.Y('attendance_rate:Q', title=f'Attendance Rate - {level_labels[selected_level]}'),
        color=alt.Color('race:N', legend=None),
        tooltip=['puma', 'year', 'attendance_rate', f'{selected_crime}']
    ).properties(
        width=200,
        height=200
    )

    # Facet grid (columns by race, rows by level)
    chart = base.facet(
        column=alt.Column('race:N', title='Race')
    )

    regression = alt.Chart(df_scatter).transform_regression(
        f'{selected_crime}', 'attendance_rate'
    ).mark_line().encode(
        x=f'{selected_crime}:Q',
        y='attendance_rate'
    )

    chart = (base + regression).facet(
        column='race:N'
    )
    return chart