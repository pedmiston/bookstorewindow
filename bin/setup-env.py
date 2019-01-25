#!/usr/bin/env python
"""Creates environment file from a template."""
import os
import jinja2

template = jinja2.Template(
    """\
GOOGLE_API_KEY={{ google_api_key }}
DISABLE_COLLECTSTATIC=1
DEBUG=1
"""
)


if __name__ == "__main__":
    env_vars = {}
    env_vars["google_api_key"] = input("Enter the Google API Key: ")

    with open(".env", "w") as dst:
        dst.write(template.render(**env_vars))
