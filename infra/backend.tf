terraform {
  backend "s3" {
    bucket = "fiapx-statefile-bucket"
    key    = "lambda-notification/terraform.tfstate"
    region = "us-east-1"
  }
}