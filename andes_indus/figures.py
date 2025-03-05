import altair as alt
import geopandas as gpd
import pathlib
import json
import pandas as pd
from merge_shp import load_pumas_shp, load_schools

def create_crime_map(gdf: gpd.GeoDataFrame, 
                     selected_crime: str, 
                     selected_year: int,
                     label_dict: dict) -> alt.Chart:

    gdf = gdf[gdf['year'] == selected_year].copy()
    map = alt.Chart(gdf).mark_geoshape(
        stroke = 'white', strokeWidth = 0.5
        ).encode(color=alt.Color(selected_crime, type="quantitative", title="Crime Rate"),
                 tooltip=[alt.Tooltip('puma_label', title='Puma'), alt.Tooltip('year', title='Year'), alt.Tooltip(selected_crime, title="Crime per 1000 hab.")]
        ).project(
            type='mercator'
        ).properties(
            width = 500,
            height = 500,
            title=f"{label_dict[selected_crime]} ocurrances per 1000 hab. for Year {selected_year}"
        )
    
    return map

def create_geo_chart(points_data, geo_data,
                     width=500, height=300,
                     background_fill='lightgray', background_stroke='white',
                     circle_size=10, circle_color='steelblue',
                     longitude_field='longitude', latitude_field='latitude',
                     tooltip_fields=None, projection='mercator'):
    if tooltip_fields is None:
        tooltip_fields = [longitude_field, latitude_field]
    
    background_chart = alt.Chart(geo_data).mark_geoshape(
        fill=background_fill,
        stroke=background_stroke
    ).properties(
        width=width,
        height=height
    ).project(projection)
    
    points_chart = alt.Chart(points_data).mark_circle(
        size=circle_size,
        color=circle_color
    ).encode(
        longitude=f'{longitude_field}:Q',
        latitude=f'{latitude_field}:Q',
        tooltip=tooltip_fields
    )
    
    final_chart = background_chart + points_chart
    return final_chart
