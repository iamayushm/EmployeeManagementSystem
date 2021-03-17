# EmployeeManagementSystem/ Flask application
This application supports two roles , Admin and Employee. An employee will register himself into organisation.Admin has rights to delete,update details of an employee.
There is an Api named search_microservice which returns Details of an employee based on given Name and Address.Api is secured using http authentication and only admin has rights to access this Api.

# Running the application
### deploy with docker compose
Clone the project and run the following command :
$ docker-compose up -d
