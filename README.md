# Circulate San Diego: Infrastructure Data Explorer

## About

### OSL Data Collaboratory
This project is part of the Open Spatial Lab's 2023 Data Collaboratory. The Collaboratory is a 6-month program OSL engages with social impact organizations to build a customized tool for data management, analysis, sharing, and visualization. Circulate San Diego’s organizational engagement and feedback directly informed this work. 

### Project Scope
**About**: Circulate San Diego works to create excellent mobility choices and vibrant, healthy neighborhoods in the San Diego region. They have promoted public transit, safe streets, and sustainable growth since their founding in 2014. 

**Project**: OSL worked with Circulate San Diego to develop an interactive mapping and data platform that integrates CSD’s community infrastructure and safety audit data with the City of San Diego’s 311 data and demographic information at multiple spatial scales. Circulate San Diego will use this tool to identify insights into where safety or infrastructures issues have persisted over time and which communities are most impacted to advocate for policy changes. 

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
