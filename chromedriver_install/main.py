import os
from chromedriver_install import install


def run():
	path = install(verbose=True, chmod=True)
	if not os.path.exists(path):
		raise FileNotFoundError('The chromedriver executable was not properly downloaded.')
	print('Chromedriver is installed at: "%s"' % path)


if __name__ == "__main__":
	run()
