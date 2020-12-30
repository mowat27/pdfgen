output "bucket_name" {
  description = "Bucket in which pdfs are generated"
  value = aws_s3_bucket.this.id
}

output "sns_topic_arn" {
  description = "SNS topic notified when an object is created"
  value = aws_sns_topic.this.id
}