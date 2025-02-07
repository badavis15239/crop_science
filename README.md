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

## To run tests
- cd weather_api
- run tests using `python -m unittest discover`

## API Calls

http://0.0.0.0:5000/swagger

http://0.0.0.0:5000/api/weather/stats?page=1&per_page=100

http://0.0.0.0:5000/api/weather?page=1&per_page=10

####  Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.

````
There are many tools I could use for data ingestion:
	- Airflow -- schedule the tasks and run them pulling data from s3 buckets
	- Lambdas can be set to cron tasks however, there is a 15 minute timeout that could limit larger datasets
	- AWS Batch can be used to spin up fargate instances for ingestion.
	- ECS can be used to spin up single tasks and run them like cron tasks
	- Triggers can be set to trigger EKS pods to run the tasks as well.  For example, orchestration with SQS

If I were to deploy this code (API) there are also several options:
	- because this is a simple api with read only and no computation -- API Gateway/Lambda would be the cheapest approach
	- ECS and EKS could also be used but for a simple microservice like this--it could be overkill unless you plan to add more to the service over time
	- You could deploy it on EC2 however, it's best to put it on ECS or EKS for scaling

If you were to deploy databases:
	- self hosted databases on EC2 however, there is a lot of maintenance invovled with it
	- RDS, Documentdb, Redshift (all of these are managed AWS services) - These are easier to maintain and have routine backups

Secrets -- 
	- Secrets manager
	- hashicorp vault
	- pick your poison

CICD -- 
	- codebuild/codepipeline 
	- Jenkins
	- Circleci
	- Github actions (runner could be self hosted on ECS or EKS)
	- again -- pick your poison.  I have worked with all of these.

```

