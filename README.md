Facegame
========

Description
-----------
Facegame is a simple game made for learning the faces and names of fellow employees. The game will give you a picture of an employee and you have to select the corresponding name from a few choices. Facegame is a great game for all kinds of organizations where it’s becoming increasingly harder to remember all the faces.

Background
----------
This game was developed as our internal application mainly designed for new employees to get familiar with the names and faces around <a href="http://www.futurice.com">Futurice</a>. Facegame was open sourced as a part of the <a href="http://blog.futurice.com/summer-of-love-of-open-source">Summer of Love</a> program.

About Futurice
--------------

<a href="http://www.futurice.com">Futurice</a> is a lean service creation company with offices in Helsinki, Tampere, Berlin and London. 

People who have contributed to Facegame:   
<a href="https://github.com/mixman">Jussi Vaihia</a>   
<a href="https://github.com/Ozzee">Oskar Ehnström</a>   
Jeremi Saarinen   
<a href="https://github.com/ojarva">Olli Jarva</a>   
Mats Malmstén   
<a href="https://github.com/Wisheri">Ville Tainio</a>   

Installation
------------

First step is to install <a href="http://www.docker.com/">docker</a> on your system.

To build the system:   
`docker build -t <your image name> .`

To run the container:   
`docker run -t -i -p 8000:8000 <your image name>`

For authentication the app uses RemoteUser. To run the system inside the docker container:
``` 
source /opt/ve/facegame/bin/activate   
export DJANGO_SETTINGS_MODULE=facegame.settings.settings   
DJANGO_SETTINGS_MODULE=facegame.settings.settings REMOTE_USER=<your username> python manage.py runserver --nostatic --traceback   
DJANGO_SETTINGS_MODULE=facegame.settings.settings python watcher.py   
```
Test data for the application is located at `test_data.json`. To modify the application to use your own json file, change `USER_DATA` at settings.

Dependancies for Facegame are located at the requirements.txt-file. You can install them manually by:   
`pip install -r requirements.txt.`

Support
-------
Pull requests and new issues are of course welcome. If you have any questions, comments or feedback you can contact us by email at sol@futurice.com. We will try to answer your questions, but we have limited manpower so please, be patient with us.
