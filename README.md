## HTTPlay~~ground~~

#### _Custom HTTP Handler_

##### Requirments:
* python 3.7.x
* Jinja2 2.10.1

##### Installation dependencies:

    pip install -r requirements.txt
    
##### Usage:
* Run 2 servers:

      python run_server.py 0
      python run_server.py 1

  0 - main server (GET form)<br>
  1 - accessory server (authorization, main processing)

* Check "URL1:PORT1/form" specified in _HTTPlayground/settings.py_
