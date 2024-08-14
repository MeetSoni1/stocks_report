**Description:** Automatic Stocks report generation with lastest Stock Market data every week by building simple ETL pipeline on AWS.

---

<h1><center>AWS ETL Architecture<center></h1>

![AWS Architecture](architecture/architecture.gif)

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
