import altair as alt
import geopandas as gpd
import plotly.express as px

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
    
def create_interactive_bar(dff, select, stroke_width, selected_year,highlight):
        # Create the bar chart sorted descending by attendance_rate_high
    bar = alt.Chart(dff).mark_bar(fill="#0099cc", stroke="black", cursor="pointer").encode(
        x=alt.X('puma_label',axis=alt.Axis(title='PUMA name'), sort=alt.EncodingSortField(field='attendance_rate_high', op='sum', order='descending')),
        y=alt.Y('attendance_rate_high', axis=alt.Axis(title='Attendance rate - high school')),
        fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
        strokeWidth=stroke_width,
    ).properties(
        title=f"Attendance Rate for Year {selected_year} - High School (self reported)"
    ).add_params(select, highlight)

    return bar

def create_crime_heat_map(gdf: gpd.GeoDataFrame,
                          selected_crime: str, 
                          selected_year: int,
                          label_dict: dict):
    
    gdf = gdf[(gdf['year'] == selected_year)].copy()

    if selected_crime != 'Non-violent' and selected_crime != 'Violent':
        gdf = gdf.groupby(['year', 'block', 'latitude', 'longitude']).agg(
            count=("count", "sum")
        ).reset_index()
    else:
        gdf = gdf[(gdf['crime_type'] == selected_crime)].copy()

    # Heatmap (Plotly)
    fig = px.density_mapbox(
        gdf, 
        lat='latitude', 
        lon='longitude', 
        z='count',
        radius=15,
        center={"lat": gdf['latitude'].mean(), "lon": gdf['longitude'].mean()},
        zoom=9,
        mapbox_style="carto-positron",
        color_continuous_scale="rdbu"
    )

    fig.update_layout(
        title=f"Heatmap of {label_dict[selected_crime]} for Year {selected_year}",
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    return fig