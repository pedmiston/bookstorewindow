import os

from requests import Session


def search(query, session=None):
    api_key = os.getenv("GOOGLE_API_KEY", None)
    base_url = "https://www.googleapis.com/books/v1/volumes"
    query_url = f"{base_url}?q={query!r}&key={api_key}"
    if session is None:
        session = Session()
    response = session.get(query_url)
    return response.json()["items"]
