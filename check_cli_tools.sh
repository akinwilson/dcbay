

GREEN='\033[0;32m'
RESET='\033[0m'

# checking if verion returned is null with -z 
if [ -z "$(docker -v)" ]; then 
  echo "Unable to find docker"
  echo -e "To install docker, please follow this guide: ${GREEN}https://docs.docker.com/get-docker${RESET}"
  exit 1 
fi
# checking if docker-compose is available 
if [ -x "$(command -v docker-compose)" ]; then
  echo "Unable to find docker-compose"
  echo "To install docker-compose, please follow this guide: ${GREEN}https://docs.docker.com/compose/install/linux/${RESET}"
  exit 1
fi 

echo "You have all the required tools for local development. "


# checking for terraform 
if [ -z "$(terraform -v)" ]; then 
  echo "Unable to find terraform"
  echo -e "To install terraform, please follow this guide: ${GREEN}https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli${RESET}"
  exit 1 
fi 

if [ -z "$(aws --version)" ]; then
  echo "Unable to find aws cli."
  echo -e "To install the aws cli, please follow this guide: ${GREEN}https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html${RESET}"
  exit 1 
fi 

echo "You have all the required CLI tools for both local development and remote deployment. Ready to begin. "


