# circulate-sd
OSL Data Collaboratory 2023: Circulate San Diego


## Running Docker commands

To build:
```
docker build -t csd-data .
```

To run:
```
docker run -p 4000:80 -v $(pwd):/app csd-data
```