from pyderman.util import downloader

_base_version = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
_base_download = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip'


def get_url(version='latest', _os=None, _os_bit=None):
	if version == 'latest':
		version = downloader.raw(_base_version)
	if not version:
		raise Exception("Unable to locate latest ChromeDriver version!")
	download = _base_download % (version, _os, _os_bit)
	return 'chromedriver', download, version


if __name__ == "__main__":
	print([u for u in get_url('latest', 'win', '32')])
