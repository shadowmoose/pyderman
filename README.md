# Chromedriver installer  [![Build Status](https://travis-ci.com/shadowmoose/chrome_driver.svg?branch=master)](https://travis-ci.com/shadowmoose/chrome_driver)

This is a super-simple package that can automatically find & download the newest (or whichever you specify) version of 
the chromedriver executable.

It should work on Windows/Linx/Mac, and also supports os-specific permissions.

To install the library, run:
```
pip install chromedriver-install
```


Then call it in your code like so:
```python
import chromedriver_install as cdi
path = cdi.install(file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version=None)
print('Installed chromedriver to path: %s' % path)
```

There are options for the output directory, disabling printout, running chmod on the downloaded executable, automatic overwriting, and version number.
