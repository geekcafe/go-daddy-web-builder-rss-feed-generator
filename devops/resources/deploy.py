import os
import subprocess
import sys

# Function to check if a variable is defined
def check_variables(vars: list):
    missing = []
    for var in vars:
        if os.getenv(var) is None:
            missing.append(var)
            print(f"Error: Environment Variable [{var}] is not set.")
    

    if len(missing) > 0:
        sys.exit(1)

# Function to load environment variables from a .env file
def load_env_file(env_file):
    if os.path.isfile(env_file):
        print(f"Loading environment variables from {env_file}")
        with open(env_file) as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split("=")
                os.environ[key] = value
    else:
        print(f"Error: {env_file} not found.")
        sys.exit(1)

# If a .env file is provided as a parameter, attempt to load it
if len(sys.argv) == 2:
    load_env_file(sys.argv[1])

# Check and load environment variables
check_variables(["AWS_DEPLOYMENT_ENVIRONMENT",
                 "AWS_DEPLOYMENT_REGION",
                 "AWS_DEPLOYMENT_ACCOUNT_ID",
                 "AWS_DEPLOYMENT_PROFILE",
                 "AWS_DEPLOYMENT_APPLICATION_NAME",
                 "CUSTOMER_NAME",
                 "DOMAIN_NAME",
                 "ACM_CERTIFICATE_ARN"
                 ])

# General info
environment = os.getenv("AWS_DEPLOYMENT_ENVIRONMENT")
application_name = os.getenv("AWS_DEPLOYMENT_APPLICATION_NAME")
customer_name = os.getenv("CUSTOMER_NAME")
domain_name = os.getenv("DOMAIN_NAME")
acm_certificate_arn = os.getenv("ACM_CERTIFICATE_ARN")

# Deployment account info
deployment_aws_region = os.getenv("AWS_DEPLOYMENT_REGION")
deployment_aws_account_id = os.getenv("AWS_DEPLOYMENT_ACCOUNT_ID")
deployment_aws_stack_name = f"{environment}-{application_name}-resources-{deployment_aws_account_id}"
deployment_aws_sam_s3_bucket_name = f"{environment}-{application_name}-sam-{deployment_aws_account_id}"
deployment_aws_profile = os.getenv("AWS_DEPLOYMENT_PROFILE")

print("creating sam deployment bucket (if needed)")
# Create the sam deployment s3 bucket for the pipeline if it doesn't exist
result = subprocess.run(
    [
        "aws",
        "s3api",
        "create-bucket",
        "--bucket",
        deployment_aws_sam_s3_bucket_name,
        "--region",
        deployment_aws_region,
        "--profile",
        deployment_aws_profile,
    ],
    stdout=subprocess.PIPE
)

output = result.stdout.decode('utf-8')  # Decode bytes to a string
print(f"Command output: {output}")
print(f"sam deployment bucket: {result}")

# Do a sam build to make sure the latest is built
print("building sam template")

run_commands = [
    "sam", "build",
    "--template", "./devops/resources/template.yaml",
    "--use-container",
    "--region", deployment_aws_region, 
]

local_build = True
if local_build:
    # we need a conainer to build it so that it gets the correct dependancies
    run_commands.append("--use-container")
    run_commands.append("--profile")
    run_commands.append(deployment_aws_profile)
    
exit_status = subprocess.run(
    [
        "sam", "build",
        "--template", "./devops/resources/template.yaml",
        "--use-container",
        "--region", deployment_aws_region, 
        "--profile", deployment_aws_profile
    ]
).returncode

# Check if the exit status indicates an error
if exit_status != 0:
    print("Error occurred during 'sam build' command")
    sys.exit(1)

print("deploying sam stack")
# Issue a sam deploy
exit_status = subprocess.run(
    [
        "sam",
        "deploy",
        "--stack-name",
        deployment_aws_stack_name,
        "--template-file",
        "./.aws-sam/build/template.yaml",
        "--capabilities",
        "CAPABILITY_IAM",
        "CAPABILITY_NAMED_IAM",
        "CAPABILITY_AUTO_EXPAND",
        "--region",
        deployment_aws_region,
        "--no-fail-on-empty-changeset",
        "--no-confirm-changeset",
        "--s3-bucket",
        deployment_aws_sam_s3_bucket_name,
        "--s3-prefix",
        f"pipeline/{environment}/{application_name}/{deployment_aws_account_id}/{deployment_aws_region}",
        "--profile",
        deployment_aws_profile,
        "--parameter-overrides",
        f"ParameterKey=AppName,ParameterValue={application_name}",
        f"ParameterKey=Environment,ParameterValue={environment}",
        f"ParameterKey=CustomerName,ParameterValue={customer_name}",
        f"ParameterKey=CdnDomainName,ParameterValue={domain_name}",
        f"ParameterKey=AcmCertificateArn,ParameterValue={acm_certificate_arn}",
    ]
).returncode

print(f"exit status {exit_status}")
# Check if the exit status indicates an error
if exit_status != 0:
    print("Error occurred during 'sam build' command")
else:
    print("sam deployed successfully")
