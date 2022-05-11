# Pyderman (Selenium Web Driver Installer)

[![Ubuntu](
  https://github.com/shadowmoose/pyderman/workflows/Ubuntu/badge.svg
  )](
  https://github.com/shadowmoose/pyderman/actions?query=workflow%3AUbuntu
) [![MacOS](
  https://github.com/shadowmoose/pyderman/workflows/MacOS/badge.svg
  )](
  https://github.com/shadowmoose/pyderman/actions?query=workflow%3AMacOS
) [![Windows](
  https://github.com/shadowmoose/pyderman/workflows/Windows/badge.svg
  )](
  https://github.com/shadowmoose/pyderman/actions?query=workflow%3AWindows
) [![MacOS (SUR)](
  https://github.com/shadowmoose/pyderman/actions/workflows/test-macOS-sur.yml/badge.svg
  )](
  https://github.com/shadowmoose/pyderman/actions/workflows/test-macOS-sur.yml
)

This is a fast, simple, dependency-free package that can automatically find & download any version of
the *Google Chrome (chromeDriver), Firefox (geckoDriver), PhantomJS, Opera (operaDriver), and Edge (edgeDriver)* web drivers.

This project was built to allow developers to seamlessly include selenium support on the user-side, without requiring any manual configuration on their part. It will automatically locate the correct driver binary for the platform & version you choose, as well as setting the os-specific permissions after downloading.

It is [tested daily](https://github.com/shadowmoose/pyderman/actions) on Windows/Linux/macOS against Python versions 3.7+.

## Installation

To install the library, run:

```bash
pip install pyderman
```

## Usage

After installed, call it in your code like so:

```python
import pyderman as driver
path = driver.install(browser=driver.firefox)
print('Installed geckodriver driver to path: %s' % path)
```

There are options for the output directory, disabling printout, running chmod on the downloaded executable,
automatic overwriting, executable file name, and version number.
All parameters are optional, and the default values are listed below.

This example downloads the Chrome Driver instead, by changing ```browser``` like so:

```python
import pyderman as dr
path = dr.install(browser=dr.chrome, file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version=None, filename=None, return_info=False)
print('Installed chromedriver to path: %s' % path)
```

The download is very fast, and will skip downloading if the file already exists. This behavior can be toggled with ```overwrite```.

## Notes

### Note on MS Edge

Microsoft has switched Edge to use a flavor of Chrome behind the scenes. As of October 2019, Pyderman will download this MS Chromium Driver. Their driver is experimental, so make sure you know what you're doing if you use this driver. If you require stability, it is recommended you specify a version instead of using the "latest".

### Note on macOS

Some versions of macOS have certificate issues with Python. Typically, in recent versions of Python, it will prompt you to install these when you install Python. Since Python needs these installed in order to make https requests, you may need to install these first. Depending on your project, it may also be possible to include a library to automatically import these certificates. Please visit [this link](https://timonweb.com/tutorials/fixing-certificate_verify_failed-error-when-trying-requests_html-out-on-mac/) to learn more.

### Note on Big Sur

Apple broke a ton of compatibility moving to Big Sur, and now many of the web drivers do not have working builds within the new architecture. This project will only halfheartedly attempt to keep any drivers working on Big Sur architecture until all the available drivers have stable release patterns for the platform.

## Why's it called 'Pyderman'?

Because it installs *web*-drivers. [Get it?](https://youtu.be/4o29VoxtsFk)
