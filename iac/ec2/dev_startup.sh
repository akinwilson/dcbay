#!/bin/bash
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" -y
sudo apt update -y 
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
sudo docker --version
# make volume location for docker-compose to use as db and pg admin storage location 
# sudo mkdir -p /home/ubuntu/website/data
# sudo sudo chown -R 5050:5050 /home/ubuntu/website/data 
