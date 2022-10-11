from __future__ import annotations

import shutil
from os import makedirs
from os.path import abspath, dirname, isdir
from typing import Any
from urllib.request import urlopen


def _open(url: str) -> Any:
    # noinspection PyBroadException
    try:
        return urlopen(url, timeout=15)
    except Exception:
        return None


def get_redirect(url: str) -> str | None:
    req = _open(url)
    if not req:
        return None
    return str(req.geturl())


def raw(url: str, encoding: str = "utf-8") -> str | None:
    resp = _open(url)
    if not resp:
        return None
    c_type = resp.headers.get_content_charset()
    c_type = c_type if c_type else encoding
    html = resp.read().decode(c_type, errors="ignore")
    return str(html)


def binary(url: str, file: str, length: int = 16 * 1024) -> bool:
    file = abspath(file)
    if not isdir(dirname(file)):
        makedirs(dirname(file), exist_ok=True)
    req = _open(url)
    if not req:
        return False
    with open(file, "wb") as fp:
        shutil.copyfileobj(req, fp, length)
    return True


if __name__ == "__main__":
    print(raw("https://google.com"))
