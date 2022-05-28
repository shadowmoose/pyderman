from __future__ import annotations

import json
import re
from typing import Any, Generator

from pyderman.util import downloader


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    beta = True
    pattern = version
    bit = ""
    if not version or version == "latest":
        beta = False
        pattern = ""
    if _os == "linux":
        bit = "64" if _os_bit == "64" else "i686"
    for release in _releases():
        name = str(release["name"]).lower()
        if not beta and "beta" in name:
            continue
        if _os is not None and _os in name and pattern in name and bit in name:
            ver = re.search(r"(\d{1,2}\.\d{1,2}\.\d{1,2})", name)
            if ver is not None:
                return (
                    "phantomjs.*/bin/phantomjs",
                    release["links"]["self"]["href"],
                    str(ver.group(1)),
                )
    raise ValueError(f"Unable to locate PhantomJSDriver version! [{version}]")


def _releases() -> Generator[dict[str, Any], None, None]:
    page = "https://api.bitbucket.org/2.0/repositories/ariya/phantomjs/downloads/"
    while page:
        s = downloader.raw(page)
        if s is None:
            raise ValueError(f"Unable to get page: {page}")
        else:
            data = json.loads(s)
            for release in data["values"]:
                yield release
            page = data["next"] if "next" in data else None


if __name__ == "__main__":
    print(get_url("latest", "win", "64"))
