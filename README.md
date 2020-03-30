# Insurance [![CircleCI](https://circleci.com/gh/alvaropaco/py-nameco-flask-microservice.svg?style=svg)](https://circleci.com/gh/alvaropaco/py-nameco-flask-microservice) [![Maintainability](https://api.codeclimate.com/v1/badges/3fc099559a53bc7800d0/maintainability)](https://codeclimate.com/github/alvaropaco/py-nameco-flask-microservice/maintainability)

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

### Get Insurance risk

Just nedd to consume one endpoint to get the insurance risk prediction:

* Endpoint: <host>/insurance/risk
* Method: POST
* Payload: 
    ```json
        {
            "age": Int,
            "dependents": Int,
            "house": {"ownership_status": String},
            "income": Int,
            "marital_status": String,
            "risk_questions": Array<Int>,
            "vehicle": {"year": Int}
        }
    ```

* Response: 
    ```json
        { 
            "auto": String, 
            "life": String,
            "disability": String, 
            "home": String
        }
    ```

Simple http call to the service URL:

`curl -X POST 127.0.0.1:5000/insurance/risk -H "Content-Type: application/json" -d @data.example.json` 

### Testing 

Can run the API tests:

`docker run -it -v $(pwd):/app -p 5000:5000  api ./entrypoint.tests.sh`