resource "aws_lambda_function" "lambda_notification" {
  function_name    = "fiapx-lambda-notification"
  handler          = "lambda_function.lambda_handler"
  runtime          = var.lambda_runtime
  role             = var.lambda_role
  filename         = var.lambda_zip_path
  source_code_hash = filebase64sha256(var.lambda_zip_path)

  environment {
    variables = {
      REGION_NAME                  = var.aws_region
      LAMBDA_AWS_ACCESS_KEY_ID     = var.lambda_aws_access_key_id
      LAMBDA_AWS_SECRET_ACCESS_KEY = var.lambda_aws_secret_access_key
      COGNITO_USER_POOL_ID         = var.cognito_user_pool_id
    }
  }

  dead_letter_config {
    target_arn = var.dlq_arn
  }
}

resource "aws_lambda_event_source_mapping" "lambda_dlq_trigger" {
  event_source_arn = var.dlq_arn
  function_name    = aws_lambda_function.lambda_notification.arn
  enabled          = true
}
