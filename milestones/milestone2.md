# Andes-Indus Analytics

## Abstract

Early school dropout is a multifaceted challenge that impacts education systems and societal outcomes in both developed and developing countries. In the United States, this phenomenon varies notably across and within regions. For instance, Chicago public schools display a wide range of 9th-grade dropout rates, ranging from 0% to 56.6% (CDPS, 2024). While the influence of individual, family, and school characteristics is well documented, a growing body of studies has begun to explore the effects of broader social contexts on adolescent educational outcomes such as neighboorhood context crime or violence. This project aims to integrate, analyze, and visualize spatial, administrative, and demographic data to characterize school dropouts across Chicago schools, with a particular focus on the role of crime in shaping these educational outcomes. 

## Data Sources

### Data Reconciliation Plan

An important thing to do at this step is to have a plan for how data from your various sources will be brought together. 

For each data set, you will need to identify the "unique key" that will allow you to connect it to other data sets. (We'll discuss this in more detail.)

Additionally, for each data source, add a section like:

### Data Source #1: {Name}

### Data Source #1: { US Population Census - American Community Survey }

- URL to the data source:  https://www.census.gov/data/developers/data-sets/census-microdata-api.html
- Is the data coming from a webpage, bulk data, or an API?: Census API
- How many records (rows) does your data set have?
  The dataset consists of individual sample information from the 18 Public Use Microdata Areas (PUMAs) that make up the city of Chicago. PUMAs are statistical geographic areas used for tabulating and disseminating data from the American Community Survey (ACS) and the Puerto Rico Community Survey Public Use Microdata Sample (PUMS). They are also used for ACS period estimates and decennial census data. The dataset contains a sample of 18,244 individuals (rows) for the year 2023.
- How many properties (columns) does your data set have?
 For the initial analysis, we will retrieve data for 10 key variables:
  PUMA (Public Use Microdata Area)
  Race: RACBLK (Black), HISP (Hispanic), RACWHT (White)
  Age: AGEP (Population Age)
  Employment Status: ESR
  School Enrollment Status: SCH
  Household Income (Past 12 Months): HINCP
  Adjustment Factor for Income and Earnings Dollar Amounts: ADJINC
  Population Weights: PWGTP
  Additional variables may be considered in the next phase of the project.

  The JSON dictionary of variables can be found here: Census API Variable Dictionary. https://api.census.gov/data/2023/acs/acs1/pums/variables.json

- Write a few sentences about your exploration of the data set. At this point you should have downloaded some of the data and explored it with an eye for things that might cause issues for your project.
  We began exploring the dataset using the Census API via the link provided above, extracting the specified variables for each of the 18 PUMAs in Chicago.
  We ensured that the total population estimate aligns with Census records (2,664,493 people).
  We verified that the retrieved variables contain complete and consistent data for our analysis.
- Are there any challenges or uncertainity about the data at this point?: 
  At this stage, we have determined the lowest level of data disaggregation available and have not encountered any major challenges with the dataset.
  However, as we continue our exploration, one potential challenge may arise when working with data prior to 2020. The number of PUMAs changed from 18 to 19 after the 2020 Census, which could impact comparisons over time. If we decide to analyze historical data, we will need to account for this change.

### Data Source #2: {Chicago Crime Data}
- URL to the data source: Crime Data (https://dev.socrata.com/foundry/data.cityofchicago.ls/ijzp-q8t2) and Homicides Data (https://dev.socrata.com/foundry/data.cityofchicago.org/gumc-mgzr)
- Is the data coming from a webpage, bulk data, or an API?: Chicago City API
- How many records (rows) does your data set have?
    - Crime data: This data set has 8,247,404 crime records from 2001 to the last update (Jan 22th, 2025). 
    - Homicides Data: This data set has 61,046 homicides records from 1991 to the last update (Jan 28th, 2025).
- How many properties (columns) does your data set have?
    - Crime data: This data set has 22 columns from which we will use the following 11 variables for the analysis: Case Number, Date, Block, IUCR (code), Primary Type, Description, Arrest, Domestic, Community Area, Latitude, and Longitude.
    - Homicides: This data set has 38 columns from which we will use the following 10 variables for the analysis: Case Number, Date, Block, IUCR (code), Description, Community Area, District, Age, Latitude, and Longitude.
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

The data will be brought together using: the borders of the 18 PUMAS of the city of Chicago, creating a variable for each datatset where we can identify the PUMA each obervation (crime - school) belongs to. 

## Project Plan

## Preliminary Project Plan
<b>Census data management:</b> 

We will retrive data from the Census API. We have already verified the information is available for 18 Public Use Microdata Areas PUMA of the city (from 2021 onwards) for which we will calculate socieconomic indicators. Our primary focus is to characterize the city's PUMA's areas in terms of socioeconomic status, predominant ethnicity, school-aged population, and the percentage of NEET (Not in Education, Employment, or Training) youth. To achieve this, we will build spatial clustering indicators, which will require cleaning the collected data and constructing comparable, clustered integration variables to interoperate and merge with the rest of the datasets. This key variables will be code for each one of the 18 PUMAs to study.

<b>School data:</b> 

School locations will be mapped, and the data will be integrated with other spatial datasets, such as neighborhood demographics, and economic indicators. This integration will enable a more comprehensive understanding of the spatial distribution of school performance and the potential influence of contextual factors. To accurately analyze these spatial relationships, it is crucial to obtain precise and up-to-date longitudinal and latitudinal coordinates for all schools. This will facilitate the creation of accurate maps and enable the application of spatial analysis techniques, such as spatial clustering, to identify groups of schools with similar characteristics and understand the spatial patterns of school performance within the city

<b>Crime data:</b> 

We will use the City of Chicago's API (Crimes) which reflects reported incidents of crime (with the exception of murders) in the city from 2001 to present. This data set contains informatión about the location of the crime (at a block level), the type of crime (accordint to the Chicago Police Department), the description of the crime, indicates whether an arrest was made, and other information related to the crime. Our primary focus will be on computing an index of crime incidents in a neighborhood level, differenciating by type of crime and arrest. Also, the City of Chicago's API has another data source that maps the homicides and non-fatal shootings that can also give us more information to characterize the crime behavior in the city.

It is recommended that you:

- Identify required (and optional) components of the project to be built.
- Have a plan that makes it clear what will be built by Milestone #3 (it may be helpful to break this out weekly for the remainder of the quarter) and what will be built by the final project.
- For each component, identify who is primarily responsible, and who else might work on it with them.

## Project Components and Responsibilities

Required Components

1. Data Collection and Cleaning
  Census Data Responsible: [Angela, Support: [Cesar]
  Crime data: [Cesar, Support: [Shahzaib]
  Schools data: [Shahzaib, Support: [Angela]

2. Spatial Analysis and Mapping – Responsible: [Cesar], Support: [Shahzaib]

3. Statistical Analysis of Dropout and Crime Correlation – Responsible: [Angela], Support: [Cesar]

4. Visualization and Reporting – Responsible: [Angela], Support: [Cesar - Shahzaib]

Milestone #3 Plan

Week 1: Data collection and cleaning finalized

Week 2: Initial spatial mapping and visualization

Week 3: Preliminary correlation analysis between crime and dropout rates

Week 4: Refinement and preparation for final integration

Final Project Deliverables

A fully integrated dataset

Interactive maps and spatial visualizations

Statistical models explaining dropout rates

A final report

## Questions

A **numbered** list of questions for us to respond to.
