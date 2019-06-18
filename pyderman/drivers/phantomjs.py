from pyderman.util import downloader
import re
import json


def get_url(version='latest', _os=None, _os_bit=None):
	beta = True
	pattern = version
	bit = ''
	if not version or version == 'latest':
		beta = False
		pattern = ''
	if _os == 'linux':
		bit = '64' if _os_bit == '64' else 'i686'
	for release in _releases():
		name = release['name'].lower()
		if not beta and 'beta' in name:
			continue
		if _os in name and pattern in name and bit in name:
			ver = re.search(r'(\d{1,2}\.\d{1,2}\.\d{1,2})', name).group(1)
			return 'phantomjs.*/bin/phantomjs', release['links']['self']['href'], ver


def _releases():
	page = 'https://api.bitbucket.org/2.0/repositories/ariya/phantomjs/downloads/'
	while page:
		data = json.loads(downloader.raw(page))
		for release in data['values']:
			yield release
		page = data['next'] if 'next' in data else None


if __name__ == "__main__":
	print(get_url('latest', 'win', '64'))
