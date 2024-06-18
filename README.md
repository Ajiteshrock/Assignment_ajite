# Recipe API

### This project is a Flask-based Recipe API that allows users to create, read, update, and delete recipes. The project uses PostgreSQL as the database, Flask-RESTx for API documentation, and pytest for testing. The application is containerized using Docker.

## Table of Contents
### Project Setup
### Running the Application
### Testing the Application
### Project Structure
### Requirements
### Project Setup
### Prerequisites
### Ensure you have the following installed on your machine:

### Docker
### Docker Compose
### Git

### Cloning the Repository
### Clone the repository to your local machine:

### Docker Setup
### This project uses Docker and Docker Compose to manage dependencies and environment setup.

### Build Docker Images:
### docker-compose build

### Running the Application

### To start the application, use Docker Compose:
#### docker-compose up
#### This command will start the application and the PostgreSQL database. The API will be available at http://localhost:5000.

#### Testing the Application
#### Testing is handled by pytest with a detailed output. Tests are run in a separate Docker container to ensure isolation.

#### Build Docker Images for Testing:

#### docker-compose -f docker-compose-test.yml build
#### Run the Tests:

#### docker-compose -f docker-compose-test.yml up --abort-on-container-exit
#### This command will run the tests and provide detailed output, including coverage reports.

#### Requirements
Python Packages
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
Flask-RESTx
pytest
pytest-cov
Docker Images
Python:3.9
PostgreSQL:13


