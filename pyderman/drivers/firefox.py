from __future__ import annotations

import re

from pyderman.util import github


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    urls = github.find_links("mozilla", "geckodriver", version)
    for u in urls:
        target = f"{_os}{_os_bit}." if _os != "mac" else "macos."
        if _os == "mac-m1":
            target = "macos-aarch64."
        if target in u:
            ver = re.search(r"v(\d+\.\d+\.\d+)", u)
            if ver is not None:
                return "geckodriver", u, str(ver.group(1))
    raise ValueError(f"Unable to locate FirefoxDriver version! [{version}]")


if __name__ == "__main__":
    print([u for u in get_url("0.24.0", "mac", "64")])
