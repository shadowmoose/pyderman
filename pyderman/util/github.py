from __future__ import annotations

import re

from pyderman.util import downloader


def find_links(
    author: str, project: str, version: str = "latest", prefix: str = "v"
) -> list[str]:
    if not version:
        version = "latest"
    if version != "latest" and not version.startswith(prefix):
        version = "%s%s" % (prefix, version)
    repo = "https://github.com/%s/%s/releases/%s" % (author, project, version)
    html = downloader.raw(repo)
    if html is None:
        raise Exception("Unable to download %s version: %s" % (project, version))
    return [
        "https://github.com%s" % str(u)
        for u in re.findall(r"\"(.+?/download.+?)\"", html)
    ]
