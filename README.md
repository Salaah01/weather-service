# Weather Service API

A HTTP service which provides an API to get a weather forecast for a given city in the UK.

The system uses [openweathermap](https://openweathermap.org/) as the data source.

The prevent needless calls to the data source, queries will not directly send a query to a the data source, rather it will attempt to fetch the data from a database. If the data does not exist, the the system will request data from the data source and store it into the database before returning it to the user.

## The Service

### `ping`
A simple health check to ensure that the service is running. It also provides information about the application.
```bash
$ curl -si http://localhost:8080/ping

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
  "name": "weatherservice",
  "status": "ok",
  "version": "1.0.0"
}
```
### `/forecast/<city>`
This endpoint allows a user to request a breakdown of the current weather for a specific city. The includes a description of the cloud cover, the humidity as a percentage, the pressure in hecto Pascals (hPa), and temperature in Celsius.

For example fetching the weather data for London should look like this:

```bash
$ curl -si http://localhost:8080/forecast/london/

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "clouds": "broken clouds",
    "humidity": "66.6%",
    "pressure": "1027.51 hPa",
    "temperature": "14.4C"
}
```
### Errors
When no data is found or the endpoint is invalid the service responds with `404` status code and an appropriate message:

```bash
$ curl -si http://localhost:8080/forecast/westeros

HTTP/1.1 404 Not Found
Content-Type: application/json; charset=utf-8
{
    "error": "Cannot find country 'westeros'",
    "error_code": "country not found"
}
```

Similarly invalid requests should return a `400` status code:

```bash
$ curl -si http://localhost:8080/forecast

HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
{
    "error": "no city provided",
    "error_code": "invalid request"
}
```
If anything else goes wrong the service responds with a 500 status code and a message that doesn't leak any information about the service internals:

```bash
$ curl -si http://localhost:8080/forecast/london

HTTP/1.1 500 Internal Server Error
Content-Type: application/json; charset=utf-8
{
    "error": "Something went wrong",
    "error_code": "internal server error"
}
```

# Getting It Running

This documentation will get help you get you running with the Weather Service application on a Linux Ubuntu 18.04 machine.

## Development

### Update Packages

Update core Linux packages.

```bash
sudo apt update
sudo apt upgrade
```

### Install Python 3, PIP and Python Virtual Environment

```bash
sudo apt install python3-pip python3-dev python3-venv
```

### Install Database

We will be setting up the application to work on a PostgreSQL database. If you prefer to use a different database please skip this step. This application is built to be compatible with a sqlite3 database and so most database systems should work correctly with the application.

```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```

#### Create Database

```sql
CREATE DATABASE weather_service;
CREATE USER <DB_USERNAME> WITH PASSWORD '<DB_PASSWORD>';
ALTER ROLE dbadmin SET client_encoding TO 'utf8';
ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbadmin SET timezone TO 'GMT';
```

#### Give Access Rights to Database

```sql
GRANT ALL PRIVILEGES ON DATABASE weather_service TO <DB_USERNAME>;
\q
```

### Environment Set Up

Create project directory

```bash
mkdir apps
cd apps
```

Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Clone Git repository. For example:

```bash
git clone https://github.com/yourgithubname/weather_service.git
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Note: this command will install psycopg2 as the app has been build using a PostGreSQL database. If you are not using a PostGreSQL database, please pip install the appropriate package to work with your database system.

If this is the case, after running the command, run `pip uninstall psycopg2` to uninstall psycopg2 from your system.

### Set up environment variables

Sensitive details are retrieved from the OS environment variable.
The following environment variables will need to to set up.
To set up an environment variable:

```bash
export NAME=VALUE
```

The following environments will need to be set up:
| Name | Value | Variable |
| --------- | ------------- | -------- |
| WEATHER_SERVICE_SECRET_KEY | Secret key for application | settings.SECRET_KEY |
| DB_ENGINE | Database engine | settings.DATABASES['default']['engine'] |
| DB_HOST | Database host | settings.DATABASES['default']['host'] |
| DB_USER | Database user | settings.DATABASES['default']['user'] |
| DB_PASSWORD | Database password | settings.DATABASES['default']['password'] |
| DB_NAME | Database name | settings.DATABASES['default']['name'] |

Please note that `WEATHER_SERVICE_SECRET_KEY` can be obtained by [signing up](https://home.openweathermap.org/users/sign_up) for a free API key from [openweathermap](https://www.openweathermap.org/).

### Run local server

```bash
python3 manage.py runserver 0.0.0.0:8000
```

This will allow you to visit the site by visitng http://localhost:8000/
A JSON response is expected indicating a 404 response. If you are getting a server error however, check `ALLOWED_HOSTS` in weather_service.settings includes "localhost" in the list.

### Logging into the admin site

navigate to `/admin` where you will be able to log in to the admin section. If there is any issue displaying the page, stop the server `Ctrl + C` and run `python3 manage.py runserver --insecure`. Or, set `DEBUG=True` in the settings.
Please note that you must turn `DEBUG=False` before deploying to production.

## Testing

To run unittests, run `python3 manage.py test`.
