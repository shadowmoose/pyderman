from pyderman.util import downloader
import re


def get_url(version='latest', _os=None, _os_bit=None):
	if version == 'latest':
		try:
			version = latest()
		except Exception as e:
			print(e)
	if _os == 'win':
		url = 'https://msedgedriver.azureedge.net/%s/edgedriver_win%s.zip' % (version, _os_bit)
	elif _os == 'mac':
		url = 'https://msedgedriver.azureedge.net/%s/edgedriver_mac64.zip' % version
	else:
		raise OSError('There is no valid EdgeDriver release for %s' % _os)
	if not version:
		raise ValueError('Unable to automatically locate latest version of EdgeDriver!')
	return 'msedgedriver', url, version


def latest():
	url = 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
	data = downloader.raw(url)
	regex = r"https://msedgedriver\.azureedge\.net/(.+?)/edgedriver"
	matches = list(set([m.group(1) for m in re.finditer(regex, data, re.MULTILINE)]))
	matches.sort(key=lambda s: [int(u) for u in s.split('.')], reverse=True)
	return matches[0]


if __name__ == "__main__":
	print(get_url('latest', 'win', '64'))
