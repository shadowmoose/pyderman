import os
import platform
import subprocess
import unittest

from pyderman import chrome, edge, firefox, install, opera, phantomjs


def process_driver(driver, self):
    print("Testing %s..." % driver.__name__)
    try:
        data = install(
            browser=driver, verbose=True, chmod=True, overwrite=True, return_info=True
        )
    except OSError as err:
        print(err)
        return  # OSError is raised if the given OS cannot support the driver, which we need to ignore.
    path = data["path"]
    if not os.path.exists(path):
        raise FileNotFoundError(
            "The %s executable was not properly downloaded." % driver.__name__
        )
    output = subprocess.check_output([path, "--version"]).decode("utf-8")
    print("Version:", output)
    self.assertIn(
        data["version"],
        output.lower(),
        msg="Driver %s did not output proper version! ('%s')"
        % (driver.__name__, data["version"]),
    )
    print('%s is installed at: "%s"' % (data["driver"], path))
    print("\n\n\n")


class TestDriverInstalls(unittest.TestCase):
    def test_details(self):
        print("Machine:", platform.machine())
        print("Platform:", platform.platform())
        print("Arch:", platform.architecture())
        print("Processor:", platform.processor())
        print("Release:", platform.release())

    def test_chrome(self):
        process_driver(chrome, self)

    def test_firefox(self):
        process_driver(firefox, self)

    def test_opera(self):
        process_driver(opera, self)

    def test_phantomjs(self):
        process_driver(phantomjs, self)

    def test_edge(self):
        process_driver(edge, self)


if __name__ == "__main__":
    unittest.main()
