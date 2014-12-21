## How to Install iPython (on Mac)
```
sudo su
pip install ipython
pip install pygment
pip install numpy
brew update
brew install sip
brew install pyqt
brew install -vd pyside  #this takes a long time, so better verbose it
```

## How to run..
```
export PYTHONPATH=$PYTHONPATH:/<where your python lib is>/site-packages # (e.g. $PYTHONPATH:/usr/local/lib/python2.7/site-packages) 
sudo chmod -R 755 /<where your python lib is>/site-packages
ipython qtconsole
```
## For iPython Notebook..
```
pip install Jinja2
pip install tornado
```
## Start iPython Server..
Go to the code repo directory to start notebook server
```
ipython notebook
```
## Run iPython Notebook Page
Go to your browser and enter this address:
```
http://localhost:8888/notebooks/DIVER%20Adapter.ipynb
```
You'll see the instructions on how to run the main features. 
