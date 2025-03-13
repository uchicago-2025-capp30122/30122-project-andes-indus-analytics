from pathlib import Path
import pandas as pd
import geopandas as gpd
from .figures import load_crimes_shp
from .app_utils import ATTENDANCE_COLS

# Loading data files - Puma level
pumas_shp = gpd.read_file(Path("data/shapefiles/data_pumas.shp"))
pumas_shp = pumas_shp.rename(
    columns={"total_cr_1": "total_crim_pc", "non_viol_1": "non_violent_pc"}
)

pumas_df = pd.read_csv(Path("data/data_pumas.csv"))

cols_to_keep = ["puma", "year", "violent_pc", "non_violent_pc", "total_crim_pc"]
pumas_df_long = pumas_df[cols_to_keep + ATTENDANCE_COLS]
pumas_df_long = pumas_df_long.melt(
    cols_to_keep,
    ATTENDANCE_COLS,
    var_name="attendance_category",
    value_name="attendance_rate",
)

df_c = pd.read_csv(Path("data/census_df.csv"))
df_c_long = pd.read_csv(Path("data/census_df_long.csv"))

# Loading maps shapefiles
pumas = gpd.read_file(Path("data/shapefiles/pumas/chicago_pumas.shp"))
neighborhood_shp = gpd.read_file(Path("data/shapefiles/data_neighborhoods.shp"))
neighborhood_shp = neighborhood_shp.rename(
    columns={"total_cr_1": "total_crim_pc", "non_viol_1": "non_violent_pc"}
)
crimes_shp = gpd.GeoDataFrame(load_crimes_shp())

# Loading school locations
schools_df = pd.read_csv(Path("data/merged_school_data.csv"))
