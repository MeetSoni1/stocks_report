# Variables declared in .tfvars file

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

variable "aws_access_key" {
  description = "AWS user access key"
  type        = string
}
variable "aws_secret_access_key" {
  description = "AWS user secret access key"
  type        = string
}

# Configure the AWS Provider
provider "aws" {
  region     = "eu-central-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_access_key
}