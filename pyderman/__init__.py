import platform
import os
from os.path import join, dirname, isfile, abspath, basename
import zipfile
import tarfile
from pyderman import chrome, firefox, downloader


_versions = sorted(['32', '64'], key=lambda _v: not platform.machine().endswith(_v))
_os_opts = [('win', 'win', '.exe'), ('darwin', 'mac', ''), ('linux', 'linux', '')]

_current_os = None
_ext = ''
for _o in _os_opts:
	if _o[0] in platform.system().lower():
		_current_os = _o[1]
		_ext = _o[2]


def install(browser=chrome, file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version='latest', filename=None, return_info=False):
	"""
	Downloads the given browser driver, and returns the path it was saved to.

	:param browser: The Driver to download. Pass as `pyderman.chrome/firefox`. Default Chrome.
	:param file_directory: The directory to save the driver.
	:param verbose: If printouts are okay during downloading.
	:param chmod: If True, attempt to make the downloaded driver executable.
	:param overwrite: If true, overwrite existing drivers of the same version.
	:param version: The version to download. Default 'latest'.
	:param filename: The filename to save the driver to. Defaults to driver-specific.
	:param return_info: If True, return an Object with more download information.
	:return: The absolute path of the downloaded driver, or None if something failed.
	"""
	if not _current_os:
		raise Exception('Cannot determine OS version! [%s]' % platform.system())
	if not version:
		version = 'latest'
	if not browser:
		browser = chrome

	for _os_bit in _versions:
		data = browser.get_url(version=version, _os=_current_os, _os_bit=_os_bit)
		if not data:
			continue
		driver, url, ver = data

		archive = '.zip' if url.endswith('.zip') else '.tar.gz'

		archive_path = join(abspath(file_directory), '%s_%s.%s' % (driver, ver, archive))
		file_path = join(abspath(file_directory), '%s_%s%s' % (driver, ver, _ext))
		if filename:
			file_path = join(abspath(file_directory), filename)

		if not overwrite and isfile(file_path):
			if verbose:
				print('%s is already installed.' % driver)
			return file_path

		if not _download(url, archive_path, verbose):
			if verbose:
				print('Download for %s version failed; Trying alternates.' % _os_bit)
			continue

		out = _extract(archive_path, driver, file_path)
		if out and chmod:
			mode = os.stat(out).st_mode
			mode |= (mode & 0o444) >> 2    # copy R bits to X
			os.chmod(out, mode)

		if return_info:
			return {
				'path': out,
				'version': ver,
				'driver': driver
			}
		return out


def _download(url, path, verbose=True):
	if verbose:
		print('\tDownloading from: ', url)
		print('\tTo: ', path)
	return downloader.binary(url, path)


def _extract(path, driver, out_file):
	"""
	Extracts zip files, or tar.gz files.
	:param path: Path to the archive file, absolute.
	:param driver:
	:param out_file:
	:return:
	"""
	path = abspath(path)
	out_file = abspath(out_file)
	if not isfile(path):
		return None
	tmp_path = join(dirname(out_file), 'tmp_dl_%s' % basename(path))
	zip_ref, namelist = None, None
	if path.endswith('.zip'):
		zip_ref = zipfile.ZipFile(path, "r")
		namelist = zip_ref.namelist()
	elif path.endswith('.tar.gz'):
		zip_ref = tarfile.open(path, "r:gz")
		namelist = zip_ref.getnames()
	if not zip_ref:
		return None
	ret = None
	for n in namelist:
		if n.startswith(driver):
			zip_ref.extract(n, tmp_path)
			ret = join(tmp_path, n)
	zip_ref.close()
	if ret:
		if isfile(out_file):
			os.remove(out_file)
		os.rename(ret, out_file)
		os.rmdir(tmp_path)
		ret = out_file
	os.remove(path)
	return ret

