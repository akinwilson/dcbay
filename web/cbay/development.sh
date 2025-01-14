echo "Starting services for local development"
set -x 
echo "exporting development environment variables ... "
export $(cat ../.dev.env | xargs) 
echo "overwriting PRIVATE_MNEMONIC ...."
export PRIVATE_MNEMONIC="case loan concert avocado mercy today sauce ring come special spawn ship"
echo "spinning up database container in detached mode ... "
docker build . -f Dockerfile.postgres -t web_postgres:latest 
docker run -d -e POSTGRES_USER='postgresUser' -e POSTGRES_PASSWORD='postgresPW' -e POSTGRES_DB='postgresDB' -e POSTGRES_HOST="localhost" -e POSTGRES_PORT=5432 -e BITCOIN_DB='bitcoinlib' -e BITCOIN_USER='bitcoinlib' -e BITCOIN_PASSWORD='password' -e BITCOIN_HOST="localhost" -e BITCOIN_PORT=5432 -p 5432:5432  web_postgres
echo "Making migrations and applying ... "
python manage.py makemigrations && python manage.py migrate
echo "Loading development data into database ... "
python manage.py loaddata ./fixtures/data.json
echo "starting development server ..."
python manage.py runserver