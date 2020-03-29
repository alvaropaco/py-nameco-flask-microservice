# Insurance

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