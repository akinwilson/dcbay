## Local development 

### Development outside of container for hotreloading 

Currently, it is difficult for developers to quickly develop upon the application since the webserver needs to access domain names of services like [celery](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) or persistence layers like [redis](https://en.wikipedia.org/wiki/Redis), where these services receive their domain names  via `docker-compose`. To avoid having to continously swtich between in and outer container development, review [this blog](https://docs.appseed.us/technologies/django/docker-auto-reload/). 

You can try to run `./`

1) Load the environment variables files form `web/cbay/`:

```export $(cat ../dev.env | xargs) && export PRIVATE_MNEMONIC="case loan concert avocado mercy today sauce ring come special spawn ship"```

from inside diretory `web/`

For some reason, exporting a long env varaible using the above doesnt work for `PRIVATE_MNEMONIC`.  

_In `./prod.env` database `HOST` variable is network name corresponding to container rather than localhost and it sets the `BCL_CONFIG_FILE` env varaible for setting the logging config location (it's set to inside the container)_

2) Run containerised postgres DB

```
docker run -e POSTGRES_USER='postgresUser' -e POSTGRES_PASSWORD='postgresPW' -e POSTGRES_DB='postgresDB' -e POSTGRES_HOST="localhost" -e POSTGRES_PORT=5432 -e BITCOIN_DB='bitcoinlib' -e BITCOIN_USER='bitcoinlib' -e BITCOIN_PASSWORD='password' -e BITCOIN_HOST="localhost" -e BITCOIN_PORT=5432 -p 5432:5432  web_postgres
```
__Assuming that the `web_postgres` container has already been built__


4) Make and apply migrations another termial (you need to load the environment variables again for the new termial session) 
Inside `web/cbay/` run:

`python manage.py makemigrations && python manage.py migrate`

5) Load dummy data into DB: 

from inside `web/cbay`

`python manage.py loaddata ./fixtures/data.json`


6) Head to `http://127.0.0.1:8000/` in two different browsers.


## Handling SSL with letsencrypt rather than AWS.

The script `init-letsencrypt.sh` is an artefact from following [this blog](https://mindsers.blog/post/https-using-nginx-certbot-docker/). 

This is only necessary if I am exposing the the webserver directly to the internet, and not behind a load balancer that can use AWS' on certificate authority. 


