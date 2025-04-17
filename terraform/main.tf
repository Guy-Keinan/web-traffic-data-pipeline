provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "web_traffic_bucket" {
  bucket = "web-traffic-bucket-52fqs7r"
  acl    = "private"
}

