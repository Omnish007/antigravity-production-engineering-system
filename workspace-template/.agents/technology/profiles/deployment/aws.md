---
name: AWS
category: deployment
baselineVersion: AWS CLI v2
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: AWS CLI v2
supportedVersions:
- AWS CLI v2
- AWS CDK v2
legacyVersions:
- AWS SDK v2
prohibitedVersions:
- AWS CLI v1
sources:
- https://docs.aws.amazon.com/
- https://docs.aws.amazon.com/cdk/v2/guide/
---
# AWS Deployment Profile

## 1. Scope
Applies to applications and services deployed to Amazon Web Services (ECS, Lambda, App Runner, S3/CloudFront, API Gateway).

## 2. Detection Signals
- Files: `cdk.json`, `serverless.yml`, `samconfig.toml`, `terraform/`, `main.tf`
- Dependencies: `"aws-cdk"`, `"@aws-sdk/*"`, `"boto3"`

## 3. Supported-Version Policy
- Target: AWS SDK v3 for JavaScript/TypeScript, Boto3 for Python, AWS CDK v2.

## 4. Core Architectural Guidance
- **IAM Least Privilege**: Each service, task, or Lambda function must assume a dedicated IAM execution role with only the minimum required permissions. Avoid wildcard (`*`) actions and resources.
- **Infrastructure as Code (IaC)**: Manage all AWS resources via code (AWS CDK, Terraform, or CloudFormation); never manually configure production resources via the AWS Console.
- **Network Isolation**: Deploy databases and private workloads in private VPC subnets with Security Groups allowing traffic only from designated application compute resources.
- **Secrets Management**: Retrieve secrets dynamically from AWS Secrets Manager or SSM Parameter Store at startup rather than storing in plaintext environment variables.

## 5. Security & Performance Guidance
- **Encryption**: Enforce encryption in transit (TLS 1.3) and encryption at rest (AWS KMS with customer-managed keys for sensitive workloads).
- **Observability**: Export structured logs to Amazon CloudWatch Logs with metric filters and configure CloudWatch Alarms for error rates.
- **Cost & Concurrency Controls**: Set reserved concurrency on Lambda functions to prevent downstream database overload and runaway costs.

## 6. Testing Guidance
- Local Testing: Use LocalStack for offline integration testing of S3, DynamoDB, and SQS.
- IaC Validation: Run `cdk synth` or `terraform plan` to validate infrastructure changes before deployment.

## 7. Common Anti-patterns
- Using IAM policies with wildcard permissions (`Action: "*", Resource: "*"`).
- Hardcoding AWS access keys or secret keys in source code or configuration files.
- Placing database instances in public subnets with open `0.0.0.0/0` security group rules.
- Omitting dead-letter queues (DLQ) on asynchronous Lambda and SQS event consumers.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.aws.amazon.com/
- AWS CDK Documentation: https://docs.aws.amazon.com/cdk/v2/guide/
- Local Inspection: Inspect `cdk.json`, `template.yaml`, or `terraform/` directory.
