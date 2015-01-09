## How to Install iPython Notebook 

First, make sure you have Python and pip installed. 
On Mac, pip comes with your Python installation. On Ubuntu, you can get pip by running the following command:
```
sudo apt-get install python-pip python-dev build-essential 
```

Now run the following commands to install iPython Notebook and all dependencies:
```
sudo su
pip install "ipython[notebook]"
pip install requests
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

First, install the following packages:

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
