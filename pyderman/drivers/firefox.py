from pyderman.util import github
import re


def get_url(version='latest', _os=None, _os_bit=None):
	urls = github.find_links('mozilla', 'geckodriver', version)
	for u in urls:
		target = '%s%s' % (_os, _os_bit) if _os is not 'mac' else 'macos'
		if target in u:
			ver = re.search(r'v(\d{1,2}\.\d{1,2}\.\d{1,2})', u).group(1)
			return 'geckodriver', u, ver


if __name__ == "__main__":
	print([u for u in get_url('0.24.0', 'mac', '64')])
