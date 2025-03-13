# Understanding School Attendance / Dropouts in Chicago

## Project Overview

This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school attendance across school age population in the chicago area and dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes. By running the application, you will be able to explore these factors and their relationships on an interactive dashboard.

---

## Data Documentation

### 1. U.S. Census Data - American Community Survey
- *Source:* [U.S. Census Bureau](https://www.census.gov/programs-surveys/acs)
- *Description:* This dataset provides demographic data extracted from the U.S. Census Bureau’s American Community Survey. No API key is required for access.

### 2. Chicago Crime Data - City of Chicago
- *Crime Data:* [City of Chicago Crime Data](https://data.cityofchicago.org/Public-Safety/Crimes-Map/mw69-m6xi)
- *Homicide Data:* [City of Chicago Homicide Data](https://data.cityofchicago.org/Public-Safety/Homicides/ijzp-q8t2)
- *Description:* This dataset includes crime and homicide statistics for the City of Chicago. API key is required for access.

### 3. Education Data - Chicago Public Schools
- *School Search:* [CPS Typeahead School Search](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-TypeaheadSchoolSearch_SearchValue)
- *School Profile:* [CPS Single School Profile](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-SingleSchoolProfile_SchoolID)
- *Description:* This dataset contains school-related information such as attendance rate, graduation rate, school address, and geographical coordinates (longitude and latitude). No API key is required for access.
- *School Metrics:* [CPS Dropout Data](https://www.cps.edu/about/district-data/metrics/)
- *Description:* This excel data set contains information pertaining to the dropout rate of schools for multiple years.

### Data Gaps & Challenges
- **Gaps:** 
    - Crime: The fetched information was retrived as a crime per block and our unit analysis was PUMA and comunity area. 
    - Education : The data for school location and profile was only available for current year. Secondly, data for dropout
    and attendace were available from two different source types, excel and APIs.
    - Census: The PUMAS distribution changed with the 2020 Census. for 2023 we had information for 18 PUMAs while for 2013 ans 2018 we had 17 PUMAS. 

- **Quality Issues:** Describe inconsistencies, outliers, or other data quality challenges.

- **Mitigation Strategies:** Explain how these issues were addressed.
    - Crime : We created a function to join the retrieved data to a PUMA-community area see quatre.py
    - Education : We created two seperate csv files from the two sources and merged the data to make it comparable and accessible.
    - Census : We did not reconcile the information and decided to show the data for 18 and 17 PUMAs, respectively. 

### Data Flow and Project Structure

- **Overview:** The project consists of three main directories: `andes_indus`, `tests`, and `data`.

`andes_indus` contains the project's main module. The module files are structured to fetch and compute data from various sources, merge and sort it, and feed it into the final dashboard (`app.py`).
Demographic and social information is retrieved using `api_get.py`, which includes functions to fetch data from the Census API and filter it for the Chicago area. Since the Community Survey (referred to as "Census") includes data for the entire United States and is quite large, we store a version of each analyzed year in Google Drive. This allows us to fetch data directly from Google Drive, making data collection more efficient.
`census_utils` contains functions to clean the data, create social and education variables for analysis, aggregate them by PUMA, generate education indicators, and provide helper functions for labeling variables and reshaping the data into a long format.
`crime_utils` contains functions to fetch crime data. Additionally, it includes a Crime object (which is useful for merging crime data with observation units—PUMAs and Community Areas). This module also provides functions to create a list of crime objects and data frames for the analyzed years. Like `api_get.py`, it retrieves data from Google Drive to enhance efficiency.
`education_utils` contains functions to fetch school-related data from the Chicago Public Schools API (e.g., school locations and profiles) and merge it with CSV files containing bulk data on school dropout rates for the analyzed years.
`merge_shp` contains classes for PUMA, Neighborhood, and School objects. It loads data from shapefiles and CSV files and creates a list of each object. It also includes functions for geospatial merging between PUMAs, Neighborhoods, Schools, and Crime data.
`join_data` contains functions to integrate data from the three main sources. The final output consists of two databases:
A dataset at the PUMA and Year level, which includes Census and Crime data at the PUMA level.
A dataset at the Neighborhood and Year level.
`app.py` contains the dashboard code, which leverages the `app_layout` folder. This folder includes the figures, text, and structure necessary to create the front end of the dashboard.   
- **Diagram:**  

![Structure](Datapipeline.png)

---

## Project Structure
### Modules and Their Functions
- **Data:**  
- contains the bulk data used for the project including the shapefiles.   
- **Tests**  
- Contains the project tests
- **Andes indus Module**
- explained above.


## Team Responsibilities

### Team Member Contributions
- **Team Member 1 (Angela Lopez):**   
  - *Responsibilities:* 

    - Data Collection: Pulled data from the census API. 
    - Data Cleaning: Created functions for cleaning census data and social and education indicators. 
    - Data Visualization: Creating graphs for demoraphic and attendace rate and dashboard structure/design.

- **Team Member 2 (César Núñez):**  
  - *Responsibilities:* 

    - Data Collection: Pulled data of crime from the Chicago Police Depertment
    - Data Cleaning: Created functions to clean and reashape crime data, compute the merge between all the information sources.
    - Testing: Create the module test functions.
    - Data Visualization: Create crime related visualizations.  

- **Team Member 3 (Shahzaib Jamali):**  
  - *Responsibilities:* 

    - Data Collection: Pulled data from CPS APIs and accessed Dropout data from excel file 
    - Data Cleaning: Cleaned the data for education and merging API data and excel data.
    - Data Visualization: Created the School related graphs for the dashboard. Lead the story telling of the project.  


### Collaboration Notes

The team coordinated its efforts by establishing a clear version control strategy. Each member worked on an individual branch within the repository, allowing for independent development of features and updates. All changes were communicated through commits from these branches into a centralized main branch, ensuring that updates were systematically integrated and the project's progress remained transparent.

---

## Final Thoughts

### Project Goals vs. Outcomes
<<<<<<< HEAD
- **Intended Goals:** This project aimed to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes. 
- **Outcomes:** The project successfully demonstrated a naïve relationship between crime and education outcomes (school dropout rates and school attendance). The next step in this project is to complete the causal analysis by robustly conducting a well-specified spatial regression analysis.
- **Lessons Learned:** 
Integrating data from the community survey, crime data, and educational metrics proved more challenging than anticipated. We had to invest significant effort into cleaning and integrating the datasets, and key assumptions—such as treating the number of schools as constant over three years—were necessary to merge the information. This experience underscored the complexities of working with disparate data sources. Key takeaways include the need for careful planning around data integration, transparent documentation of assumptions, and iterative validation to maintain data accuracy. 

---

- **Contact Information:** Provide details on how to reach the team for support or contributions.
- Angela : [Github](https://github.com/AngelaLop) [Email](alopezsanchez@uchicago.edu)
- César  : [Github](https://github.com/cesarnunezh) [Email](cnunezh@uchicago.edu)
- Shahzaib : [Github](https://github.com/Shahzaib-Jamali) [Email](shahzaibjamali@uchicago.edu)
