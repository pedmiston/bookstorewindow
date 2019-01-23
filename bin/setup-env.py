#!/usr/bin/env python
"""Creates environment file from a template."""
import os
import jinja2
from ansible_vault import Vault

template = jinja2.Template(
    """\
#!/usr/bin/env bash
export ANSIBLE_VAULT_PASSWORD_FILE={{ ansible_vault_password_file }}
export GOOGLE_API_KEY={{ google_api_key }}
export DIGITALOCEAN_ACCESS_TOKEN={{ digitalocean_access_token }}

{{ virtualenv_command }}
"""
)


def read_secrets(key, ansible_vault_password_file):
    secrets_file = "vars/secrets.yml"
    password = open(ansible_vault_password_file).read().strip()
    vault = Vault(password)
    data = vault.load(open(secrets_file).read())
    return data.get(key)


if __name__ == "__main__":
    if "ANSIBLE_VAULT_PASSWORD_FILE" in os.environ:
        ansible_vault_password_file = os.environ["ANSIBLE_VAULT_PASSWORD_FILE"]
    else:
        ansible_vault_password_file = input(
            "Enter the path to the Ansible Vault password file: "
        )
    env_vars = dict(ansible_vault_password_file=ansible_vault_password_file)
    try:
        env_vars["google_api_key"] = read_secrets(
            "google_api_key", ansible_vault_password_file
        )
        env_vars["digitalocean_access_token"] = read_secrets(
            "digitalocean_access_token", ansible_vault_password_file
        )
    except Exception as e:
        raise e

    env_vars["virtualenv_command"] = input(
        "Enter the command to activate the virtualenv: "
    )

    with open(".env", "w") as dst:
        dst.write(template.render(**env_vars))
