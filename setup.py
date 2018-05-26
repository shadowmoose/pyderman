from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name='chromedriver_install',
	version='0.1',
	description='Installs chromedriver automatically.',
	long_description=readme(),
	url='http://github.com/shadowmoose/chrome_driver',
	author='ShadowMoose',
	author_email='shadowmoose@github.com',
	license='MIT',
	packages=['chromedriver_install'],
	install_requires=[
		'requests',
	],
	entry_points={
		'console_scripts': ['chromedriver-install=chromedriver_install:install'],
	},
	zip_safe=False)
