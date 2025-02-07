# crop_science

## Steps for deployment:

This application runs on python version 3.12.8.  Use pyenv to get your python version

- mkdir test_this_project
- git clone https://github.com/badavis15239/crop_science.git
- git clone https://github.com/corteva/code-challenge-template
- cd crop_science
- cp .env_example .env
- set -a; source .env; set +a (this sets env variables.  Note: this step isn't necessary when deploying in the cloud)
- mkdir postgres_data
- docker compose up -d (this will deploy local postgres and other resources.  It will also run sql code to create necessary permissions for api user and schemas)
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- cd ingestion
- python ingeston.py (this will load the data and set the schema for the api user.  Any additional runs will load data in the inactive schema and then swap the schema once the ingestion, indexes, dedups are complete)
- cd ../calculations
- python calc.py (this will do the calculations and put the data in schema_c)

## To run API

`docker-compose up -d`

## To run tests
- cd weather_api
- run tests using `python -m unittest discover`

## API Calls

http://0.0.0.0:5000/swagger

http://0.0.0.0:5000/api/weather/stats?page=1&per_page=100

http://0.0.0.0:5000/api/weather?page=1&per_page=10
