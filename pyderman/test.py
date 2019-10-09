import os
from pyderman import install, all_drivers
import subprocess
import unittest


class TestDriverInstalls(unittest.TestCase):

	def test_all_installs(self):
		for driver in all_drivers:
			print("Testing %s..." % driver.__name__)
			try:
				data = install(browser=driver, verbose=True, chmod=True, overwrite=True, return_info=True)
			except OSError as err:
				print(err)
				continue  # OSError is raised if the given OS cannot support the driver, which we need to ignore.
			path = data['path']
			if not os.path.exists(path):
				raise FileNotFoundError('The %s executable was not properly downloaded.' % driver.__name__)
			output = subprocess.check_output([path, '--version']).decode('utf-8')
			print('Version:', output)
			self.assertIn(
				data['version'],
				output.lower(),
				msg="Driver %s did not output proper version! ('%s')" % (driver.__name__, data['version'])
			)
			print('%s is installed at: "%s"' % (data['driver'], path))
			print('\n\n\n')


if __name__ == "__main__":
	unittest.main()

