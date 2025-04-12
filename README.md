# Understanding School Dropouts in Chicago: The Role of Crime and Socioeconomic Factors

## Abstract
Early school dropout is a multifaceted challenge that impacts education systems and societal outcomes in both developed and developing countries. In the United States, this phenomenon varies notably across and within regions. For instance, Chicago public schools display a wide range of 9th-grade dropout rates, ranging from 0% to 56.6% (CDPS, 2024). While the influence of individual, family, and school characteristics is well documented, a growing body of studies has begun to explore the effects of broader social contexts on adolescent educational outcomes including neighborhood crime or violence. 

This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes. By running the application, you will be able to explore these factors and their relationships on an interactive dashboard.

![screenshot](images/project_screenshot.png)

## Authors
| **Team Member**     | **Responsibilities** |
|---------------------|----------------------|
| **Angela Lopez** <br> alopezsanchez@uchicago.edu   | - Pulled data from the Census API.<br> - Cleaned census, social, and education indicator data.<br> - Designed graphs for demographics and attendance rates.<br> - Structured and styled the dashboard. |
| **César Núñez**  <br> cnunezh@uchicago.edu    | - Pulled crime data from the Chicago Police Department.<br> - Cleaned and reshaped crime data, and merged all data sources.<br> - Built module test functions.<br> - Created crime-related visualizations. |
| **Shahzaib Jamali** <br> shahzaibjamali@uchicago.edu  | - Pulled data from CPS APIs and Excel dropout files.<br> - Cleaned education data and merged sources.<br> - Created school-related graphs.<br> - Led project storytelling. |

## Project Video:
[Project Video](https://youtu.be/aOXfe6JOBbc) 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/aOXfe6JOBbc/0.jpg)](https://www.youtube.com/watch?v=aOXfe6JOBbc)

***
### How to run the project

1. [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone the repo for the project using the url on GitHub
```
git clone git@github.com:uchicago-2025-capp30122/30122-project-andes-indus-analytics.git
```
As this module brings together information from different data sources. To run this program it is necessary to provide an APP key for the City of Chicago Data.
The steps to create an APP KEY are:

    1. Enter https://data.cityofchicago.org/ to create an account
    2. Enter https://data.cityofchicago.org/profile/edit/developer_settings and hit "Create a new App Token"
    3. Save your APP TOKEN in a safe place 

After sort out the API Key step, by running the following commands, a new tab in your preferred browser will prompt with the final visualization of our project. 

3. Synchronize the virtual environment.
```
uv sync
```
4. If you want to use the data we have already stored on Google Drive, run the following command in the terminal. This command should take <b>1 minute</b> to run.
```
uv run -m andes_indus
```
5. If you want to fetch the data from the original sources, run the following command in the terminal. This command should take <b>15 minute</b> to run.
```
uv run -m andes_indus --full
```
### Running Tests

Before running any test, you should define the CHICAGO_APP_TOKEN in your environment. Then to run the tests, please use the following command in andes-indus.

```
uv run pytest tests
```
***

## Data Sources

### 1. U.S. Census Data - American Community Survey
- *Source:* [U.S. Census Bureau](https://www.census.gov/data/developers/data-sets/census-microdata-api.html)
- *Description:* This dataset provides demographic data extracted from the U.S. Census Bureau’s American Community Survey. No API key is required for access.

### 2. Chicago Crime Data - City of Chicago
- *Crime Data:* [City of Chicago Crime Data](https://dev.socrata.com/foundry/data.cityofchicago.ls/ijzp-q8t2)
- *Description:* This dataset includes crime records for the City of Chicago. 

### 3. Education Data - Chicago Public Schools
- *School Search:* [CPS Typeahead School Search](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-TypeaheadSchoolSearch_SearchValue)
- *School Profile:* [CPS Single School Profile](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-SingleSchoolProfile_SchoolID)
- *Description:* This dataset contains school-related information such as attendance rate, graduation rate, school address, and geographical coordinates (longitude and latitude). No API key is required for access.
- *School Metrics:* [CPS Dropout Data](https://www.cps.edu/about/district-data/metrics/)
- *Description:* This excel data set contains information pertaining to the dropout rate of schools for multiple years.

## Acknowledgments
We would like to express our sincere gratitude to James Turk (CAPP 30122 Instructor) and Daniel Muñoz (CAPP 30122 TA) for their support and guidance throughout this project.
