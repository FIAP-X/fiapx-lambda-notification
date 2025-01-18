terraform {
  backend "s3" {
    bucket = "fiapx-bucket-statefile"
    key    = "lambda-notification/terraform.tfstate"
    region = "us-east-1"
  }
}