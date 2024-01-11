# Circulate San Diego: Infrastructure Data Explorer

## About

### OSL Data Collaboratory
This project is part of the Open Spatial Lab's 2023 Data Collaboratory. The Collaboratory is a 6-month program where OSL engages with social impact organizations to build a customized tool for data management, analysis, communication, and visualization. Circulate San Diego’s organizational engagement and feedback directly informs this work. 

Based at the University of Chicago Data Science Institute, the Open Spatial Lab creates open source data tools and analytics to solve problems using geospatial data science. Read more about OSL at https://datascience.uchicago.edu/research/open-spatial-lab/. 

### Project Scope
**About**: Circulate San Diego works to create excellent mobility choices and vibrant, healthy neighborhoods in the San Diego region. They have promoted public transit, safe streets, and sustainable growth since their founding in 2014. 

**Project**: OSL worked with Circulate San Diego to develop an interactive mapping and data platform that integrates CSD’s community infrastructure and safety audit data with the City of San Diego’s 311 data and demographic information at multiple spatial scales. Circulate San Diego will use this tool to identify insights into where safety or infrastructures issues have persisted over time and which communities are most impacted to advocate for policy changes. 

## Repo & Data

This repo contains raw and compressed data used in this project, devop scripts, and the github page preview file. 

`data` folder contains publicly available data and community data collected made available by Circulate San Diego. 
Public data includes:
- `community vars` community socioeconomic variables from [ACS 2021 5-year data via Social Explorer](https://www.socialexplorer.com/tables/ACS2021_5yr)
- `geo` spatial data boundaries. Tracts and Zip Codes (ZCTAs) from [US Census geo/TigerLine 2021 shapefiles](https://www2.census.gov/geo/tiger/GENZ2021/shp/)
- Community Planning Districts boundaries (updated 2024) via [City of San Diego Open Data Portal - Community Planning Districts](https://data.sandiego.gov/datasets/community-planning-district-boundaries/)
- City Council Districts boundaries (updated 2021) via [City of San Diego Open Data Portal - City Council Districts](https://data.sandiego.gov/datasets/city-council-districts/)
- `walk audits` contains Circulate San Diego program data. Walk audits are conducted throughout the year by Circulate San Diego staff in collaboration with community members to document and track pedestrian safety and infrastructure needs in San Diego neighborhoods.
- `CSD Walk Audit Data Consolidation.csv` file contains a crosswalk to standardize label name conventions of Circulate's walk audits. For example, 'Broken/Narrow Sidewalks' and 'Broken/Uneven Sidewalks' and 'Broken/narrow Sidewalk' are all crosswalked and standardized to 'Broken Sidewalk' for the purpose of calculating summary statistics and data visualization. 
- `get it done 2021-2023` contains data from the [Get it Done program](https://www.sandiego.gov/get-it-done), San Diego's 311 service. We pulled all service requests from 2021, 2022, and 2023 (as of Aug 2023) from their public data portal. 

## Technical

### Running Docker commands

To build:
```
docker build -t csd-data .
```

To run:
```
docker run -p 4000:80 -v $(pwd):/app csd-data
```
