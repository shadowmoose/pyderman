from __future__ import annotations

import os
import platform
import re
import subprocess
import time
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
    latest = None

    @classmethod
    def setUpClass(self) -> None:
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

    def test_get_url_mac_arm(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="mac-m1", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_mac_arm64.zip",
        )
        return

    def test_get_url_mac_m1(self):
        version = "105.0.5195.52"
        drvr, url, vers = chrome.get_url(version, _os="mac-m1", _os_bit="64")
        self.assertEqual(vers, version)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64_m1.zip",
        )
        return

    def test_get_url_mac_86(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_mac64.zip",
        )
        return

    def test_get_url_win_32(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="win", _os_bit="32")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_win32.zip",
        )
        return

    def test_get_url_win_64(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="win", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_win64.zip",
        )
        return

    def test_get_url_linux_64(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="linux", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_linux64.zip",
        )
        return

    def test_get_url_linux_32(self):
        drvr, url, vers = chrome.get_url(self.latest, _os="linux", _os_bit="32")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{self.latest}/chromedriver_linux32.zip",
        )
        return

    def test_get_url_unrecognized_version(self):
        version = "abd.xyz"
        drvr, url, vers = chrome.get_url(version, _os="linux", _os_bit="32")
        self.assertEqual(vers, version)
        self.assertEqual(
            url,
            f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux32.zip",
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
            str(exc.exception), "Unable to locate ChromeDriver version! [25.25.25.25]"
        )
        return


class TestEdge(unittest.TestCase):
    version_re = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
    stable = None
    major = None

    @staticmethod
    def fetch(url: str) -> str:
        resp = urlopen(url, timeout=15)
        html = resp.read().decode("utf-16", errors="ignore").strip()
        return str(html)

    @staticmethod
    def looseVer(ver1):
        """Shorten the given version, dropping the trailing build ID to prevent artifact caching errors."""
        return ".".join(ver1.split(".")[:-1])

    @classmethod
    def setUpClass(self) -> None:
        url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
        if self.stable is None:
            self.stable = self.fetch(url)

        match = self.version_re.match(self.stable)
        if not match:
            raise ValueError(f"Invalid version string: {self.stable!r}")

        major, minor, patch, build = match.groups()
        self.major = major

        url_latest = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{self.major}"
        self.latest = self.fetch(url_latest)
        return

    def get_latest_os(self, major: str, _os: str) -> set[str]:
        url = f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{major}_{_os.upper()}"
        opts = set()
        for i in range(15):
            # This endpoint occasionally returns an older cached value,
            # so we have to fish for the cache to make testing more robust and cut down on false errors.
            latest_mac = self.fetch(url)
            opts.add(latest_mac)
            time.sleep(0.25)
        return opts

    def test_get_latest_mac(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="mac", _os_bit="64")
        latest_macs = self.get_latest_os(self.major, "MACOS")
        self.assertIn(vers, latest_macs)

    def test_get_stable_mac(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="mac", _os_bit="64")
        self.assertEqual(vers, self.stable)
        self.assertEqual(self.looseVer(vers), self.looseVer(self.stable))
        self.assertTrue("edgedriver_mac64" in url, "The returned mac URL is not valid!")

    def test_get_latest_linux(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="linux", _os_bit="64")
        latest_linux = self.get_latest_os(self.major, "LINUX")
        self.assertIn(vers, latest_linux)

    def test_get_stable_linux(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="linux", _os_bit="64")
        self.assertEqual(self.looseVer(vers), self.looseVer(self.stable))
        self.assertTrue(
            "edgedriver_linux64" in url, "The returned linux URL is not valid!"
        )

    def test_get_latest_windows(self) -> None:
        drvr, url, vers = edge.get_url("latest", _os="win", _os_bit="64")
        latest_wins = self.get_latest_os(self.major, "WINDOWS")
        self.assertIn(vers, latest_wins)

    def test_get_stable_windows(self) -> None:
        drvr, url, vers = edge.get_url("stable", _os="win", _os_bit="64")
        self.assertEqual(self.looseVer(vers), self.looseVer(self.stable))
        self.assertTrue(
            "edgedriver_win64" in url, "The returned windows URL is not valid!"
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
            edge.get_url(None, _os="mac", _os_bit="64")  # type: ignore[arg-type]
        self.assertEqual(
            str(exc.exception), "Unable to locate EdgeDriver version! [None]"
        )
        return

    def test_get_url_mac_arm(self):
        drvr, url, vers = edge.get_url(self.latest, _os="mac-m1", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.stable}/edgedriver_mac64_m1.zip",
        )

    def test_get_url_mac_m1(self):
        drvr, url, vers = edge.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_mac64.zip",
        )

    def test_get_url_mac_32(self):
        drvr, url, vers = edge.get_url(self.latest, _os="mac", _os_bit="32")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_mac32.zip",
        )

    def test_get_url_mac_86(self):
        drvr, url, vers = edge.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_mac64.zip",
        )

    def test_get_url_win_32(self):
        drvr, url, vers = edge.get_url(self.latest, _os="win", _os_bit="32")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_win32.zip",
        )

    def test_get_url_win_64(self):
        drvr, url, vers = edge.get_url(self.latest, _os="win", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_win64.zip",
        )

    def test_get_url_linux_64(self):
        drvr, url, vers = edge.get_url(self.latest, _os="linux", _os_bit="64")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_linux64.zip",
        )

    def test_get_url_linux_32(self):
        drvr, url, vers = edge.get_url(self.latest, _os="linux", _os_bit="32")
        self.assertEqual(vers, self.latest)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{self.latest}/edgedriver_linux32.zip",
        )

    def test_get_url_unrecognized_version(self):
        version = "abd.xyz"
        drvr, url, vers = edge.get_url(version, _os="linux", _os_bit="32")
        self.assertEqual(vers, version)
        self.assertEqual(
            url,
            f"https://msedgedriver.azureedge.net/{version}/edgedriver_linux32.zip",
        )


