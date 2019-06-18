import shutil
from os.path import isdir, dirname, abspath
from os import makedirs
try:
	from urllib.request import urlopen  # Python 3
except ImportError:
	# noinspection PyUnresolvedReferences
	from urllib2 import urlopen  # Python 2


def _open(url):
	# noinspection PyBroadException
	try:
		return urlopen(url, timeout=15)
	except Exception:
		return None


def raw(url):
	resp = _open(url)
	if not resp:
		return False
	c_type = resp.headers.get_content_charset()
	c_type = c_type if c_type else 'utf-8'
	html = resp.read().decode(c_type, errors='ignore')
	return html


def binary(url, file, length=16*1024):
	file = abspath(file)
	if not isdir(dirname(file)):
		makedirs(dirname(file), exist_ok=True)
	req = _open(url)
	if not req:
		return False
	with open(file, 'wb') as fp:
		shutil.copyfileobj(req, fp, length)
	return True


if __name__ == '__main__':
	print(raw('https://google.com'))
