## How to Install iPython Notebook (on Mac)
```
sudo su
pip install ipython
pip install pygment
pip install numpy
brew update
brew install sip
brew install pyqt
brew install -vd pyside  #this takes a long time, so better verbose it
pip install Jinja2
pip install tornado
pip install requests
```

## Set paths and permissions..
```
export PYTHONPATH=$PYTHONPATH:/<where your python lib is>/site-packages # (e.g. $PYTHONPATH:/usr/local/lib/python2.7/site-packages) 
sudo chmod -R 755 /<where your python lib is>/site-packages
```

## Start iPython Notebook Server..

Get the code from the repository
```
git clone https://github.com/IntersectAustralia/divermodc.git
```

Go to the 'notebook' directory to start notebook server
```
cd divermodc/notebook
ipython notebook
```

Once the server is started, your browser will automatically open to the correct page. 

## Open iPython Notebook Page 
Assuming you already have the iPython Notebook server started, go to your browser and enter this address:
```
http://localhost:8888/notebooks/DIVER%20Adapter.ipynb
```
You'll see the instructions on how to run the main features. 

## Run unit tests

Go into the 'notebook' directory, then run command to execute all unit tests

```
cd divermodc/notebook
python -m unittest discover -s tests/ -p 'test_*.py'
```
