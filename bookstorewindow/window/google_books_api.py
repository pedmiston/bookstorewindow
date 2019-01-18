import os

from requests import Session


def search(query, session=None):
    """Search for book data via the Google Books API.

    Book data returned by the Google Books API is described here:
    https://developers.google.com/books/docs/v1/reference/volumes#resource

    Args:
        query (str): The search query to send to the API.
        session (requests.Session): A session to use to make the URL
            request. If a session is not provided, a new one will be
            created.
    Returns:
        A list of dicts.

    """
    api_key = os.getenv("GOOGLE_API_KEY", None)
    base_url = "https://www.googleapis.com/books/v1/volumes"
    query_url = f"{base_url}?q={query!r}&key={api_key}"
    if session is None:
        session = Session()
    response = session.get(query_url)
    return response.json()["items"]
