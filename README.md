# dcbay 
![](img/dcbay.jpg "markets")

## Overview
dcbay, standing for remotely **d**eployed ***c***rypto-currencies **bay**, is a repository containing  the infrastructure as code and application code to host a [e-commerece](https://en.wikipedia.org/wiki/E-commerce) platform  with an integrated crypto-currency payment gateway - [Bitcoin](https://bitcoin.org/en/) so far - remotely on the AWS infrastructure. To achieve this, [Terraform](https://www.terraform.io/) is used as the infrastructure as code language, [python](https://www.djangoproject.com/) for the application code - particularly utilising the library [django](https://www.djangoproject.com/); the full-stack development library, and [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/). Legacy payment systems serve the interest of archaic banking systems. Whilst the trading of crypto-currencies has expontentially increased since the inception of bitcoin, their use as a means of exchange of value in business transactions as lagged behind. This could mainly be attributed two source: regulations and a lack of technical expertise. This repository aims to illuminate this required technical expertise, hopefully accelerating the  adoption of cryto-currencies as a payment system.

## Usage 
The repository has been set up to allow contiunal development upon the platform. I.e. configuration for both a development and production environment can be found. The `iac/` folder contains logic related to the infrastructure, and `web/` related to the application code itself. To ensure you have all the required CLI tools, please run the script:
```
./check_cli_tools.sh
```

### Development 
For local development, first clone the repository and run a script that will spin up a server locally, which automatically updates to any changes made to the repository
```
./web/cbay/development.sh
```
Since we have adopted a containerised workflow 
```
docker-compose -f dc.dev.yaml up 
```




### Deployment
Again, clone the repository. To deploy the application to AWS, you will need to provision the required resources to host the site. You will also need AWS credentials to an AWS account. First and foremost, create a [state-store](https://developer.hashicorp.com/terraform/language/state/backends) for terraform to use in order to remotely track the infrastructure deployed. 

```
./iac/utils/crreate-s3-tf-backend-bucket.sh 
```
******
**Note**: this bucket has been created **without** terraform. Hence, you must manage and track it on your own. Deleting it when you stop hosting the site. For this, a script is provide. 

next you will next to plan and infra deployment. You can do this by running: 
```
terraform plan
```
check the output such that you are happy with the resources that are about to be provisioned. If so, run 
```
terraform apply
```



Next, we need to use the [ssh](https://en.wikipedia.org/wiki/Secure_Shell) protocol to securely connect to our [EC2](https://aws.amazon.com/ec2/) instance in order to transfer over our application code. This workflow does not follow [gitOps](https://about.gitlab.com/topics/gitops/) design principals but still, it allows for the deployment. The command for this will look something like:
```
ssh -i "~/ssh/aws-dev-key" ubuntu@ec2-3-146-3.eu-west-2.compute.amazonaws.com 
```

After this, we can use the [scp](https://en.wikipedia.org/wiki/Secure_copy_protocol) (secure copy protocol) in order to transfer our application code to our EC2 instance. 
```
scp -r ./web/ ubuntu@webserver:~/
```



## Further improvements 
1) Currently, end-users of the site can only choose bitcoin as a payment option. An improvment would be to also integrate more accepted crypto-currenies like for example [monero](https://www.getmonero.org/). 
2) Git synchronizer. Currently, any application code changes made to platform need to be manually update via using ssh and scp. It would be benefical to automatically synchronize with a remote git repository instead of following this manual workflow. 
3) Currently, the storage available locally to the EC2 instance is used to store the database. It would be benefical to use something like [aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html) to off-load the responsibility of persistence to an external service. 
4) [Multi-tenancy](https://en.wikipedia.org/wiki/Multitenancy) platform. Instead of the platform allowing for a single e-commerce site to be generated, it would be benefical if user of the platform could *prop-up* their own store fronts, under subdomains,  on the platform. Similar to [shopify](https://www.shopify.com/uk)'s business model.

# TODO 21 Jan 2025:
- [ ] Set up containerised development environment. 
- [ ] Generated script to deploy infrastructure 
- [ ] Generate script to remove infrastructure 
- [ ] write more tests for platform. 
- [ ] Integrate monero as payment option
- [ ] Integrate multi-tenancy. 


