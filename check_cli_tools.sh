#!/usr/bin/env bash 


set -e 
# checking if verion returned is null with -z 
if [ -z "$(docker -v)" ]; then 
  echo "Unable to find docker"
  echo "To install docker, please follow this guide: https://docs.docker.com/get-docker"
  exit 1 
fi
# checking if docker-compose is available 
if [ -z "$(docker-compose -v)" ]; then
  echo "Unable to find docker-compose"
  echo "To install docker-compose, please follow this guide: https://docs.docker.com/compose/install/linux/"
  exit 1
fi 

echo "You have all the required tools for local development. "


# checking for terraform 
if [ -z "$(terraform -v)" ]; then 
  echo "Unable to find terraform"
  echo "To install terraform, please follow this guide: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli"
  exit 1 
fi 

if [ -z "$(aws -v)" ]; then
  echo "Unable to find aws cli."
  echo "To install the aws cli, please follow this guide: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
  exit 1 
fi 

echo "You have all the required CLI tools for both local development and remote deployment. Ready to begin. "


