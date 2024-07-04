import os
import shutil
import tempfile
import urllib.request

from pystats19 import option
from pystats19.utils import get_url


def dl_stats19(
        file_name: str,
        data_dir=option.data_directory,

):
    url = get_url(file_name)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with urllib.request.urlopen(url) as f:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(f.read())
            temp_file_name = temp_file.name
            print(temp_file_name)
            dest = os.path.join(data_dir, file_name)
            print(dest)
        shutil.move(temp_file_name, dest)
