import argparse
from join_data import gen_final_data, transform_to_long_format
import pandas as pd
from pathlib import Path
import folium as fm
import geopandas as gpd
import webbrowser


def main():
    path_puma = Path("data/data_pumas.csv")
    path_neighborhood = Path("data/data_neighborhoods.csv")

    if not path_puma.exists() or not path_neighborhood.exists():
        gen_final_data()

    data_pumas = pd.read_csv(path_puma)
    data_neighborhoos = pd.read_csv(path_neighborhood)

   # transform_to_long_format(
    #"data/census_df.csv",
    #["PUMA","year"],
    #'indicator',
    #'value') 

    # pumas_shp = gpd.read_file('data/shapefiles/pumas/pumas2022.shp')
    # neighborhoods_shp = gpd.read_file('data/shapefiles/chicomm/chicomm.shp')
    # z = fm.Map(location = [41.8783874319104, -87.62875352665596], tiles='cartodbpositron', zoom_start = 10.5)

    # fm.Choropleth(
    #     geo_data=neighborhoods_shp,
    #     data=schools_by_neighborhood,
    #     columns=['neighborhood', 'total_students'],
    #     key_on="feature.properties.CHICOMNO",
    #     fill_color="YlOrRd",
    #     fill_opacity=0.8,
    #     line_opacity=0.2,
    #     legend_name="Attendance rate (%)",
    #     smooth_factor=0,
    #     Highlight= True,
    #     line_color = "#0000",
    #     overlay=True,
    #     nan_fill_color = "White"  # fill white missing values
    #     ).add_to(z)

    # highlight_function = lambda x: {'fillColor': '#000000',
    #                             'color':'#000000',
    #                             'fillOpacity': 0.5,
    #                             'weight': 0.1}

    # breakpoint()
    # # schools_by_puma = schools_by_puma.rename(columns={"puma": "PUMACE20"})
    # schools_by_neighborhood = schools_by_neighborhood.rename(columns={"neighborhood": "CHICOMNO"})

    # # pumas_shp["PUMACE20"] = pd.to_numeric(pumas_shp["PUMACE20"])

    # # data_both = pd.merge(pumas_shp, schools_by_puma, how="inner", on="PUMACE20")
    # data_both = pd.merge(neighborhoods_shp, schools_by_neighborhood, how="inner", on="CHICOMNO")
    # data_both = data_both.to_json()

    # details = fm.features.GeoJson(
    #     data = data_both,
    #     control=False,
    #     highlight_function=highlight_function,
    #     tooltip=fm.features.GeoJsonTooltip(
    #         fields=['CHICOMNO'],   #Variable selection
    #         aliases=['Neighborhood'],  # renames
    #         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    #     )
    # )

    # z.add_child(details)
    # z.keep_in_front(details)
    # z.save("visualizations/high_school_rate.html")


if __name__ == "__main__":
    main()
    # html = Path("visualizations/high_school_rate.html")
    # webbrowser.open_new_tab(html)
