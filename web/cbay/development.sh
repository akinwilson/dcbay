#!/bin/sh

# colours 
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
# reset 
RESET='\033[0m'


echo "\nStarting services for ${GREEN}local development${RESET}...\n"
echo "\n${RED}NOTE${RESET}: transitioning over to a complete containerised workflow. Currently, only running DB in and container. But as application grew, more and more serivces need to be added\n"
echo "\nBlog ${GREEN}https://docs.appseed.us/technologies/django/docker-auto-reload${RESET} teaches you how to run the django server in a production environment with hot-reloading enabled inside a container.\n\n"

echo "exporting development environment variables ... "
export $(cat ../dev.env | xargs) 
export PRIVATE_MNEMONIC="case loan concert avocado mercy today sauce ring come special spawn ship"
echo "Due to ${LIGHTPURPLE}ENV_VARIABLE${RESET} length constrained via ${LIGHTBLUE}xgars${RESET}, overwriting ${LIGHTPURPLE}PRIVATE_MNEMONIC${RESET} variable such that:\n\n${LIGHTPURPLE}PRIVATE_MNEMONIC${RESET}=${YELLOW}${PRIVATE_MNEMONIC}${RESET}\n\n"
filename="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"

echo "${RED}NOTE${RESET}: This means there are two places; ${LIGHTCYAN}dev.env${RESET} and this file; ${LIGHTCYAN}${filename}${RESET}, where the ${LIGHTPURPLE}PRIVATE_MNEMONIC${RESET} appears, but ${LIGHTCYAN}${filename}${RESET} takes president and sets its value."

echo "Want to be able to set ${LIGHTPURPLE}ENV_VARIABLE${RESET} in one place, ${LIGHTCYAN}dev.env${RESET}"


echo "spinning up database container in detached mode ... "
docker build . -f Dockerfile.postgres -t web_postgres:latest 
docker run -d -e POSTGRES_USER='postgresUser' -e POSTGRES_PASSWORD='postgresPW' -e POSTGRES_DB='postgresDB' -e POSTGRES_HOST="localhost" -e POSTGRES_PORT=5432 -e BITCOIN_DB='bitcoinlib' -e BITCOIN_USER='bitcoinlib' -e BITCOIN_PASSWORD='password' -e BITCOIN_HOST="localhost" -e BITCOIN_PORT=5432 -p 5432:5432  web_postgres
echo "Making migrations and applying ... "
python manage.py makemigrations && python manage.py migrate
echo "Loading development data into database ... "
python manage.py loaddata ./fixtures/data.json
echo "starting development server ..."
python manage.py runserver