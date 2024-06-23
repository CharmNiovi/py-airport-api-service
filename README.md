# py-airport-api-service
Airport API Service is an API service for processing airport data. It contains functionality for retrieving, updating and deleting information about various airports and orders.

## Installing / Getting started
[Python 3.10](https://github.com/python/cpython/tree/3.10) or later

[PostgreSQL 16](https://github.com/postgres/postgres/tree/REL_16_STABLE)


There is also an option to run via [docker-compose](https://github.com/docker/awesome-compose)


### Installation instructions
#### Via docker-compose
* Configure the `.env` file using the example of `.env_example`
* Build `docker-compose.yaml` and run

#### Manual
* Create and activate a virtual environment
* Configure the `.env` file using the example of `.env_example` and activate it
* Execute `runserver.sh` file to migrate db schema, createsuperuser and run server

## Developing

To develop in debug mode, you need to specify `DEBUG=False` in `.env`

To test app run:
```shell
./manage.py test
```

## Contributing

When you publish something as open source, one of the 
biggest motivations is that anyone can just jump in 
and start contributing to your project.

In addition, this project is licensed under the WTFPL,
which gives you a lot of freedom to use and modify the software. 
If you would like to contribute, please branch the repository and 
use the functionality branch. We warmly welcome pull requests.


## Licensing

"The code in this project is licensed under WTFPL license."
