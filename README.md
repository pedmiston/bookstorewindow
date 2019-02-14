# Bookstore Window

Search for books and view the results as in a store window.

## Development

Here are the steps to take to work on this project. These
steps were developed on a macOS with `homebrew` as a program
manager.

### Python environment

```bash
# Install pyenv and pipenv
brew install pyenv pipenv

# Activate pyenv to pin specific versions of python.
eval "$(pyenv init -)"

# Install the version of python.
pyenv install 3.7.1

# Use the version of python in this project.
pyenv local 3.7.1

# Create a virtual environment for the project.
# The packages and required version of python are listed in the Pipfile.
pipenv install --python 3.7.1 --dev
```

### User tests

The user tests use Selenium and a Chrome headless web driver.

```bash
# Install the required web drivers for user tests
brew cask install chromedriver
```

### Heroku

```bash
# Install the heroku command line tool
brew install heroku/brew/heroku

# Authenticate with the heroku client
heroku login

# List any running apps
heroku apps
```

## Configuring the local environment

Running the app locally requires the following environment variables:

* GOOGLE_API_KEY
* DEBUG

Run the "bin/setup-env.py" script in the project's virtualenv to create a
".env" file containing the required environment variables. The script will
prompt the user for the required environment variables and write them as
KEY=VALUE to an ".env" file. **The .env file is loaded by `pipenv` and
`heroku`.**

```bash
pipenv run bin/setup-env.py
```

## Running the app on a local server

```bash
# Activate the virtual environment, reading environment variables from the ".env" file.
pipenv shell

# Collect static files and apply DB migrations
./manage.py collectstatic
./manage.py migrate

# Run the app on the django development server
./manage.py runserver
```

## Run the app on a virtual server

```bash
# Run the app as a virtual heroku app, reading environment variables from the ".env" file.
heroku local
```

## Run the app on a Vagrant VM

```bash
# Requires: virtualbox, vagrant
vagrant box add geerlingguy/ubuntu1804
vagrant up
```

## Testing

The full test suite includes user tests, which use a Selenium
web driver to simulate user behavior, as well as unit tests.

**Note:** The full test suite requires a valid Google API Key. Requests are
made once and stored in plaintext using `betamax`. After running the tests once,
on subsequent runs, the cached responses are used instead. Although in theory
the cached responses could be committed to the repo as fixtures, the Google
API Key is included in the cached response, and therefore is not committed to
this repo, since it is public.

```
# Prerequisites
echo $GOOGLE_API_KEY
echo $DEBUG
./manage.py collectstatic

# Run tests
./manage.py test               # run all tests
./manage.py test user_tests    # run user tests only
./manage.py test window        # run unit tests for main app only
./manage.py test google_books  # run tests for connecting to google books
```

To run the user tests against a staging server:

```bash
# Start the heroku virtual machine
heroku local

# in a new terminal window
STAGING_SERVER=http://0.0.0.0:5000 pipenv run ./manage.py test user_tests
```

## Deploying the app with Heroku

```bash
# Creates a heroku machine and points a git remote to it
heroku apps:create

# If a Heroku app has already been created, set a git remote to point to it
heroku git:remote -a APPNAME

# Set the required virtual environment variables on the host machine.
heroku config:set GOOGLE_API=XXXXXXXX
heroku config:set SECRET_KEY=XXXXXXXX

# Deploy the app by pushing to the git remote heroku
git push heroku master:master

# Run the migration script on the heroku machine to initialize the DB tables.
heroku run python manage.py migrate
```

## Accessing the Postgres database

```bash
heroku pg:info  # view db info
heroku pg:psql  # jump into a db session
heroku pg:reset # reset the db
```

## Using the Google Books API

Using the Google Books API requires requires an API key, which was created via
the Google Developer Console.
