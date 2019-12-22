#Python HTTP Server

This is a simple HTTP server made in Python3 for the Indoor Location Framework.

>Make sure `python3`  is intalled in your computer, along with its version of `pip`.
This project was developed using `virtualenvirorment` and all the required dependencies are specified in the file __requeriments.txt__. If you are going to use it as well make sure that it's also installed.

To set it up and run it:

Create a new dir where your virtualenvirorment will be created.
```
mkdir venv
``` 
Create the virtual envirorment using your `python3` interpreter. This will install the interpreter and the required tools setup the required dependencies, like `pip`.
```
virtualenv -p <path-to-python3> venv
```
Start the `virtualenv`. Now, it will use the tools from the virtual envirorment.  
```
source venv/bin/activate
``` 
Install all dependencies
``` 
pip install -r requeriments.txt
``` 

Once all requeriments are installed, start the server by calling
``` 
python api.py
``` 

To desactivate the virtualenvirorment, run.
``` 
deactivate
``` 

  

