## How to Install iPython Notebook 

1. Go to http://continuum.io/downloads
2. Click on 'I want Python 3.4'
3. Click on Graphical Installer to download
4. Run the downloaded installer
5. Run this command: 
```
conda update conda
```
6. Run this command: 
```
conda update ipython ipython-notebook ipython-qtconsole
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

First, make sure you have 'pip' installed. Then, install the following packages:

```
sudo su
pip install sure
pip install httpretty
```

Now go into the 'notebook' directory, then run command to execute all unit tests

```
cd divermodc/notebook
python -m unittest discover -s tests/ -p 'test_*.py'
```
