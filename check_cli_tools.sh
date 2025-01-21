#!/bin/sh

GREEN='\033[0;32m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
YELLOW='\033[1;33m'
# reset 
RESET='\033[0m'


project_title=$(cat <<"EOF"

     _      _                 
  __| | ___| |__   __ _ _   _ 
 / _` |/ __| '_ \ / _` | | | |
| (_| | (__| |_) | (_| | |_| |
 \__,_|\___|_.__/ \__,_|\__, |
                        |___/ 

EOF
)

echo "${YELLOW}${project_title}${RESET}"


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

echo "\n\nYou have all the required tools for ${LIGHTCYAN}local development${RESET}."


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

echo "You have all the required CLI tools for both ${LIGHTCYAN}local development${RESET} and ${LIGHTPURPLE}remote deployment${RESET}.\n\nReady to begin."


