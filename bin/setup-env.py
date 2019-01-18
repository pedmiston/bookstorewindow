#!/usr/bin/env python
"""Creates environment file from a template."""
import jinja2
from ansible_vault import Vault

template = jinja2.Template(
    """\
ANSIBLE_VAULT_PASSWORD_FILE={{ ansible_vault_password_file }}
GOOGLE_API_KEY={{ google_api_key }}
"""
)


def read_secrets(key, ansible_vault_password_file):
    secrets_file = "vars/secrets.yml"
    password = open(ansible_vault_password_file).read().strip()
    vault = Vault(password)
    data = vault.load(open(secrets_file).read())
    return data.get(key)


if __name__ == "__main__":
    ansible_vault_password_file = input(
        "Enter the path to the Ansible Vault password file: "
    )
    env_vars = dict(ansible_vault_password_file=ansible_vault_password_file)
    try:
        env_vars["google_api_key"] = read_secrets(
            "google_api_key", ansible_vault_password_file
        )
    except Exception as e:
        raise e

    with open(".env", "w") as dst:
        dst.write(template.render(**env_vars))
