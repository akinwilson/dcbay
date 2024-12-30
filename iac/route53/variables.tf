variable "name" {
  description = "Name of service"
}

variable "environment" {
  description = "the name of your environment, e.g. \"prod\""
}

variable "ttl" {
  description = "time to live"
  default     = 60
}

variable "domain_name" {
  description = "domain name to"
}

variable "alb" {
  description = "Application balancer for route53 to point at"
}