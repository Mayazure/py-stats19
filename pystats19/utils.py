from urllib.parse import urljoin

from pystats19 import DEFAULT_SOURCE_DOMAIN, DEFAULT_SOURCE_DIRECTORY


def get_url(
        file_name="",
        domain=DEFAULT_SOURCE_DOMAIN,
        directory=DEFAULT_SOURCE_DIRECTORY
):
    url = "/".join((directory, file_name)) if file_name else directory
    base = urljoin(domain, url)
    return base
