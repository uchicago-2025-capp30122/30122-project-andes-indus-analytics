import argparse
from join_data import gen_final_data, transform_to_long_format
import pandas as pd
from pathlib import Path
from app import app


def main():
    path_puma = Path("data/data_pumas.csv")
    path_neighborhood = Path("data/data_neighborhoods.csv")

    if not path_puma.exists() or not path_neighborhood.exists():
        gen_final_data(full_fetch=False)

    data_pumas = pd.read_csv(path_puma)
    data_neighborhoos = pd.read_csv(path_neighborhood)

    transform_to_long_format(
        "data/census_df.csv", ["PUMA", "year"], "indicator", "value"
    )


if __name__ == "__main__":
    # main()
    app.run_server(debug=False)
