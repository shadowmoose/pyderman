from __future__ import annotations

import re

from pyderman.util import downloader

_base_version = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
_base_download = "https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip"


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    match = re.match(r"^(\d*)[.]?(\d*)[.]?(\d*)[.]?(\d*)$", version)
    if version == "latest":
        resolved_version = downloader.raw(_base_version)
    elif match:
        major, minor, patch, build = match.groups()
        if patch:
            patch_version = "{}.{}.{}".format(major, minor, patch)
        else:
            patch_version = major
        resolved_version = downloader.raw("{}_{}".format(_base_version, patch_version))
    else:
        resolved_version = version
    if not resolved_version:
        raise Exception("Unable to locate ChromeDriver version: {}!".format(version))
    if _os == "mac-m1":
        _os = "mac"  # chromedriver_mac64_m1
        _os_bit = "%s_m1" % _os_bit
    download = _base_download % (resolved_version, _os, _os_bit)
    return "chromedriver", download, resolved_version


if __name__ == "__main__":
    print([u for u in get_url("latest", "win", "32")])
