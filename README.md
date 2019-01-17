# Bookstore Window

Search for books and view the results as in a store window.

## Development

Here are the steps to take to work on this project. These
steps were developed on a macOS with homebrew as a program
manager.

```bash
# Install required programs
brew install pyenv pipenv

# Activate pyenv to pin specific versions of python
eval "$(pyenv init -)"

# Install the required python packages in a virtual environment
# The required python packages are listed in the Pipfile
pipenv install --dev

# Creates an environment file from a template named ".env"
# pipenv will load the ".env" file when the venv is activated.
pipenv run bin/setup-env.py
```

## Environment vars

There is only one environment variable that needs to be provided in order
to develop the application.

`ANSIBLE_VAULT_PASSWORD_FILE`: The full path to the password file used to access data encrypted with ansible-vault.

## Running the app on a local server

```bash
cd bookstorewindow
pipenv run ./manage.py runserver
```

## Testing

Run all of the tests, including functional tests, which use a selenium
web driver to simulate user behavior.

```
pipenv run ./manage.py test
pipenv run ./manage.py test window  # run unit tests only
```

## Using the Google Books API

### Obtain an API key

Obtaining public data from the Google Books API requires an API key,
which was created via the Google Developer Console. The key for this
project is stored in a yaml file that was encrypted using the
ansible-vault tool.
