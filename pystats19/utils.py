from urllib.parse import urljoin

import pystats19


def get_url(
        file_name="",
        domain=pystats19.stats19_source_domain,
        directory=pystats19.stats19_source_directory
):
    url = "/".join((directory, file_name)) if file_name else directory
    base = urljoin(domain, url)
    return base


dtype_map = {
    int: "Int64",
    float: "Float64"
}


def replace_pd_dtype(dtype: dict):
    return {k: dtype_map.get(v, v) for k, v in dtype.items()}
