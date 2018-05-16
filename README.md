[![Build Status](https://travis-ci.org/Bonifase/WeConnect-.svg?branch=master)](https://travis-ci.org/Bonifase/WeConnect-)
[![Coverage Status](https://coveralls.io/repos/github/Bonifase/WeConnect-/badge.svg?branch=develop)](https://coveralls.io/github/Bonifase/WeConnect-?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/2e2b8561b617ae21d04d/maintainability)](https://codeclimate.com/github/Bonifase/WeConnect-/maintainability)


[![CircleCI](https://circleci.com/gh/Bonifase/WeConnect-/tree/develop.svg?style=svg)](https://circleci.com/gh/Bonifase/WeConnect-/tree/develop)
# WeConnect
WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with. 


The building blocks are:

* Python 3
* Flask
* PostgreSQL or MySQL

## Setting Up for Development

These are instructions for setting up WeConnect Flask app
in development environment.

* prepare directory for project code and virtualenv:

        $ mkdir -p ~/weconnect
        $ cd ~/weconnect

* prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):

        $ virtualenv --python=python3 wc-venv
        $ source wc-venv/bin/activate

* check out project code:

        $ git clone https://github.com/Bonifase/WeConnect-.git

* install requirements (Flask, ...) into virtualenv:

        $ pip install -r weconnect/requirements.txt

## Running the tests
1. Use nosetests to manually test the application
2. Navigate to the directory where the api folder is located using the terminal
3. Run the nosetests command in the terminal

## Deployment

1. Use Heroku for deployment. 
2. Sign up, Download and install the Heroku CLI and then upload our app to the platform effortlessly.
3. Login into the Heroku Cli by running this command in the terminal: heroku login
4. Add a Procfile to that application.
5. Update the requirements file by running: pip freeze > requirements.txt
6. Add this line of code: web: gunicorn app:app
7. In the application folder run this command: heroku create WeConnect-api-heroku.
8. WeConnect is the name of the application, this has to be unique across Heroku. 

## Built With

 * [Flask](http://flask.pocoo.org/)- The web framework used

 * [Bootstrap](https://getbootstrap.com/)- An open source toolkit for developing with HTML, CSS, and JS.


## Versioning

This is the first v1 

## Authors

* **Bonifase Orwa** - *Initial work* - [WeConnect](https://github.com/Bonifase/WeConnect-)

## License

This is a free open source application with no license

## Acknowledgments
* Bootstrap CDN
* LFAs
* Team members




