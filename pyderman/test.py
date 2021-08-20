import os
from pyderman import install, chrome, firefox, opera, phantomjs, edge
import subprocess
import unittest
import platform


def test_driver(driver):
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


class TestDriverInstalls(unittest.TestCase):

	def test_details(self):
		print('Machine:', platform.machine())
		print('Platform:', platform.platform())
		print('Arch:', platform.architecture())
		print('Processor:', platform.processor())
		print('Release:', platform.release())
		
	def test_chrome(self):
		test_driver(chrome)
		
	def test_firefox(self):
		test_driver(firefox)

	def test_opera(self):
		test_driver(opera)

	def test_phantomjs(self):
		test_driver(phantomjs)

	def test_edge(self):
		test_driver(edge)

if __name__ == "__main__":
	unittest.main()

