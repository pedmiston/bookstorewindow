#!/usr/bin/env python
"""Creates environment file from a template."""
import jinja2

template = jinja2.Template("""\
ANSIBLE_VAULT_PASSWORD_FILE={{ ansible_vault_password_file }}
""")


if __name__ == "__main__":
    env_vars = dict(
        ansible_vault_password_file=input("Enter the path to the Ansible Vault password file: "),
    )
    with open(".env", "w") as dst:
        dst.write(template.render(**env_vars))

