import requests


_base_version = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
_base_download = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip'


def get_url(version='latest', _os=None, _os_bit=None):
	if version == 'latest':
		version = requests.get(_base_version).text
	download = _base_download % (version, _os, _os_bit)
	return 'chromedriver', download, version


if __name__ == "__main__":
	print([u for u in get_url('latest', 'win', '32')])
