import os

from requests import Session


def search_volumes(query, session=None):
    """Search for volume data via the Google Books API.

    Args:
        query (str): The search query to send to the API.
        session (requests.Session): A session to use to make the URL
            request. If a session is not provided, a new one will be
            created.
    Returns:
        A list of dictionaries. The volume data returned by the Google Books
        API is described here: https://developers.google.com/books/docs/v1/reference/volumes#resource
    """
    api_key = os.getenv("GOOGLE_API_KEY", None)
    base_url = "https://www.googleapis.com/books/v1/volumes"

    query_url = f"{base_url}?q={query!r}&key={api_key}"
    if session is None:
        session = Session()
    response = session.get(query_url)
    if "items" not in response.json():
        logger.error(
            f"No items in the response json, status code: {response.status_code}"
        )
        return []
    else:
        return response.json()["items"]
