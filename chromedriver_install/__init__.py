import requests
import platform
import shutil
import os
import zipfile


_base_version = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
_base_download = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip'

_versions = ['32', '64']
_os_opts = [('win', 'win', 'chromedriver.exe'), ('darwin', 'mac', 'chromedriver'), ('linux', 'linux', 'chromedriver')]

_os_version = None
_os_filename = None
for _v in _versions:
	if platform.machine().endswith(_v):
		_os_version = _v
		break

_current_os = None
for _o in _os_opts:
	if _o[0] in platform.system().lower():
		_current_os = _o[1]
		_os_filename = _o[2]


def install(file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version=None, filename=None):
	if not _current_os or not _os_version:
		raise Exception('Cannot determine OS/bitness version! [%s,%s]' % (_current_os, _os_version))
	if not version:
		latest = requests.get(_base_version).text
	else:
		latest = version
	if not filename:
		filename = _os_filename
	download = _base_download % (latest, _current_os, _os_version)
	path = os.path.join(os.path.abspath(file_directory), 'chromedriver_%s.zip' % latest)
	out_filename = os.path.join(os.path.abspath(file_directory), filename)
	if not overwrite and os.path.exists(out_filename):
		if verbose:
			print('chromedriver is already installed.')
		return out_filename

	if not _download(download, path, verbose):
		if verbose:
			print('Download for %s version failed; Trying alternates.' % _os_version)
		for _v in _versions:
			download = _base_download % (latest, _current_os, _v)
			if _v != _os_version and _download(download, path, verbose):
				break
	out = out_filename if _extract(path) else None
	if out and chmod:
		mode = os.stat(out).st_mode
		mode |= (mode & 0o444) >> 2    # copy R bits to X
		os.chmod(out, mode)
	return out


def _download(url, path, verbose=True):
	if verbose:
		print('\tDownloading from: ', url)
		print('\tTo: ', path)
	r = requests.get(url, stream=True)
	if r.status_code != 200:
		return False
	else:
		if not os.path.isdir(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
			return True


def _extract(path):
	if not os.path.exists(path):
		return False
	with zipfile.ZipFile(path, "r") as zip_ref:
		zip_ref.extractall(os.path.dirname(path))
	os.remove(path)
	return True
