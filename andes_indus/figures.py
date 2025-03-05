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

def create_crime_heat_map(gdf: gpd.GeoDataFrame,
                          selected_crime: str, 
                          selected_year: int,
                          label_dict: dict) -> alt.Chart:
    
    gdf = gdf[gdf['year'] == selected_year].copy()

    # Heatmap (Plotly)
    fig = px.density_mapbox(
        gdf, 
        lat='latitude', 
        lon='longitude', 
        z=selected_crime,
        radius=25,
        center={"lat": gdf['latitude'].mean(), "lon": gdf['longitude'].mean()},
        zoom=10,
        mapbox_style="carto-positron",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        title=f"Heatmap of {label_dict[selected_crime]} (per 1000 inhabitants) for Year {selected_year}",
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    return fig