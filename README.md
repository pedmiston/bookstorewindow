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
python -m venv /path/to/venvs/bookstore-window
source activate /path/to/venvs/bookstore-window/bin/activate
pip install -r requirements.txt
pip install -r bookstorewindow/requirements/dev.txt

# Creates an environment file from a template named ".env"
python bin/setup-env.py

# Export the required environment variables and activate the venv
source .env
```

## Environment vars

There is only one environment variable that needs to be provided in order
to develop the application.

`ANSIBLE_VAULT_PASSWORD_FILE`: The full path to the password file used to access data encrypted with ansible-vault.

All the other environment variables are extracted from a file encrypted
using `ansible-vault`.

## Running the app on a local server

```bash
# Use the django server to run locally
pipenv run bookstorewindow/manage.py runserver
```

## Running the app on a virtual machine

```bash
vagrant up
vagrant ssh
cd /apps/bookstorewindow
source venv/bin/activate
./manage.py runserver 0.0.0.0:8000
```

## Running the app on a Digital Ocean Droplet

To browse available Droplet details, use the `doctl` command line tool.

```bash
brew install doctl
echo $DIGITALOCEAN_ACCESS_TOKEN
doctl compute image list-distribution --public  # list public distributions
doctl compute size list                         # list droplet sizes
doctl compute ssh-key list                      # list available ssh keys
```

To create a Droplet for the app, run the following Ansible playbook:

```bash
ansible-playbook provision.yml
```

To view the Droplet that was created, use the `doctl` tool:

```
doctl compute droplet list                      # list running droplets
doctl compute ssh [DROPLET_NAME]                # ssh to running droplet
```

## Testing

Run all of the tests, including functional tests, which use a selenium
web driver to simulate user behavior.

```
pipenv run ./manage.py test
pipenv run ./manage.py test user_tests  # run user tests only
pipenv run ./manage.py test window      # run unit tests only
```

## Using the Google Books API

Using the Google Books API requires requires an API key, which was created via
the Google Developer Console. The key for this project is stored in a yaml file
that was encrypted using the `ansible-vault` tool.
