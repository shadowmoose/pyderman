from pyderman.util import github
import re


def get_url(version='latest', _os=None, _os_bit=None):
	urls = github.find_links('operasoftware', 'operachromiumdriver', version, prefix='v.')
	for u in urls:
		if '%s%s' % (_os, _os_bit) in u:
			ver = re.search(r'v\.(\d{1,2}\.\d{1,2})', u).group(1)
			return 'operadriver.*/operadriver', u, ver


if __name__ == "__main__":
	print([u for u in get_url('2.42', 'mac', '64')])
