# Andes-Indus Analytics

## Members

- Shahzaib Jamali <shahzaibjamali@uchicago.edu>
- Angela López <alopezsanchez@uchicago.edu>
- César Núñez <cnunezh@uchicago.edu>

## Abstract
100-200 words explaining the general idea for your project.  Be sure to read the project requirements and consider how you'll incorporate the various components.  These details can change as much as needed over the next few weeks, but we want to take a look at what's being considered.

Early school dropout is a multifaceted challenge that impacts education systems and societal outcomes in both developed and developing countries. In the United States, this phenomenon varies notably across and within regions. For instance, Chicago public schools display a wide range of 9th-grade dropout rates, ranging from 0% to 56.6% (CDPS, 2024). While the influence of individual, family, and school characteristics is well documented, a growing body of studies has begun to explore the effects of broader social contexts on adolescent educational outcomes such as neighboorhood context crime or violence. This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes.  

## Preliminary Data Sources

The project will use and integrate 3 main data sources: Demographic data from the 2020 population Cesus; Administrative School data and Crime data.

### Data Source #1: { US Population Census - American Community Survey }

- URL to the data source: https://www.census.gov/data/developers/data-sets/census-microdata-api.html
- Is the data coming from a webpage, bulk data, or an API?: Census API
- Are there any challenges or uncertainity about the data at this point?: Yes, the microdata geography is the public use for certain areas we havent fully mapped Chicago.

### Data Source #2: {Chicago Crime and Homicides Data}
- URL to the data source: Crime Data (https://dev.socrata.com/foundry/data.cityofchicago.org/ijzp-q8t2) and Homicides Data (https://dev.socrata.com/foundry/data.cityofchicago.org/gumc-mgzr)
- Is the data coming from a webpage, bulk data, or an API?: Chicago API
- Are there any challenges or uncertainity about the data at this point?: None we have thougth of at this point

### Data Source #3: {Chicago Public Schools Administrative Records}
- URL to the data source: https://www.cps.edu/about/district-data/metrics/ 
- Is the data coming from a webpage, bulk data, or an API?: Administrative Records - Bulk data
- Are there any challenges or uncertainity about the data at this point?: How to Map Schools (Locations)

## Preliminary Project Plan

A short summary of what components of the project might be needed (e.g. data ingestion, cleaning/preparation, visualization).
Census data management: Angela 
We will gather data from the Census API and verify that the information is available at the neighborhood level within the city (or undertand the lowest dissagregation level). Our primary focus is to characterize the city's neighborhoods (or the lowest disaggregation level) in terms of socioeconomic status, predominant ethnicity, school-aged population, and the percentage of NEET (Not in Education, Employment, or Training) youth. To achieve this, we will build spatial clustering indicators, which will require cleaning the collected data and constructing comparable, clustered integration variables to interoperate and merge with the rest of the datasets.

School data: Shahzaib
<<<<<<< HEAD
School locations will be mapped, and the data will be integrated with other spatial datasets, such as neighborhood demographics, and economic indicators. This integration will enable a more comprehensive understanding of the spatial distribution of school performance and the potential influence of contextual factors.

To accurately analyze these spatial relationships, it is crucial to obtain precise and up-to-date longitudinal and latitudinal coordinates for all schools. This will facilitate the creation of accurate maps and enable the application of spatial analysis techniques, such as spatial clustering, to identify groups of schools with similar characteristics and understand the spatial patterns of school performance within the city

Crime data: Cesar
=======
>>>>>>> cesar

Crime data: Cesar
We will use the City of Chicago's API (Crimes) which reflects reported incidents of crime (with the exception of murders) in the city from 2001 to present. This data set contains informatión about the location of the crime (at a block level), the type of crime (accordint to the Chicago Police Department), the description of the crime, indicates whether an arrest was made, and other information related to the crime. Our primary focus will be on computing an index of crime incidents in a neighborhood level, differenciating by type of crime and arrest. Also, the City of Chicago's API has another data source that maps the homicides and non-fatal shootings that can also give us more information to characterize the crime behavior in the city.

## Questions

A **numbered** list of questions for us to respond to.