class TestFirefox(unittest.TestCase):
    version_re = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
    stable = None

    @staticmethod
    def fetch(url: str) -> str:
        resp = urlopen(url, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore").strip()
        return str(html)

    @classmethod
    def setUpClass(self) -> None:
        page = urlopen(
            "https://github.com/mozilla/geckodriver/releases/latest", timeout=15
        )
        redirect = page.geturl()
        version_string = redirect.split("/")[-1]
        self.latest = version_string
        return

    def test_get_url_mac_arm(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="mac-m1", _os_bit="64")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-macos-aarch64.tar.gz",
        )
        return

    def test_get_url_mac_m1(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-macos.tar.gz",
        )
        return

    def test_get_url_mac_32(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="mac", _os_bit="32")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-macos.tar.gz",
        )
        return

    def test_get_url_mac_86(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="mac", _os_bit="64")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-macos.tar.gz",
        )
        return

    def test_get_url_win_32(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="win", _os_bit="32")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-win32.zip",
        )
        return

    def test_get_url_win_64(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="win", _os_bit="64")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-win64.zip",
        )
        return

    def test_get_url_linux_64(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="linux", _os_bit="64")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-linux64.tar.gz",
        )
        return

    def test_get_url_linux_32(self):
        drvr, url, vers = firefox.get_url(self.latest, _os="linux", _os_bit="32")
        self.assertEqual(vers, self.latest[1:])
        self.assertEqual(
            url,
            f"https://github.com/mozilla/geckodriver/releases/download/"
            f"{self.latest}/geckodriver-{self.latest}-linux32.tar.gz",
        )
        return

    def test_get_url_unrecognized_version(self):
        version = "abd.xyz"
        with self.assertRaises(Exception) as exc:
            drvr, url, vers = firefox.get_url(version, _os="linux", _os_bit="32")
        self.assertEqual(
            str(exc.exception), f"Unable to download geckodriver version: v{version}"
        )


if __name__ == "__main__":
    unittest.main()
