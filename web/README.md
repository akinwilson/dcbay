# cbay

## TESTING 

Running tests with coverage `pip install coverage`
```
coverage run manage.py test
```

```
coverage report
```
outputs: 

```
Name                           Stmts   Miss  Cover
--------------------------------------------------
core/__init__.py                   0      0   100%
core/settings.py                  20      0   100%
core/urls.py                       7      1    86%
manage.py                         12      2    83%
store/__init__.py                  0      0   100%
store/admin.py                    12      0   100%
store/apps.py                      4      0   100%
store/migrations/__init__.py       0      0   100%
store/models.py                   28      1    96%
store/tests/__init__.py            0      0   100%
store/tests/test_models.py         1      0   100%
store/tests/test_views.py          1      0   100%
--------------------------------------------------
TOTAL                             85      4    95%
```


## getting session data from console 
```
from django.contrib.sessions.models import Session
s  = Session.objects.get(pk='li84ol9s2pctiruewxjc4pp3at6sqfnd')
s.get_decoded()
>>> 
{'_auth_user_id': '1', '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend', '_auth_user_hash': 'faec252fe41729e1a1e7ad6ec262d23548aab5b3d49d31c4e8258e775cc2ddbc'}
```



```
django-admin startproject <porject_name>
```
Creates boilerplate code for porject with name _project_name_


```
python manage.py startapp <app_name> 
```
starts app within project

```
python manage.py migrate
```
Propagates changes to code base of models describing ORM to database schema 



```
python manage.py runserver
```
Starts the server 



## **Applications**
### **Admin and authentication** : _django.contrib.admin_ , _django.contrib.auth_

see `./src/first_project/first_project/settings.py` _INSTALLED_APPS_ for other applications that come with django

```
python manage.py createsuperuser
```
creates admin user for DB


### **Custom application**

```
python manage.py startapp <app_name>
```


### Starting containerised DB 
```
docker run --name myPostgresDb -p 5455:5432 -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -e POSTGRES_DB=postgresDB -d postgres
```


# To do 19/11/22

Payment:
the wallet loop needs to be initialised AFTER the webserver first starts up. 

basket:
Clicking on basket without anything in it shows £4.5. 
Added something, then delete, total shows correct amount. Then refresh, total shows the shipping amount. 


# To do 03/05/23 

describe ec2 instanece 
```
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,InstanceType,PublicIpAddress, PrivateIpAddress,Tags[?Key==`Name`]| [0].Value]' --output table

```
get IP address of priv ec2 
```
aws ec2 describe-instances --query 'Reservations[].Instances[].[PublicIpAddress, PrivateIpAddress,Tags[?Key==`Name`]| [0].Value]' --output text | grep priv | grep -Po '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```

1) need to configure production and development environments 
----> cannot easily watch for changes to code to reboot watching server from 
----> need to run server with `python manage.py runserver 0.0.0.0:8000` for it to be able to watch for changes. Currently working on production. Started with `docker-compose.dev.yml` and `docker-compose.prod.yml` files. 


2) prepoluate user form with existing email for shipping form in HTML form `web/cbay/store/templates/payment/home.html`

3) need to test out payment system end to end. 
 ---> should use `wallet.sweep()` method to extract coins from all addresses rather than sending individual coins from server wallet to 

4) need to configure used of production database managed by AWS/terraform or contiunue to use the docker-volumes approach. 
