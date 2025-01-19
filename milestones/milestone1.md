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

### Data Source #2: {Chicago Crime Data}
- URL to the data source: https://www.chicagopolice.org/statistics-data/data-requests/
- Is the data coming from a webpage, bulk data, or an API?: Chicago Police Depertment API
- Are there any challenges or uncertainity about the data at this point?: None we have thougth of at this point

### Data Source #3: {Chicago Public Schools Administrative Records}
- URL to the data source: https://www.cps.edu/about/district-data/metrics/ 
- Is the data coming from a webpage, bulk data, or an API?: Administrative Records - Bulk data
- Are there any challenges or uncertainity about the data at this point?: How to Map Schools (Locations)

## Preliminary Project Plan

A short summary of what components of the project might be needed (e.g. data ingestion, cleaning/preparation, visualization).
Cesus data management: Angela 
We will gather data from the Census API and verify that the information is available at the neighborhood level within the city (or undertand the lowest dissagregation level). Our primary focus is to characterize the city's neighborhoods (or the lowest disaggregation level) in terms of socioeconomic status, predominant ethnicity, school-aged population, and the percentage of NEET (Not in Education, Employment, or Training) youth. To achieve this, we will build spatial clustering indicators, which will require cleaning the collected data and constructing comparable, clustered integration variables to interoperate and merge with the rest of the datasets.

School data: Shahzaib
Crime data: Cesar

This can be very brief, and will almost certainly change by the next milestone.

## Questions

A **numbered** list of questions for us to respond to.
