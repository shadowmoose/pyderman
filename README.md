# Chromedriver installer

This is a super-simple package that can automatically find & download the newest (or whichever you speficy) version of 
the chromedriver executable.

It should work on Windows/Linx/Mac, and also supports os-specific permissions.

To install the library, run:
```
pip install chromedriver-install
```


Then call it in your code like so:
```python
import from chromedriver_install
path = chromedriver_install.install(file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version=None)
print('Installed chromedriver to path: %s' % path)
```

There are options for the output directory, disabling printout, running chmod on the downloaded executable, automatic overwriting, and version number.