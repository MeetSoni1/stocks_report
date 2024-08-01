# EVENTBRIDGE
# IAM Role
# Policies
# Event bridge scheduler (default)
resource "aws_iam_role" "eventbridge_scheduler_role" {
  name = "tf-eventbridge-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "scheduler.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_scheduler_policy" {
  name = "tf-eventbridge-scheduler-policy"
  role = aws_iam_role.eventbridge_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = aws_lambda_function.tf_local_lambda.arn
      }
    ]
  })
}

resource "aws_scheduler_schedule" "tf_local_eventbidge" {
  name       = "tf-eventbridge-schedule"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 8 ? * 1 *)"

  target {
    arn      = aws_lambda_function.tf_local_lambda.arn
    role_arn = aws_iam_role.eventbridge_scheduler_role.arn

    retry_policy {
              maximum_event_age_in_seconds = 3600
              maximum_retry_attempts       = 3
    }
  }
}


# LAMBDA
# IAM Role
# Policies
# Lambda Basic Excecution(default)
# Parameter Store
# S3 put object

resource "aws_iam_role" "iam_for_lambda" {
  name               = "tf-iam-for-lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "lambda_basic_execution" {
  name = "lambda_basic_execution"
  role = aws_iam_role.iam_for_lambda.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ssm:GetParameter"
        ],
        Resource = "arn:aws:ssm:*:*:parameter/*"
      }
    ]
  })
}

resource "aws_lambda_function" "tf_local_lambda" {
  # If the file is not in the current working directory you will need to include a path.module in the filename.
  filename      = "Y:/projects/finance/aws/myTestFuncTF.zip"
  function_name = "tf_local_lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256 # Defined in datasources.tf file

  runtime = "python3.12"

  # environment {
  #   variables = {
  #     foo = "bar"
  #   }
  # }
}


# PARAMETER STORE

variable "alphaVantageAPI" {
  description = "Alpha Vantage API key"
  type        = string
}
resource "aws_ssm_parameter" "tf_local_parameter_store" {
  name        = "/stocksReport/tf_keyAlphaVantageAPI"
  description = "TF parameter description"
  type        = "SecureString"
  value       = var.alphaVantageAPI

  #   tags = {
  #     environment = "production"
  #   }
}


# S3

resource "aws_s3_bucket" "tf_local_s3" {
  bucket = "tf-bucket-for-trial"

  #   tags = {
  #     Name        = "My bucket"
  #     Environment = "Dev"
  #   }
}
# resource "aws_s3_bucket_object" "object" {
#   bucket = "tf-bucket"
#   key    = "tf-bucket-stocksreport"
# source = "path/to/file"
# }

# SNS
# Access Policy

resource "aws_sns_topic" "tf_local_sns_topic" {
  name = "tf-sns-s3togmail"
}

variable "email" {
  description = "My email address to send SNS notification"
  type        = string
}

resource "aws_sns_topic_subscription" "email_notification" {
  topic_arn = aws_sns_topic.tf_local_sns_topic.arn
  protocol  = "email"
  endpoint  = var.email
}

# Cloudwatch

# output "name" {
# #   To ouput value on the console while terraform apply
# # Ony one entity per output
# # terraform output - command to see only the outputs on the console
# }