import os
from chromedriver_install import install

if __name__ == "__main__":
	path = install(verbose=True, chmod=True)
	if not os.path.exists(path):
		raise FileNotFoundError('The chromedriver executable was not properly downloaded.')
	print('Chromedriver is installed at: "%s"' % path)
