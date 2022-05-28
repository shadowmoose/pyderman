from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import tarfile
import zipfile
from os.path import abspath, basename, dirname, isfile, join
from types import ModuleType

from pyderman import drivers
from pyderman.drivers import all_drivers, chrome, edge, firefox, opera, phantomjs
from pyderman.util import downloader

_versions = sorted(["32", "64"], key=lambda _v: not platform.machine().endswith(_v))
_os_opts = [("win", "win", ".exe"), ("darwin", "mac", ""), ("linux", "linux", "")]

_current_os = None
_ext = ""
for _o in _os_opts:
    if _o[0] in platform.system().lower():
        _current_os = _o[1]
        _ext = _o[2]
if (
    _current_os == "mac"
    and shutil.which("sysctl")
    and subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
    .decode("utf-8")
    .lower()
    .startswith("apple m1")
):
    _current_os = "mac-m1"


def install(
    browser: ModuleType | None = None,
    file_directory: str = "./lib/",
    verbose: bool = True,
    chmod: bool = True,
    overwrite: bool = False,
    version: str = "latest",
    filename: str | None = None,
    return_info: bool = False,
) -> str | dict[str, str | None] | None:
    """
    Downloads the given browser driver, and returns the path it was saved to.

    :param browser: The Driver to download. Pass as `pyderman.chrome/firefox/etc.`. Default Chrome.
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
        raise Exception(f"Cannot determine OS version! [{platform.system()}]")
    if not version:
        version = "latest"
    if not browser:
        browser = drivers.chrome

    for _os_bit in _versions:
        data = browser.get_url(version=version, _os=_current_os, _os_bit=_os_bit)
        if not data:
            continue
        driver_path, url, ver = data
        driver = basename(driver_path)
        exts = [e for e in [".zip", ".tar.gz", ".tar.bz2"] if url.endswith(e)]
        if len(exts) != 1:
            raise Exception(
                f"Unable to locate file extension in URL: {url} ({','.join(exts)})"
            )
        archive = exts[0]

        archive_path = join(abspath(file_directory), f"{driver}_{ver}{archive}")
        file_path = join(abspath(file_directory), f"{driver}_{ver}{_ext}")
        if filename:
            file_path = join(abspath(file_directory), filename)

        if not overwrite and isfile(file_path):
            if verbose:
                print(f"{driver} is already installed.")
            return file_path

        if not _download(url, archive_path, verbose):
            if verbose:
                print(f"Download for {_os_bit} version failed; Trying alternates.")
            continue

        out = _extract(archive_path, driver_path, file_path)
        if out is not None and chmod is not None:
            mode = os.stat(out).st_mode
            mode |= (mode & 0o444) >> 2  # copy R bits to X
            os.chmod(out, mode)

        if return_info:
            return {"path": out, "version": str(ver), "driver": str(driver)}
        return out
    raise Exception("Unable to locate a valid Web Driver.")


def _download(url: str, path: str, verbose: bool = True) -> bool:
    if verbose:
        print("\tDownloading from: ", url)
        print("\tTo: ", path)
    return downloader.binary(url, path)


def _extract(path: str, driver_pattern: str, out_file: str) -> str | None:
    """
    Extracts zip files, or tar.gz files.
    :param path: Path to the archive file, absolute.
    :param driver_pattern:
    :param out_file:
    :return: extracted file path.
    """
    path = abspath(path)
    out_file = abspath(out_file)
    if not isfile(path):
        return None
    tmp_path = join(dirname(out_file), f"tmp_dl_dir_{basename(path)}")
    zip_ref: zipfile.ZipFile | tarfile.TarFile | None = None
    namelist: list[str] = []
    if path.endswith(".zip"):
        zip_ref = zipfile.ZipFile(path, "r")
        namelist = zip_ref.namelist()
    elif path.endswith(".tar.gz"):
        zip_ref = tarfile.open(path, "r:gz")
        namelist = zip_ref.getnames()
    elif path.endswith(".tar.bz2"):
        zip_ref = tarfile.open(path, "r:bz2")
        namelist = zip_ref.getnames()
    if not zip_ref:
        return None
    ret = None
    for n in namelist:
        if re.match(driver_pattern, n):
            zip_ref.extract(n, tmp_path)
            ret = join(tmp_path, n)
    zip_ref.close()
    if ret:
        if isfile(out_file):
            os.remove(out_file)
        os.rename(ret, out_file)
        shutil.rmtree(tmp_path)
        ret = out_file
    os.remove(path)
    return ret


__all__ = [
    "drivers",
    "all_drivers",
    "chrome",
    "edge",
    "firefox",
    "opera",
    "phantomjs",
    "downloader",
    "install",
]

if __name__ == "__main__":
    install(drivers.opera, overwrite=True)
