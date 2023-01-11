from __future__ import annotations

import re

from pyderman.util import downloader

_base_version = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
_base_download = "https://chromedriver.storage.googleapis.com/{version}/chromedriver_{os}{os_bit}.zip"


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    match = re.match(r"^(\d*)[.]?(\d*)[.]?(\d*)[.]?(\d*)$", version)
    if version == "latest":
        resolved_version = downloader.raw(_base_version)
    elif match:
        major, minor, patch, _build = match.groups()
        if patch:
            patch_version = f"{major}.{minor}.{patch}"
        else:
            patch_version = major
        resolved_version = downloader.raw(f"{_base_version}_{patch_version}")
    else:
        resolved_version = version
    if not resolved_version:
        raise ValueError(f"Unable to locate ChromeDriver version! [{version}]")
    if _os == "mac-m1":
        _os = "mac"
        version_tuple = tuple(map(int, resolved_version.split(".")))
        if version_tuple > (106, 0, 5249, 21):
            _os_bit = "_arm%s" % _os_bit  # chromedriver_mac_arm64
        else:
            _os_bit = "%s_m1" % _os_bit  # chromedriver_mac64_m1
    download = _base_download.format(version=resolved_version, os=_os, os_bit=_os_bit)
    return "chromedriver", download, resolved_version


if __name__ == "__main__":
    print([u for u in get_url("latest", "win", "32")])
