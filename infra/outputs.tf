output "bucket_name" {
  description = "Bucket in which pdfs are generated"
  value = aws_s3_bucket.this.id
}