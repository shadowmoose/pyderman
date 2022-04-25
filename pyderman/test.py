from __future__ import annotations

import os
import platform
import subprocess
import unittest
from types import ModuleType

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


if __name__ == "__main__":
    unittest.main()
