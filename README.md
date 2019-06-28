# Pyderman (Selenium Web Driver Installer) [![Build Status](https://dev.azure.com/theshadowmoose/theshadowmoose/_apis/build/status/shadowmoose.pyderman?branchName=master)](https://dev.azure.com/theshadowmoose/theshadowmoose/_build/latest?definitionId=1&branchName=master)

This is a fast, simple, dependency-free package that can automatically find & download any version of 
the Google Chrome (chromedriver), Firefox (geckodriver), PhantomJS, and Opera (operadriver) web drivers.

This project was built to allow developers to seamlessly include selenium support on the user-side, without requiring any manual configuration on their part. It will automatically locate the correct driver binary for the platform & version you choose, as well as setting the os-specific permissions after downloading.

It is tested daily on Windows/Linux/macOS against Python versions 3.5+. [![Build Status](https://travis-ci.com/shadowmoose/pyderman.svg?branch=master)](https://travis-ci.com/shadowmoose/pyderman)

To install the library, run:
```
pip install pyderman
```


Then call it in your code like so:

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

## Why's it called 'Pyderman'?
Because it installs *web*-drivers. [Get it?](https://youtu.be/SUtziaZlDeE)
