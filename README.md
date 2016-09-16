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

<a href="http://www.futurice.com">Futurice</a> is a lean service creation company with offices in Helsinki, Tampere, Berlin, London, Stockholm and Munich. 

People who have contributed to Facegame:   
<a href="https://github.com/mixman">Jussi Vaihia</a>   
<a href="https://github.com/Ozzee">Oskar Ehnström</a>   
Jeremi Saarinen   
<a href="https://github.com/ojarva">Olli Jarva</a>   
Mats Malmstén   
<a href="https://github.com/Wisheri">Ville Tainio</a>   

Installation
------------

Facegame runs on docker with the database in a separate container. First set all the secrets and other missing configuration to `local_settings.py` or to `settings.py`. You have to set at least FUM_API_URL and FUM_API_TOKEN for fetching user pictures, database credentials and django secret key. 

When configuration is done, build facegame:
```
docker build -t facegame .
```

Then run database container (we use the default postgres container):

```
docker run -e POSTGRES_USER=<your db user> -e POSTGRES_DB=<your db name> postgres
```
Then find out the ip address of your postgres container (with `docker inspect`for example) and start facegame container. If you want have a password in your database, give it as environment variable POSTGRES_PASSWORD. 

```
docker run -p 80:8000 -e DB_HOST=<postgres container ip> facegame
```

If you are developing locally, set FAKE_LOGIN to True. This enables a middleware that authenticates you as the user given in settings.REMOTE_USER. Always set FAKE_LOGIN to False in production 


Support
-------
Pull requests and new issues are of course welcome. If you have any questions, comments or feedback you can contact us by email at sol@futurice.com. We will try to answer your questions, but we have limited manpower so please, be patient with us.
