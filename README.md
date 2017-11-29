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

Build facegame:
```
docker build -t facegame .
```

Setup database container:
```
docker run --name postgres -e POSTGRES_PASSWORD=secret -d postgres
docker exec -it postgres sh -c "dropdb -Upostgres facegame"
docker exec -it postgres sh -c "createdb -Upostgres facegame"
```

Run facegame locally at http://localhost:8000
```
docker run --rm -it -p 8000:8000 --name facegame \
    -e DB_USER=postgres \
    -e DB_PASSWORD=secret \
    -e DB_HOST=postgres \
    -e FAKE_LOGIN=true \
    -e REMOTE_USER=myusername \
    -e DEBUG=true \
    --link postgres:postgres \
    facegame
```

TODO: deprecate FUM_API_URL,FUM_API_TOKEN => fetching .json

Env vars DEBUG, FAKE_LOGIN and REMOTE_USER are for local development only.

Support
-------
Pull requests and new issues are of course welcome. If you have any questions, comments or feedback you can contact us by email at sol@futurice.com. We will try to answer your questions, but we have limited manpower so please, be patient with us.
