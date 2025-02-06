# crop_science

## Steps for deployment:

This application runs on python version 3.12.8.  Use pyenv to get your python version

- git clone https://github.com/badavis15239/crop_science.git
- cd crop_science
- cp .env_example .env
- mkdir postgres_data
- docker compose up -d (this will deploy local postgres and other resources.  It will also run sql code to create necessary permissions for api user and schemas)
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python /ingeston/ingeston.py (this will load the data and set the schema for the api user.  Any additional runs will load data in the inactive schema and then swap the schema once the ingestion, indexes, dedups are complete)
- python /calculations/calc.py (this will do the calculations and put the data in schema_c)
- To query the api go to http://127.0.0.1/swagger