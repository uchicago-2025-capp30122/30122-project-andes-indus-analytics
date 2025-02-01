# Andes-Indus Analytics

## Abstract

Early school dropout is a multifaceted challenge that impacts education systems and societal outcomes in both developed and developing countries. In the United States, this phenomenon varies notably across and within regions. For instance, Chicago public schools display a wide range of 9th-grade dropout rates, ranging from 0% to 56.6% (CDPS, 2024). While the influence of individual, family, and school characteristics is well documented, a growing body of studies has begun to explore the effects of broader social contexts on adolescent educational outcomes such as neighboorhood context crime or violence. This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes. 

## Data Sources

### Data Reconciliation Plan

An important thing to do at this step is to have a plan for how data from your various sources will be brought together. to discuss on Thursday

For each data set, you will need to identify the "unique key" that will allow you to connect it to other data sets. (We'll discuss this in more detail.)

Additionally, for each data source, add a section like:

### Data Source #1: {Name}

### Data Source #1: { US Population Census - American Community Survey }

- URL to the data source: https://www.census.gov/data/developers/data-sets/census-microdata-api.html
- Is the data coming from a webpage, bulk data, or an API?: Census API
- How many records (rows) does your data set have?
- How many properties (columns) does your data set have?
- Write a few sentences about your exploration of the data set. At this point you should have downloaded some of the data and explored it with an eye for things that might cause issues for your project.
- Are there any challenges or uncertainity about the data at this point?: Yes, the microdata geography is the public use for certain areas we havent fully mapped Chicago.

### Data Source #2: {Chicago Crime Data}
- URL to the data source: Crime Data (https://dev.socrata.com/foundry/data.cityofchicago.ls/ijzp-q8t2) and Homicides Data (https://dev.socrata.com/foundry/data.cityofchicago.org/gumc-mgzr)
- Is the data coming from a webpage, bulk data, or an API?: Chicago City API
- How many records (rows) does your data set have?
    - Crime data: from 2001 to the last update (Jan 22th, 2025) there are 8,247,404 records in the database. 
    - Homicides Data: from 1991 to the last update (Jan 28th, 2025) there are 61,046 records in the database.
- How many properties (columns) does your data set have?
    - Crime data: It has 22 columns such as ID, Case Number, Date, Block, IUCR (code), Primary Type, Description, Location Description, Arrest, Domestic, Beat, District, Ward, Community Area, FBI Code, X Coordinate, Y Coordinate, Latitude, and Longitude.
    - Homicides: It has 38 columns such as Case Number, Date, Block, IUCR (code), Description, Zip code, Ward, Community Area, District and Age.
- Write a few sentences about your exploration of the data set. At this point you should have downloaded some of the data and explored it with an eye for things that might cause issues for your project.
    - Crime data: There are some missing values for latitude and longitude (and other columns) for some records in every year. From a sample of 100,000 entries, the percentage of records that has missing values for latitude and longitude is between 0.005% (2023-2025) to 1.9% (2021).
    - Homicides: In this data set the variables with significant missing values are those related to victim's personal identity, which is not relevant for our application. All the other variables has less than 0.1%
- Are there any challenges or uncertainity about the data at this point?: None we have thougth of at this point

### Data Source #3: {Chicago Public Schools Administrative Records}
- URL to the data source: https://www.cps.edu/about/district-data/metrics/ 
- Is the data coming from a webpage, bulk data, or an API?: Administrative Records - Bulk data
- The data source is coming from Bulk data and is in csv format.
- How many records (rows) does your data set have?
- The data spans 152 rows, with each row representing a different school.
- How many properties (columns) does your data set have?
- Graduation and Dropout Rates (2017–2024) :The dataset consists of eight columns for both graduation and dropout rates, with each  column representing a year from 2017 to 2024. In addition to these rates, the data also includes the total number of graduates, the number of dropouts, and the number of students in the 9th-grade cohort for each corresponding year.
- Write a few sentences about your exploration of the data set. At this point you should have downloaded some of the data and explored it with an eye for things that might cause issues for your project.
- The dataset provides comprehensive information on graduation and dropout rates for the period between 2017 and 2024. Data is available for most columns; however, it is important to note that some schools ceased operations during this period, and certain schools lack data for the initial years of the timeframe.
- Are there any challenges or uncertainity about the data at this point?: How to Map Schools (Locations)
- An online locator tool is available; however, there is no dedicated data source from which the precise latitude and longitude coordinates of the schools can be extracted. Therefore, it is necessary to engage in a discussion regarding geocoding procedures to obtain accurate location data.


## Project Plan

## Preliminary Project Plan
<b>Census data management:</b> 

We will gather data from the Census API and verify that the information is available at the neighborhood level within the city (or undertand the lowest dissagregation level). Our primary focus is to characterize the city's neighborhoods (or the lowest disaggregation level) in terms of socioeconomic status, predominant ethnicity, school-aged population, and the percentage of NEET (Not in Education, Employment, or Training) youth. To achieve this, we will build spatial clustering indicators, which will require cleaning the collected data and constructing comparable, clustered integration variables to interoperate and merge with the rest of the datasets.

<b>School data:</b> 

School locations will be mapped, and the data will be integrated with other spatial datasets, such as neighborhood demographics, and economic indicators. This integration will enable a more comprehensive understanding of the spatial distribution of school performance and the potential influence of contextual factors. To accurately analyze these spatial relationships, it is crucial to obtain precise and up-to-date longitudinal and latitudinal coordinates for all schools. This will facilitate the creation of accurate maps and enable the application of spatial analysis techniques, such as spatial clustering, to identify groups of schools with similar characteristics and understand the spatial patterns of school performance within the city

<b>Crime data:</b> 

We will use the City of Chicago's API (Crimes) which reflects reported incidents of crime (with the exception of murders) in the city from 2001 to present. This data set contains informatión about the location of the crime (at a block level), the type of crime (accordint to the Chicago Police Department), the description of the crime, indicates whether an arrest was made, and other information related to the crime. Our primary focus will be on computing an index of crime incidents in a neighborhood level, differenciating by type of crime and arrest. Also, the City of Chicago's API has another data source that maps the homicides and non-fatal shootings that can also give us more information to characterize the crime behavior in the city.

It is recommended that you:

- Identify required (and optional) components of the project to be built.
- Have a plan that makes it clear what will be built by Milestone #3 (it may be helpful to break this out weekly for the remainder of the quarter) and what will be built by the final project.
- For each component, identify who is primarily responsible, and who else might work on it with them.

## Questions

A **numbered** list of questions for us to respond to.