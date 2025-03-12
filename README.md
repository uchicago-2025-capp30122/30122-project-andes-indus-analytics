# Understanding School Dropouts in Chicago: The Role of Crime and Socioeconomic Factors

## Abstract
Early school dropout is a multifaceted challenge that impacts education systems and societal outcomes in both developed and developing countries. In the United States, this phenomenon varies notably across and within regions. For instance, Chicago public schools display a wide range of 9th-grade dropout rates, ranging from 0% to 56.6% (CDPS, 2024). While the influence of individual, family, and school characteristics is well documented, a growing body of studies has begun to explore the effects of broader social contexts on adolescent educational outcomes such as neighborhood crime or violence. 

This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes.By running the application, you will be able to explore these factors and their relationships on an interactive dashboard.

![screenshot](images/project_screenshot.png)

## Authors
- *Angela López Sanchez*
- *Cesar Núñez*
- *Shahzaib Jamali*


## Project Video:
[Project Video](linktovideo)


***
### How to run the project

1. Clone the repo for the project using the url on GitHub

    `git clone git@github.com:uchicago-2025-capp30122/30122-project-andes-indus-analytics.git`

As this module brings together information from different data sources. To run this program it is necessary to provide an APP key for the City of Chicago Data.
The steps to create an APP KEY are:

    1. Enter https://data.cityofchicago.org/ to create an account
    2. Enter https://data.cityofchicago.org/profile/edit/developer_settings and hit "Create a new App Token"
    3. Safe your APP TOKEN in a safe place 

For simplicity, you can work with our key that will be provided by email and you shouyld define a constant in the terminal:

On Windows: 
```
$env:CHICAGO_APP_TOKEN = "Eqk9pQsM8RsYYawwjwyFUTlYj"
```
On Linux/MacOS:
```
export CHICAGO_APP_TOKEN="Eqk9pQsM8RsYYawwjwyFUTlYj"
```

After sort out the API Key step, by running the following commands, a new tab in your preferred browser will prompt with the final visualization of our project. 

2. Run `uv sync`
### This command may take a minute to load the project to the terminal.
3. Run `uv run -m andes_indus`, if you want to use the data we have already storage on [Google Drive](https://drive.google.com/drive/folders/1Xw6wfJzPkBWHGvuAjtEUTKerQygmDidL).
### This command may take 15 minutes to load the project to the terminal.
4. Run `uv run -m andes_indus --full`, if you want to fetch the data from the original sources. This might take 15 minutes to run on average.

### Running Tests

Before running any test, you should define the CHICAGO_APP_TOKEN in your environment. Then to run the tests, please use the following command in andes-indus.

```bash
`uv run pytest tests`
```
***

## Data Sources

### 1. U.S. Census Data - American Community Survey
- *Source:* [U.S. Census Bureau](https://www.census.gov/programs-surveys/acs)
- *Description:* This dataset provides demographic data extracted from the U.S. Census Bureau’s American Community Survey. No API key is required for access.

### 2. Chicago Crime Data - City of Chicago
- *Crime Data:* [City of Chicago Crime Data](https://data.cityofchicago.org/Public-Safety/Crimes-Map/mw69-m6xi)
- *Description:* This dataset includes crime statistics for the City of Chicago.

### 3. Education Data - Chicago Public Schools
- *School Search:* [CPS Typeahead School Search](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-TypeaheadSchoolSearch_SearchValue)
- *School Profile:* [CPS Single School Profile](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-SingleSchoolProfile_SchoolID)
- *Description:* This dataset contains school-related information such as attendance rate, graduation rate, school address, and geographical coordinates (longitude and latitude). No API key is required for access.
- *School Metrics:* [CPS Dropout Data](https://www.cps.edu/about/district-data/metrics/)
- *Description:* This excel data set contains information pertaining to the dropout rate of schools for multiple years.
