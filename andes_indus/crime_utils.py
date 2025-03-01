from typing import NamedTuple


class Crime(NamedTuple):
    case_number: str
    latitude: float
    longitude: float
    block: str
    year: int
    date: str
    primary_type: str
    puma: None | str
    neighborhood: None | str


def get_crime_data(client, data_set: str, lst_years: list) -> list[Crime]:
    """
    Gathers data from an specific dataset from the City of Chicago's Data

    Args:
        - data_set: data set code
        - lst_years: list of years to gather

    Returns: pd.DataFrame with all the records from the data_set in lst_years
    """

    if data_set == "gumc-mgzr":
        results = client.get(data_set, limit=1000)
        return process_results(results, [])
    else:
        results = [client.get(data_set, year=y, limit=1000) for y in lst_years]
        return process_results([r for year in results for r in year], [])


def process_results(results, lst_results) -> list:
    for row in results:
        if "latitude" in row.keys():
            lst_results.append(
                Crime(
                    case_number=row["case_number"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    block=row["block"],
                    year=int(row["date"][0:4]),
                    date=row["date"],
                    primary_type=row.get("primary_type", "homicide"),
                    puma=None,
                    neighborhood=None,
                )
            )
    return lst_results
