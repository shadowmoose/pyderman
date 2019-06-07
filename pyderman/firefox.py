from pyderman import downloader
import re


def get_url(version='latest', _os=None, _os_bit=None):
	if version != 'latest' and not version.startswith('v'):
		version = 'v%s' % version
	repo = 'https://github.com/mozilla/geckodriver/releases/%s' % version
	html = downloader.raw(repo)
	if not html:
		raise Exception("Unable to download version: %s" % version)
	urls = ['https://github.com%s' % u for u in re.findall(r'\"(.+?/download.+?)\"', html)]
	for u in urls:
		if '%s%s' % (_os, _os_bit) in u:
			ver = re.search(r'v(\d{1,2}\.\d{1,2}\.\d{1,2})', u).group(1)
			return 'geckodriver', u, ver


if __name__ == "__main__":
	print([u for u in get_url('0.24.0', 'win', '64')])
