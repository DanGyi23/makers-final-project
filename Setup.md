# Chessy Setup:

**Install Python in Terminal**
- `brew install python` (on Mac)
<br><br>

**Install pip, PYtest, pytest-cov and slackclient**
<br>
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
python3 -m pip install pytest
python3 -m pip install pytest-cov
python3 -m pip install slackclient
python3 -m pip install --user pillow
python3 -m pip install python-chess
python3 -m pip install cairosvg
brew install cairo
```


**Running PYtest**
- In Project root dir, as with rspec, just type `python3 -m pytest`
- Coverage report `python3 -m pytest --cov ./`
