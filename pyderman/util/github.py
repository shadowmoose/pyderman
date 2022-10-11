from __future__ import annotations

import re

from pyderman.util import downloader


def make_asset_url(author: str, project: str, version: str) -> str:
    return f"https://github.com/{author}/{project}/releases/expanded_assets/{version}"


def make_releases_url(author: str, project: str, version: str) -> str:
    return f"https://github.com/{author}/{project}/releases/{version}"


def find_links(
    author: str, project: str, version: str = "latest", prefix: str = "v"
) -> list[str]:
    if not version:
        version = "latest"
    if version == "latest":
        redirect = downloader.get_redirect(make_releases_url(author, project, version))
        if not redirect:
            raise Exception(f"Unable to locate latest version of {project}")
        version = redirect.split("/")[-1]
    if not version.startswith(prefix):
        version = "{}{}".format(prefix, version)
    repo = make_asset_url(author, project, version)
    html = downloader.raw(repo)
    if html is None:
        raise Exception(f"Unable to download {project} version: {version}")
    return [
        "https://github.com%s" % str(u)
        for u in re.findall(r"\"(.+?/download.+?)\"", html)
    ]
