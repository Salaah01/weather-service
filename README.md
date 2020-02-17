# Getting It Running
This documentation will get help you get you running with the Weather Service application on a Linux Ubuntu 18.04 machine.

## Development
**Update Package**
Update core Linux packages.
```bash
sudo apt update
sudo apt upgrade
```

## Install Python 3, PIP and Python Virtual Environment
```bash
sudo apt install python3-pip python3-dev python3-venv
```

## Install Database
We will be setting up the application to work on a PostgreSQL database. If you prefer to use a different database please skip this step. This application is built to be compatible with a sqlite3 database and so most database systems should work correctly with the application.

```
