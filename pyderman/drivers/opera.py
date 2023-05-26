from __future__ import annotations

import re

from pyderman.util import github
from pyderman.util.const import MAC_ARM


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    urls = github.find_links(
        "operasoftware", "operachromiumdriver", version, prefix="v."
    )
    if _os == MAC_ARM:
        _os = "mac"
    # opera converted to a new version scheme in 2017
    # was v.2.45, now (chromium pattern) v.76.0.3809.132
    for u in urls:
        if f"{_os}{_os_bit}" in u:
            pat = r"v\.(\d*[.]?\d*[.]?\d*[.]?\d*)"
            ver = re.search(pat, u)
            if ver is not None:
                return "operadriver.*/operadriver", u, str(ver.group(1))
    raise ValueError(f"Unable to locate OperaDriver version! [{version}]")


if __name__ == "__main__":
    print([u for u in get_url("2.42", "mac", "64")])
