# aws-hello-world
Simple IaC project

## Architecture
It is a simple static web-page hosted in a private S3 bucket and distributed through CloudFront (CF)).
CloudFront is used to provide HTTPS access to the content (S3 static website allows only HTTP).
[Origin access identity (OAI)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html) is used to secure access from CF to S3

## Deployment

### Resources
* [static-s3/infra.yaml](static-s3/infra.yaml) containes code to create resources required for web-site, such as S3 bucket, CF, etc. For simlicity, site is created with default CF URL to avoid additional charges (such as registration of your domain name).
* [static-s3/web](static-s3/web) is web site content

### How to deploy
CloudFormation template doesn't require any parameters and can be deployed via console or CLI. The output would give you a web-site URL and S3 bucket name. Upload content from web folder to the root of S3 bucket and it is ready to be served (subject to some propogation delays).