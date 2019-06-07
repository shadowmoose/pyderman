import os
from pyderman import install, chrome, firefox
import subprocess


def run():
	for driver in [chrome, firefox]:
		print("Testing %s..." % driver.__name__)
		data = install(browser=driver, verbose=True, chmod=True, overwrite=True, return_info=True)
		path = data['path']
		if not os.path.exists(path):
			raise FileNotFoundError('The %s executable was not properly downloaded.' % driver.__name__)
		output = subprocess.check_output([path, '--version']).decode('utf-8')
		print('Version:', output)
		assert data['version'] in output.lower()
		print('%s is installed at: "%s"' % (data['driver'], path))
		print('\n\n\n')


if __name__ == "__main__":
	run()
