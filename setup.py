from setuptools import setup


def readme(file='', split=False):
	with open(file) as f:
		if split:
			return f.readlines()
		else:
			return f.read()


setup(
	name='chromedriver_install',
	version='0.3',
	description='Package for installing the latest chromedriver automatically.',
	long_description=readme('README.md'),
	long_description_content_type='text/markdown',
	url='http://github.com/shadowmoose/chrome_driver',
	author='ShadowMoose',
	author_email='shadowmoose@github.com',
	license='MIT',
	packages=['chromedriver_install'],
	install_requires=readme('requirements.txt', split=True),
	zip_safe=False)

# python setup.py sdist;twine upload dist/*
