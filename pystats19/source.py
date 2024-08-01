import os
import os.path
import shutil
import tempfile
import urllib.request

from pystats19 import options
from pystats19.utils import get_url


def pull_file(
        filename: str,
        data_dir: str | os.PathLike = options.data_directory
):
    """Download a specific data file from source website.

    :param str filename: The name of the file to download. Must be a valid filename which is defined in
    pystats19.stats19_data_files, pystats19.stats19_adjustment_files, pystats19.stats19_metadata_files
    :param str | PathLike data_dir: The directory to store the downloaded files.
    """
    url = get_url(filename)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with urllib.request.urlopen(url) as f:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(f.read())
            temp_file_name = temp_file.name
            dest = os.path.join(data_dir, filename)
        shutil.move(temp_file_name, dest)
