# Understanding School Dropouts in Chicago: The Role of Crime and Socioeconomic Factors

## Project Overview

This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes.By running the application, you will be able to explore these factors and their relationships on an interactive dashboard.

---

## Data Documentation

### 1. U.S. Census Data - American Community Survey
- *Source:* [U.S. Census Bureau](https://www.census.gov/programs-surveys/acs)
- *Description:* This dataset provides demographic data extracted from the U.S. Census Bureau’s American Community Survey. No API key is required for access.

### 2. Chicago Crime Data - City of Chicago
- *Crime Data:* [City of Chicago Crime Data](https://data.cityofchicago.org/Public-Safety/Crimes-Map/mw69-m6xi)
- *Homicide Data:* [City of Chicago Homicide Data](https://data.cityofchicago.org/Public-Safety/Homicides/ijzp-q8t2)
- *Description:* This dataset includes crime and homicide statistics for the City of Chicago. No API key is required for access.

### 3. Education Data - Chicago Public Schools
- *School Search:* [CPS Typeahead School Search](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-TypeaheadSchoolSearch_SearchValue)
- *School Profile:* [CPS Single School Profile](https://api.cps.edu/schoolprofile/Help/Api/GET-CPS-SingleSchoolProfile_SchoolID)
- *Description:* This dataset contains school-related information such as attendance rate, graduation rate, school address, and geographical coordinates (longitude and latitude). No API key is required for access.
- *School Metrics:* [CPS Dropout Data](https://www.cps.edu/about/district-data/metrics/)
- *Description:* This excel data set contains information pertaining to the dropout rate of schools for multiple years.

### Data Gaps & Challenges
- **Gaps:** 
    - Crime: 
    - Education : The data for school location and profile was only available for current year. Secondly, data for dropout
    and attendace were available from two different source types, excel and APIs.
    - Census
- **Quality Issues:** Describe inconsistencies, outliers, or other data quality challenges.

- **Mitigation Strategies:** Explain how these issues were addressed.
    - Crime : 
    - Education : We created two seperate csv files from the two sources and merged the data to make it comparable and accessible.
    - Census :

### Data Flow and Project Structure

- **Overview:** Explain how data is ingested, processed, and output.
- **Diagram:**  

![Structure](Datapipeline.png)

---

## Project Structure

### Overview
- Provide a brief description of the project layout and its modular design.

### Modules and Their Functions
- **Module A:**  
- *Purpose:* Explain what this module does.  
- *Key Components:* List functions or classes.
- **Module B:**  
- *Purpose:* Describe its functionality.  
- *Key Components:* List major elements.
- *(Add more modules as applicable.)*


## Team Responsibilities

### Team Member Contributions
- **Team Member 1 (Angela Lopez):**   
  - *Responsibilities:* 

    - Data Collection: Pulled data from the census API. API-Get.py
    - Data Cleaning: Created functions for cleaning census data. census_utils.py
    - Data Engineering/Database: 
    - Data Visualization: Creating graphs for demoraphic and attendace rate. figures.py

- **Team Member 2 (César Núñez):**  
  - *Responsibilities:* 

    - Data Collection:
    - Data Cleaning:
    - Data Engineering/Database
    - Data Visualization: 

- **Team Member 3 (Shahzaib Jamali):**  
  - *Responsibilities:* 

    - Data Collection: Pulled data from CPS APIs and accessed Dropout data from excel file 
    - Data Cleaning: Cleaned the data for education and merging API data and excel data. Education.py
    - Data Engineering/Database: 
    - Data Visualization:


### Collaboration Notes

The team coordinated its efforts by establishing a clear version control strategy. Each member worked on an individual branch within the repository, allowing for independent development of features and updates. All changes were communicated through commits from these branches into a centralized main branch, ensuring that updates were systematically integrated and the project's progress remained transparent..

---

## Final Thoughts

### Project Goals vs. Outcomes
- **Intended Goals:** 
The intended goal of our project was to provide a comprehensive analysis of crime and education trends across Chicago. By integrating diverse datasets—from community demographics and crime statistics to detailed educational metrics—our goal was to equip policymakers, community leaders, and educators with actionable insights. These insights can drive data-driven decisions, improve resource allocation, enhance community safety, and foster educational improvements across various neighborhoods in Chicago.
- **Outcomes:** 
We discovered that merging community, crime, and education data required extensive cleaning and normalization, and we had to make certain assumptions to reconcile differences. For example, we assumed that the number of schools remained constant over the three years of analysis, an approximation necessary to align the education data. This experience underscored the complexity of working with disparate data sources and highlighted the importance of careful data management and assumption testing in multi-source analysis
- **Lessons Learned:** 
Integrating data from the community survey, crime data, and educational metrics proved more challenging than anticipated. We had to invest significant effort into cleaning and normalizing the datasets, and key assumptions—such as treating the number of schools as constant over three years—were necessary to merge the information. This experience underscored the complexities of working with disparate data sources. Key takeaways include the need for careful planning around data integration, transparent documentation of assumptions, and iterative validation to maintain data accuracy. For future improvements, developing more robust methods for handling temporal variations and automating parts of the integration process could help streamline the workflow and enhance overall data fidelity.

---

- **Contact Information:** Provide details on how to reach the team for support or contributions.
- Angela : [Github](https://github.com/AngelaLop) [Email](alopezsanchez@uchicago.edu)
- César  : [Github](https://github.com/cesarnunezh) [Email](cnunezh@uchicago.edu)
- Shahzaib : [Github](https://github.com/Shahzaib-Jamali) [Email](shahzaibjamali@uchicago.edu)
