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

# -- SQS -----------------------------------------------------------------------

resource "aws_sqs_queue" "input" {
  name_prefix = "pdfgen-input-"
  
  visibility_timeout_seconds = 30
  message_retention_seconds = 60

  receive_wait_time_seconds = 10

  tags = {
    Environment = "dev"
  }
}

resource "aws_sqs_queue" "output" {
  name_prefix = "pdfgen-output-"
  
  visibility_timeout_seconds = 30
  message_retention_seconds = 60

  receive_wait_time_seconds = 10

  tags = {
    Environment = "dev"
  }
}

resource "aws_sqs_queue_policy" "s3_output" {
  queue_url = aws_sqs_queue.output.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.output.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_s3_bucket.this.arn}"
        }
      }
    }
  ]
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

resource "aws_s3_bucket_notification" "this" {
  bucket = aws_s3_bucket.this.id

  queue {
    id = "pdfgen-pdf-created"
    queue_arn     = aws_sqs_queue.output.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".pdf"
  }
}