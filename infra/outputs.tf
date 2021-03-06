output "aws_region" {
  description = "Region to which the resources were deployed"
  value = var.aws_region
}

output "aws_profile" {
  description = "AWS profile used to create the resources"
  value = var.aws_profile
}

output "bucket_name" {
  description = "Bucket in which pdfs are generated"
  value = aws_s3_bucket.this.id
}

output "input_queue" {
  description = "SQS queue polled for pdf requests"
  value = aws_sqs_queue.input.id
}

output "output_queue" {
  description = "SQS queue notified by s3 when a pdf is created"
  value = aws_sqs_queue.output.id
}