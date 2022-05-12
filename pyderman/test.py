from __future__ import annotations

import os
import platform
import re
import subprocess
import unittest
from types import ModuleType

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    # noinspection PyUnresolvedReferences
    from urllib2 import urlopen  # type: ignore[import,no-redef]

from pyderman import chrome, edge, firefox, install, opera, phantomjs


def process_driver(driver: ModuleType, self: TestDriverInstalls) -> None:
    print("Testing %s..." % driver.__name__)
    try:
        data = install(
            browser=driver, verbose=True, chmod=True, overwrite=True, return_info=True
        )
    except OSError as err:
        print(err)
        return  # OSError is raised if the given OS cannot support the driver, which we need to ignore.
    if type(data) is not dict or not os.path.exists(str(data.get("path"))):
        raise FileNotFoundError(
            "The %s executable was not properly downloaded." % driver.__name__
        )
    path = str(data.get("path"))
    output = subprocess.check_output([path, "--version"]).decode("utf-8")
    print("Version:", output)
    self.assertIn(
        data["version"],
        output.lower(),
        msg="Driver %s did not output proper version! ('%s')"
        % (driver.__name__, data["version"]),
    )
    print('{} is installed at: "{}"'.format(data["driver"], path))
    print("\n\n\n")


class TestDriverInstalls(unittest.TestCase):
    def test_details(self) -> None:
        print("Machine:", platform.machine())
        print("Platform:", platform.platform())
        print("Arch:", platform.architecture())
        print("Processor:", platform.processor())
        print("Release:", platform.release())

    def test_chrome(self) -> None:
        process_driver(chrome, self)

    def test_firefox(self) -> None:
        process_driver(firefox, self)

    def test_opera(self) -> None:
        process_driver(opera, self)

    def test_phantomjs(self) -> None:
        process_driver(phantomjs, self)

    def test_edge(self) -> None:
        process_driver(edge, self)


class TestChrome(unittest.TestCase):
    def setUp(self) -> None:
        version_re = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
        url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        resp = urlopen(url, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        version_string = str(html)
        self.latest = version_string

        match = version_re.match(version_string)
        if not match:
            raise ValueError("Invalid version string: %r" % version_string)

        major, minor, patch, build = match.groups()
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build
        return

    def chrome_version(self, version: str) -> None:
        drvr, url, vers = chrome.get_url(version, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_mac64.zip",
        )

    def test_get_latest(self) -> None:
        self.chrome_version("latest")

    def test_get_major(self) -> None:
        self.chrome_version(f"{self.major}")

    def test_get_patch(self) -> None:
        self.chrome_version(f"{self.major}.{self.minor}.{self.patch}")

    def test_get_build(self) -> None:
        self.chrome_version(f"{self.latest}")

    def test_get_nonsense(self) -> None:
        with self.assertRaises(Exception) as exc:
            self.chrome_version("25.25.25.25")
        self.assertEqual(
            str(exc.exception), "Unable to locate ChromeDriver version: 25.25.25.25!"
        )
        return


class TestEdge(unittest.TestCase):
    version_re = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
    stable = None

    @staticmethod
    def fetch(url: str) -> str:
        resp = urlopen(url, timeout=15)
        html = resp.read().decode("utf-16", errors="ignore").strip()
        return str(html)

    def setUp(self) -> None:
        url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
        if self.stable is None:
            self.stable = self.fetch(url)

            match = self.version_re.match(self.stable)
            if not match:
                raise ValueError(f"Invalid version string: {self.stable!r}")

            major, minor, patch, build = match.groups()
            self.major = major
        return

    def get_latest_os(self, major: str, _os: str) -> str:
        url = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{major}_{_os.upper()}"
        return self.fetch(url)

    def test_get_latest_mac(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="mac", _os_bit="64")
        latest_mac = self.get_latest_os(self.major, "MACOS")
        self.assertEqual(vers, latest_mac)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{latest_mac}/edgedriver_mac64.zip",
        )

    def test_get_stable_mac(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="mac", _os_bit="64")
        self.assertEqual(vers, self.stable)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.stable}/edgedriver_mac64.zip",
        )

    def test_get_latest_linux(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="linux", _os_bit="64")
        latest_linux = self.get_latest_os(self.major, "LINUX")
        self.assertEqual(vers, latest_linux)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{latest_linux}/edgedriver_linux64.zip",
        )

    def test_get_stable_linux(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="linux", _os_bit="64")
        self.assertEqual(vers, self.stable)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.stable}/edgedriver_linux64.zip",
        )

    def test_get_latest_windows(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="win", _os_bit="64")
        latest_win = self.get_latest_os(self.major, "WINDOWS")
        self.assertEqual(vers, latest_win)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{latest_win}/edgedriver_win64.zip",
        )

    def test_get_stable_windows(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="win", _os_bit="64")
        self.assertEqual(vers, self.stable)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.stable}/edgedriver_win64.zip",
        )

    def test_get_major(self) -> None:
        """only proves url is created, not that it's valid"""
        drvr, url, vers = edge.get_url(self.major, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.major)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.major}/edgedriver_mac64.zip",
        )

    def test_get_build(self) -> None:
        url_latest = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{self.major}"
        self.latest = self.fetch(url_latest)

        match_latest = self.version_re.match(self.latest)
        if not match_latest:
            raise ValueError(f"Invalid version string: {self.latest!r}")

        major_latest, minor_latest, patch_latest, build_latest = match_latest.groups()
        self.major_latest = major_latest

        drvr, url, vers = edge.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_mac64.zip",
        )

    def test_get_invalid_os(self) -> None:
        with self.assertRaises(OSError) as exc:
            edge.get_url("1.2.3.4", "lcars", "4096")
        self.assertEqual(
            str(exc.exception), "There is no valid EdgeDriver release for lcars"
        )

    def test_unresolved_version(self) -> None:
        with self.assertRaises(Exception) as exc:
            edge.get_url(None, _os="mac", _os_bit="64")  # type: ignore
        self.assertEqual(
            str(exc.exception), "Unable to locate EdgeDriver version: None!"
        )
        return


if __name__ == "__main__":
    unittest.main()
