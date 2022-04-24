from __future__ import annotations

import re

from pyderman.util import github


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    urls = github.find_links(
        "operasoftware", "operachromiumdriver", version, prefix="v."
    )
    for u in urls:
        if "{}{}".format(_os, _os_bit) in u:
            ver = re.search(r"v\.(\d{1,2}\.\d{1,2})", u)
            if ver is not None:
                return "operadriver.*/operadriver", u, str(ver.group(1))
    raise ValueError("Unable to get url")


if __name__ == "__main__":
    print([u for u in get_url("2.42", "mac", "64")])
