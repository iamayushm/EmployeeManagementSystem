# EmployeeManagementSystem/ Flask application
Employee Management Web Application built using Flask and SQLAlchemy .This application supports two roles , Admin and Employee. An employee will register himself into organisation.Admin has rights to delete,update details of an employee.
There is an Api named search_microservice which returns Details of an employee based on given Name and Address.Api is secured using http authentication and only admin has rights to access this Api.

# Installtion
1) Python
2) Docker

# Running the application
### Deploy with docker compose
Clone the project and run the following command : <br/>
$ docker-compose up -d
Make sure that while running the command your docker-compose file is present in your working directory.

# Screenshots

## login
![GitHub Logo](https://github.com/iamayushm/EmployeeManagementSystem/blob/fbec0e89e97145b6190ea98afd382a11c35594e4/login.PNG)

## register
![GitHub Logo](https://github.com/iamayushm/EmployeeManagementSystem/blob/9f16c95e7f4b2c32072de102fccd44616e0b9100/register.PNG)

## Admin Screen and search form
![GitHub Logo](https://github.com/iamayushm/EmployeeManagementSystem/blob/b1984d6041c444ae9b79b49c0c638e74b7f4b118/Masterscreen.PNG)

## Reset Password
![GitHub Logo](https://github.com/iamayushm/EmployeeManagementSystem/blob/18a605eb62b4c90898db922a41646b164959e63f/ResetPassword.PNG)




