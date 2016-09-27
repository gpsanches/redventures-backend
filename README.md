This is a skeleton for Tornado applications containing these features:

- Modularization;
- Settings for different environments (DEV, HOMOL, PROD);
- Database connection and ORM (SQLAlchemy) with mysql;
- REST APIs (Tornado-JSON);
- Logging;
- Celery;


Steps to install the app:

$ pip install virtualenv

$ mkdir /opt/redventures

$ cd /opt/redventures

$ virtualenv -p /usr/bin/python3.4 venv

$ source /opt/redventures/venv/bin/activate

$ git clone git@github.com:gpsanches/redventures-backend.git

$ cd redventures-backend

$ pip install -r requirements.txt

$ fab deploy


-----------------------------------------------------------------------

Samples with requests api to postman are in project root

file: redventures.postman_collection.json

-----------------------------------------------------------------------

------------------------------------
USERS
------------------------------------

GET

http://localhost:8888/users

http://localhost:8888/users/id/1

POST

http://localhost:8888/users

    body: {
             "name": "Guilherme",
             "gravatar": "http://www.gravatar.com/avatar/a51972ea936bc3b841350caef34ea47e?s=64&d=monsterid"
          }

------------------------------------
WIDGETS
------------------------------------

GET

http://localhost:8888/widgets

http://localhost:8888/widgets/id/1

http://localhost:8888/widgets/name/Test

POST

http://localhost:8888/widgets

    body: {
             "name": "Test",
             "color": "blue",
             "inventory": 123,
             "price": 10.90,
             "melts": true
          }

PUT

http://localhost:8888/widgets/id/1

    body: {
        "color": "red"
    }

DELETE

http://localhost:8888/widgets/id/7