variable "aws_region" {
  default = "eu-north-1"
}

variable "project_name" {
  default = "cloud-lab1"
}

variable "db_username" {
  default = "postgres"
}

variable "db_password" {
  description = "Password for RDS PostgreSQL"
  type        = string
  sensitive   = true
}

variable "db_name" {
  default = "appdb"
}