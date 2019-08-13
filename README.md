## HTTPlay~~ground~~

#### _Custom HTTP Handler_

##### Requirments:
* python 3.7.x
* Jinja2 2.10.1

##### Installation dependencies:

    pip install -r requirements.txt
    
##### Usage:
Run 2 servers:
    
    python path_to_main.py 0
    python path_to_main.py 1
    
0 - main server (GET form)<br>
1 - accessory server (authorization, main processing)