# crm_agile

This project exposes some services to manage users and customers.

## Pre-view

You can use the url https://crm-agile.herokuapp.com/api/ to test the services. 

To check the endpoints documentation, go to https://crm-agile.herokuapp.com/admin/ and login with:
- user **admin**
- password **admin1234** 

Then go to https://crm-agile.herokuapp.com/api/docs/ to see the docs.

Yo can use the endpoint *GET* https://crm-agile.herokuapp.com/api/users/ using the admin user token *a5fbeb0da9be3a2e4ac5311b53993f98f4cace6e* to list all available users.

### How to authenticate?

You can use the services using a user Token. To athenticate the request, add the header **Authorization** with value **Token [TOKEN].**


# Run project in local

This repo contains all the required configuration files to run the server locally using Docker.
Follow the next steps:
- Clone this project
- Go to the project directory
- Create the Docker images using docker-compose:
  ```
  docker-compose -f docker-compose.yml up --build crm_agile
  ```
- It will run the server and expose it at localhost in port 8005
- Create a shell sesion inside the container to apply django migrations and create the django admin user
  ```
  docker exec -ti crm_agile bash
  python manage.py migrate
  python manage.py createsuperuser
  ```
- Use the user created to log-in into the django admin site http://localhost:8005/admin/. Then go to the endpoint documentation page to view the available services http://localhost:8005/api/docs/

# Run the tests

To run the application tests, start a shell sesion inside the container and excecute the django tests:
```
docker exec -ti crm_agile bash
python manage.py test
```

