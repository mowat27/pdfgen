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

# -- SNS -----------------------------------------------------------------------

resource "aws_sns_topic" "this" {
  name_prefix = "pdfgen-"

policy = <<POLICY
{
    "Version":"2012-10-17",
    "Statement":[{
        "Effect": "Allow",
        "Principal": {
            "Service": "s3.amazonaws.com"
            },
        "Action": "SNS:Publish",
        "Resource": "arn:aws:sns:${var.aws_region}:${var.aws_account}:pdfgen-*",
        "Condition":{
            "ArnLike":{"aws:SourceArn":"${aws_s3_bucket.this.arn}"}
        }
    }]
}
POLICY
}

# -- S3 ------------------------------------------------------------------------

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

# resource "aws_s3_bucket_notification" "this" {
#   bucket = aws_s3_bucket.this.id

#   topic {
#     topic_arn     = aws_sns_topic.this.arn
#     events        = ["s3:ObjectCreated:*"]
#     filter_suffix = ".pdf"
#   }
# }