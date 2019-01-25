# Bookstore Window

Search for books and view the results as in a store window.

## Development

Here are the steps to take to work on this project. These
steps were developed on a macOS with homebrew as a program
manager.

```bash
# Install required programs
brew install pyenv

# Activate pyenv to pin specific versions of python
eval "$(pyenv init -)"

# Install the required python packages in a virtual environment
# The required python packages are listed in the requirements file.
python -m venv /path/to/venvs/bookstorewindow
source activate /path/to/venvs/bookstorewindow/bin/activate
pip install -r requirements/dev.txt
```

## Running the app on a local server

```bash
# run with django
./manage.py runserver

# or with heroku
heroku local
```

## Testing

Run all of the tests, including user tests, which use a selenium
web driver to simulate user behavior.

```
./manage.py test
./manage.py test user_tests  # run user tests only
./manage.py test window      # run unit tests only
```

To run the user tests against a staging server:

```bash
heroku local

# in a new terminal window
STAGING_SERVER=http://0.0.0.0:5000 ./manage.py test user_tests
```

## Deploying the app with Heroku

To deploy the app on a Heroku server, first install the `heroku` command line
client, and login.

```bash
brew install heroku/brew/heroku
heroku login
heroku create
heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set GOOGLE_API=XXXXXXXX

git push heroku heroku:master
heroku run python manage.py migrate
```

## Accessing the Postgres database

```bash
brew install postgres  # must have postgres installed locally
heroku pg:info
heroku pg:psql
```

## Using the Google Books API

Using the Google Books API requires requires an API key, which was created via
the Google Developer Console.
