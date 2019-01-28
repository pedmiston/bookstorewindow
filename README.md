# Bookstore Window

Search for books and view the results as in a store window.

## Development

Here are the steps to take to work on this project. These
steps were developed on a macOS with `homebrew` as a program
manager.

```bash
# Install required programs
brew install pyenv pipenv heroku/brew/heroku postgres

# Authenticate with the heroku client
heroku login

# Activate pyenv to pin specific versions of python
eval "$(pyenv init -)"

# Create a virtual environment for the project.
# The packages and required version of python are listed in the Pipfile.
pipenv install --dev
```

## Configuring the local environment

The following command runs the setup-env.py script in the project's
virtualenv. The setup-env.py script will prompt the user for the required
environment variables and write them as KEY=VALUE to a ".env" file.
**The .env file is loaded by `pipenv` and `heroku`.**

```bash
pipenv run bin/setup-env.py
```

## Running the app on a local server

```bash
# Activate the virtual environment, reading environment variables from the ".env" file.
pipenv shell

# Run the app on the django development server
./manage.py runserver
```

## Run the app on a virtual server

```bash
# Run the app as a virtual heroku app, reading environment variables from the ".env" file.
heroku local
```

## Testing

Run all of the tests, including user tests, which use a selenium
web driver to simulate user behavior.

```
./manage.py test
./manage.py test user_tests  # run user tests only
./manage.py test window      # run unit tests for main app only
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
heroku create

# Set the required virtual environment variables on the host machine.
heroku config:set GOOGLE_API=XXXXXXXX

# Deploy the app by pushing to the git remote heroku
git push heroku master:master

# Run the migration script on the heroku machine to initialize the DB tables.
heroku run python manage.py migrate
```

## Accessing the Postgres database

```bash
heroku pg:info
heroku pg:psql
```

## Using the Google Books API

Using the Google Books API requires requires an API key, which was created via
the Google Developer Console.
