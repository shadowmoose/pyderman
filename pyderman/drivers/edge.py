from __future__ import annotations

from pyderman.util import downloader


def get_url(
    version: str = "latest", _os: str | None = None, _os_bit: str | None = None
) -> tuple[str, str, str]:
    if version == "latest":
        try:
            version = latest()
        except Exception as e:
            print(e)
    if _os == "win":
        url = "https://msedgedriver.azureedge.net/{}/edgedriver_win{}.zip".format(
            version,
            _os_bit,
        )
    elif _os == "mac":
        url = "https://msedgedriver.azureedge.net/%s/edgedriver_mac64.zip" % version
    elif _os == "linux":
        url = "https://msedgedriver.azureedge.net/%s/edgedriver_linux64.zip" % version
    else:
        raise OSError("There is no valid EdgeDriver release for %s" % _os)
    if not version:
        raise ValueError("Unable to automatically locate latest version of EdgeDriver!")
    return "msedgedriver", url, version


def latest() -> str:
    url = "https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_STABLE"
    data = downloader.raw(url, "utf-16")
    if data is None:
        raise Exception("Unable to get: %s" % url)
    return data.strip()


if __name__ == "__main__":
    print(get_url("latest", "win", "64"))
    print(get_url("latest", "linux", "64"))
