# Insurance [![CircleCI](https://circleci.com/gh/alvaropaco/py-weather-micro-service.svg?style=svg)](https://circleci.com/gh/alvaropaco/py-weather-micro-service) [![Maintainability](https://api.codeclimate.com/v1/badges/3fc099559a53bc7800d0/maintainability)](https://codeclimate.com/github/alvaropaco/py-weather-micro-service/maintainability)

Insurance microservice implementation to predict the client profile based on risk metrics.

### Requeriments

* Docker I/O

### Building

Firstly we need to build the docker image:

`docker build -t api .` 

### Running

Run command will push up the micro-service:

`docker run -it -v $(pwd):/app -p 5000:5000  api ./entrypoint.sh` 

### Usage

Simple http call to the service URL:

`curl -X POST 127.0.0.1:5000/insurance/risk -H "Content-Type: application/json" -d @data.example.json` 

### Testing 

Can run the API tests:

`docker run -it -v $(pwd):/app -p 5000:5000  api ./entrypoint.tests.sh`