import argparse
from .join_data import gen_final_data
from .census_utils import rename_functions
from pathlib import Path
import webbrowser
from threading import Timer
import time

def main():
    path_puma = Path("data/data_pumas.csv")
    path_neighborhood = Path("data/data_neighborhoods.csv")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        help="Fetch the data from the original sources and generates csv files.",
        action="store_true",
    )
    args = parser.parse_args()
    if args.full:
        gen_final_data(True)
    else:
        if not path_puma.exists() or not path_neighborhood.exists():
            gen_final_data(False)


    rename_functions(output_file="data/census_df_long.csv")

def open_browser():
    webbrowser.open_new("http://localhost:8050")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'Duration: {end-start}')
    from .app import app
    Timer(1, open_browser).start()
    app.run_server(debug=False, port = '8050')
