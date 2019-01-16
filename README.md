# Bookstore Window

Search for books and view the results as in a store window.

## Development

Here are the steps I took to work on this project. These
steps were developed on a macOS with homebrew as a program
manager.

```bash
# Install required programs
brew install pyenv pipenv

# Activate pyenv to pin specific versions of python
eval "$(pyenv init -)"

# Install the required python packages in a 3.6 virtual environment
# The required python packages are stored in the Pipfile
pipenv install --python=3.6.6 --dev
```

## Running the app on a local server

```bash
# Use the django server to run locally
pipenv run bookstorewindow/manage.py runserver
```

## Running the app on a virtual machine

```bash
vagrant up
```

## Testing

Run all of the tests, including functional tests which use a selenium
web driver to simulate user behavior.

```
pipenv run ./manage.py test
```
