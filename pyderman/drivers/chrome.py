import re

from pyderman.util import downloader

_base_version = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
_base_download = "https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip"


def get_url(version="latest", _os=None, _os_bit=None):
    if version == "latest":
        resolved_version = downloader.raw(_base_version)
    elif re.match(r"\d+(\.\d+\.\d+)?", version):
        resolved_version = downloader.raw("{}_{}".format(_base_version, version))
    else:
        resolved_version = version
    if not resolved_version:
        raise Exception("Unable to locate ChromeDriver version: {}!".format(version))
    if _os == "mac-sur":
        _os = "mac"  # chromedriver_mac64_m1
        _os_bit = _os_bit + "_m1"
    download = _base_download % (resolved_version, _os, _os_bit)
    return "chromedriver", download, resolved_version


if __name__ == "__main__":
    print([u for u in get_url("latest", "win", "32")])
