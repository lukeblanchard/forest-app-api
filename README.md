# forest-app-api

## Getting Started 
The instructions below will get the project up and running on your local machine 

### Prerequisites
You need both Docker and Docker Compose 

### Installing
Once you have installed Docker and Docker compose, change to the root directory of the project and build the app image with the following command 
```
docker-compose build
```

### Running tests and lint 
If this is your first time running the app, you will need to apply migrations to your local database with the following command
```
docker-compose run --rm app sh -c "python manage.py migrate"
```

To execute tests and linting, run the following command
```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

### Running the App 
After successfully building the image, run the following command, from the root directory, to start the app
```
docker-compose up
```


Navigate to http://127.0.0.1:8000/api/forest/ and you will see a list of API endpoints displayed in the Django admin interface