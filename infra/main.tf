terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  profile = var.aws_profile
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  bucket_prefix = "pdfgen-"
  acl = "private"
  force_destroy = true

  lifecycle_rule {
    id = "expiration"
    enabled = true
    expiration {
      days = 7
    }
  }
  
  tags = {
    Name        = "pdfgen ${var.environment}"
    Environment = var.environment
  }
}