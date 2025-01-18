variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "lambda_runtime" {
  description = "Ambiente de execução"
  default     = "python3.12"
}

variable "lambda_role" {
  description = "ARN da role IAM"
  type        = string
}

variable "lambda_zip_path" {
  description = "Caminho do arquivo do pacote de implantação"
  default     = "../lambda_function.zip"
}

variable "lambda_aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "lambda_aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "cognito_user_pool_id" {
  description = "ID do usuário no Cognito"
  type        = string
}

variable "dlq_arn" {
  description = "O ARN da DLQ para ser usado como Dead Letter Queue"
  type        = string
}