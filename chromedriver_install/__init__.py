import requests
import platform
import shutil
import os
import zipfile


_base_version = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
_base_download = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip'

versions = ['32', '64']
os_opts = [('win', 'win', 'chromedriver.exe'), ('darwin', 'mac', 'chromedriver'), ('linux', 'linux', 'chromedriver')]

os_version = None
os_filename = None
for v in versions:
	if platform.machine().endswith(v):
		os_version = v
		break

current_os = None
for o in os_opts:
	if o[0] in platform.system().lower():
		current_os = o[1]
		os_filename = o[2]


def install(file_directory='./lib/', verbose=True, chmod=True, overwrite=False):
	if not current_os or not os_version:
		raise Exception('Cannot determine OS/bitness version! [%s,%s]' % (current_os, os_version))
	latest = requests.get(_base_version).text
	download = _base_download % (latest, current_os, os_version)
	path = os.path.join(os.path.abspath(file_directory), 'chromedriver_%s.zip' % latest)
	out_filename = os.path.join(os.path.abspath(file_directory), os_filename)
	if not overwrite and os.path.exists(out_filename):
		if verbose:
			print('chromedriver is already installed.')
		return out_filename

	if not _download(download, path, verbose):
		if verbose:
			print('Download for %s version failed; Trying alternates.' % os_version)
		for _v in versions:
			download = _base_download % (latest, current_os, _v)
			if _v != os_version and _download(download, path, verbose):
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
	if r.status_code == 404:
		return False
	if r.status_code == 200:
		if not os.path.isdir(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
			return True
	return True


def _extract(path):
	if not os.path.exists(path):
		return False
	with zipfile.ZipFile(path, "r") as zip_ref:
		zip_ref.extractall(os.path.dirname(path))
	os.remove(path)
	return True


if __name__ == "__main__":
	path = install(verbose=True, chmod=True)
	if not os.path.exists(path):
		raise FileNotFoundError('The chromedriver executable was not properly downloaded.')
	print('Chromedriver is installed at: "%s"' % path)
