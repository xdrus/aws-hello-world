# aws-hello-world

Simple IaC project

## Architecture

It is a simple static web-page hosted in a private S3 bucket and distributed through CloudFront (CF).
CloudFront is used to provide HTTPS access to the content (S3 static website allows only HTTP).
[Origin access identity (OAI)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
is used to secure access from CF to S3

## Deployment

### Resources

* [static-s3/infra.yaml](static-s3/infra.yaml) containes code to create resources required for web-site, such as S3 bucket, CF, etc. For simlicity, site is created with default CF URL to avoid additional charges (such as registration of your domain name).
* [static-s3/web](static-s3/web) is web site content
* [static-s3/cicd/deployment.yaml](static-s3/cicd/deployment.yaml) created a deployment pipeline to deploy web-site changes automatically. **Note**: Deployment infrastructure is not updated automatically yet, you need to re-execute Step 1 and Step 2 below to deploy any changes to this file.
* [tests](tests) contains a simple testing framework that can be used both as deployment validation and health-check. 

### How to deploy

#### Prerequisites

* You need to an AWS account and aws cli configured (or alternatively have acccess to AWS console)
* You need to fork this repository if you want to deploy the project into your account.
* You need to clone this repo/fork in order to run the commands below (or alternatively download required files manually and use AWS console).

#### Step 1: set variables

Override environment variables if you need so (i.e. change email or region):

```bash
AWS_REGION=ap-southeast-2

GWOwner=xdrus
GHRepo=aws-hello-world
EMAIL=`git config --get user.email`

AWS_ACCOUNT=`aws sts get-caller-identity --query "Account" --output text`
BUCKET_NAME="${GHRepo}-${AWS_REGION}-${AWS_ACCOUNT}"
```

#### Step 2: Deploy CI/CD infrastructure

```bash
aws cloudformation deploy \
    --no-fail-on-empty-changeset \
	--parameter-overrides GitHubRepo=$GWOwner/$GHRepo WebSiteBucketName=$BUCKET_NAME NotificationsEmail=$EMAIL \
	--stack-name $GHRepo-deployment-resources \
	--template-file static-s3/cicd/deployment.yaml \
	--tags "Project=$GHRepo" \
    --capabilities CAPABILITY_IAM
```

if you want to get email notifications about deployment status please confirm SNS topic subscription (you will get an email in mailbox specified in the `EMAIL` variable above).

#### Step 3: integration with GitHub

Codepipeline created on the step 2 uses [CodeStar Connections](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html)
for GitHub integration. Connections created through [CloudFormation resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html)
are in Pending state by default and require manual updating in the web console. Please refer to [this guide](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-update.html)
to finish setup and allow CodePipeline to get access to GitHub.

One you have installed AWS application for GitHub and granted access to the target repository you can re-run pipeline:

```bash
PIPELINE=`aws codepipeline list-pipelines --query "pipelines[?contains(@.name, '$BUCKET')].name" --output text`
aws codepipeline start-pipeline-execution --name $PIPELINE
```

If you have confirmed subscription you will get a notification email in case of both failure and succesfull deployment. Alternatively you can check a status of pipeline in AWS web console.

### How to test

Tests are written using pytest library and usable for both deployment validation and for quick health-check of the site.
In case if a more robust monitoring is needed (i.e. constant periodic health-check) it is better to use managed services capabilities
(i.e. [Route53 health checks with failover](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)) 
or specialised services (i.e. uptime.com)

#### Prerequisites

* python 3
* [pipenv](https://pipenv.pypa.io/en/latest/basics/)

To install dependencies and create virtual environment use:

```bash
pipenv install
```

#### Get test URL

```bash
URL=$(aws cloudformation describe-stacks --stack-name website-$BUCKET_NAME-resources \
            --query 'Stacks[0].Outputs[?OutputKey==`WebsiteURL`].OutputValue' --output text)
```

#### Run tests

```bash
pipenv run pytest -vs --url $URL
```
