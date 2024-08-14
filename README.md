<center># AWS ETL Architecture for Automated Stocks Report</center>

![AWS Architecture](architecture/architecture.gif)

---
**Description:** Automatic Stocks report generation every week by building simple ETL pipeline on AWS.
---

* **Data Collection:** Asynchronous REST API calls
* **Scripting Language:** Python
* **Infrastructure provisioning and maintenance:** Terraform

___

🌐 AWS Stack:

* **Parameter Store:** Secure storage for API keys with KMS encryption
* **EventBridge:** Scheduling CRON jobs to trigger Lambda function
* **Lambda:** Run Python Script for Data Extraction and Transformation
* **S3:** Storing the generated reports
* **SNS:** Email notifications for new reports
* **CloudWatch:** Logging and monitoring
* **IAM:** Managing roles and policies
