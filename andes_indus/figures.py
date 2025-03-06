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

import pathlib
import json
import pandas as pd
import altair as alt

# Import your custom functions from merge_shp.py
from merge_shp import load_pumas_shp, load_schools

# Import your create_geo_chart function
# (Assume it's in a separate module or defined in this script)
def create_geo_chart(points_data, geo_data,
                     width=500, height=300,
                     background_fill='lightgray', background_stroke='white',
                     circle_size=10, circle_color='steelblue',
                     longitude_field='longitude', latitude_field='latitude',
                     tooltip_fields=None, projection='albersUsa'):
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

pumas_path = pathlib.Path("path/to/your/pumas_shapefile.shp")  # update with your shapefile path
pumas = load_pumas_shp(pumas_path)

# Convert list of Puma objects to a GeoJSON FeatureCollection
features = []
for puma in pumas:
    feature = {
       "type": "Feature",
       "geometry": puma.polygon.__geo_interface__,  # Convert Shapely Polygon to GeoJSON format
       "properties": {
            "id": puma.id,
            "name": puma.name
       }
    }
    features.append(feature)

geo_data = {
    "type": "FeatureCollection",
    "features": features
}


schools_csv_path = pathlib.Path("path/to/your/schools.csv")  # update with your CSV path
schools_list = load_schools(schools_csv_path)

# Convert list of School objects to a DataFrame
# Adjust the field names if needed. Here, we assume:
# - 'Latitude' and 'Longitude' are in the CSV (converted to float).
# - 'School Name' and other fields you want to display.
schools_data = []
for school in schools_list:
    schools_data.append({
         "id": school.id,
         "school_name": school.name,
         "lat": float(school.latitude),    # Convert to float if not already numeric
         "lon": float(school.longitude),
         "student_count": float(school.student_count)  # Example additional field
    })

schools_df = pd.DataFrame(schools_data)


chart = create_geo_chart(
    points_data=schools_df,
    geo_data=geo_data,
    longitude_field='lon',       # Use the column name from your DataFrame for longitude
    latitude_field='lat',        # Use the column name for latitude
    tooltip_fields=['school_name', 'student_count']  # Customize tooltips as needed
)

# Display the chart (in Jupyter Notebook or another supported environment)
chart.display()
