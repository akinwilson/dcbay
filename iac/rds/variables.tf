variable "name" {
  description = "Name of service"
}

variable "environment" {
  description = "the name of your environment, e.g. \"prod\""
}

variable "sg" {
  description = "security group for rds"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID"
}

variable "snapshot_id" {
  type    = string
  default = ""
}

variable "cluster_identifier" {
  type        = string
  description = "Name of the aurora cluster"
  default     = "mlflow-backend"
}


variable "replication_source_identifier" {
  type        = string
  description = "DB ID to create the read replica from"
  default     = ""
}
variable "instance_count" {
  type        = number
  description = "How many instances in the cluster"
  default     = 1
}
variable "db_pw" {
  description = "Database password"
}
variable "db_user" {
  description = "Database user"
}


variable "db_name" {
  type        = string
  description = "Name of the DB in mysql"
  default     = "main_db"
}

variable "private_subnet" {
  description = "What subnets should the proxy for the db be in"
}