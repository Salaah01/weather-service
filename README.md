# Getting It Running
This documentation will get help you get you running with the Weather Service application on a Linux Ubuntu 18.04 machine.

## Development
**Update Package**
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
sudo apt install ostgresql postgresql-contrib
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

Install dependencies
```bash
pip install -r requirements.txt
```
Note: requirements.txt will install psycopg2 as the app has been build using a PostGreSQL database. If you are not using a PostGreSQL database, please pip install the appropriate package to work with your database system.

Run local server
```bash
python3 manage.py runserver 0.0.0.0:8000
```
If you have a problem running this command, checked ALLOWED_HOSTS in weather_service.settings include "localhost" in the list.