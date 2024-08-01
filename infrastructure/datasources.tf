data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "Y:/projects/finance/aws/myTestFuncTF"
  output_path = "Y:/projects/finance/aws/myTestFuncTF.zip"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}