"""
AWS SAM Deployment Module
"""
import os
import subprocess
import sys

# General info
environment = os.getenv("AWS_DEPLOYMENT_ENVIRONMENT")
application_name = os.getenv("AWS_DEPLOYMENT_APPLICATION_NAME")
customer_name = os.getenv("CUSTOMER_NAME")
domain_name = os.getenv("DOMAIN_NAME")
acm_certificate_arn = os.getenv("ACM_CERTIFICATE_ARN")

# Deployment account info
deployment_aws_region = os.getenv("AWS_DEPLOYMENT_REGION")
deployment_aws_account_id = os.getenv("AWS_DEPLOYMENT_ACCOUNT_ID")
deployment_aws_stack_name = f"{environment}-{application_name}-" \
    f"resources-{deployment_aws_account_id}"
deployment_aws_sam_s3_bucket_name = f"{environment}-{application_name}-" \
    f"sam-{deployment_aws_account_id}"
deployment_aws_profile = os.getenv("AWS_DEPLOYMENT_PROFILE")
use_container:bool = str(os.getenv("SAM_BUILD_USE_CONTAINER", "false")).lower() == "true"

# Function to check if a variable is defined
def check_variables(env_vars: list):
    """
    Check for required variables
    """
    missing = []
    for var in env_vars:
        if os.getenv(var) is None:
            missing.append(var)
            print(f"Error: Environment Variable [{var}] is not set.")

    if len(missing) > 0:
        sys.exit(1)

# Function to load environment variables from a .env file
def load_env_file(env_file):
    """
    Load an environment file
    """
    if os.path.isfile(env_file):
        print(f"Loading environment variables from {env_file}")
        with open(env_file, encoding="utf-8") as f:
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
def validate_check_variables():
    """
    validate environment vars
    """
    env_vars = [
        "AWS_DEPLOYMENT_ENVIRONMENT",
        "AWS_DEPLOYMENT_REGION",
        "AWS_DEPLOYMENT_ACCOUNT_ID",
        "AWS_DEPLOYMENT_PROFILE",
        "AWS_DEPLOYMENT_APPLICATION_NAME",
        "CUSTOMER_NAME",
        "DOMAIN_NAME",
        "ACM_CERTIFICATE_ARN"
    ]

    check_variables(env_vars)

def create_deployment_bucket():
    """
    Create an s3 deployment bucket
    """
    print("creating sam deployment bucket (if needed)")
    # Create the sam deployment s3 bucket for the pipeline if it doesn't exist
    run_commands = [
        "aws",
        "s3api",
        "create-bucket",
        "--bucket",
        deployment_aws_sam_s3_bucket_name,
        "--region",
        deployment_aws_region
    ]

    if deployment_aws_profile:
        run_commands.append("--profile")
        run_commands.append(deployment_aws_profile)

    result = subprocess.run(
        run_commands,
        stdout=subprocess.PIPE,
        check=False
    )

    output = result.stdout.decode('utf-8')  # Decode bytes to a string
    print(f"Command output: {output}")
    print(f"sam deployment bucket: {result}")

def sam_build():
    """
    Build the SAM template
    """
    # Do a sam build to make sure the latest is built
    print("building sam template")

    run_commands = [
        "sam", "build",
        "--template", "./devops/resources/template.yaml",        
        "--region", deployment_aws_region, 
    ]

    if deployment_aws_profile:
        run_commands.append("--profile")
        run_commands.append(deployment_aws_profile)

    if use_container:
        # we need a conainer to build it so that it gets the correct dependancies
        # not all projects require this but Pillow module in the requirements.txt
        # is platform dependent.  i'm locally building this on a mac, and after deployment
        # it fails in lambda
        run_commands.append("--use-container")

    exit_status = subprocess.run(run_commands, check=False).returncode

    # Check if the exit status indicates an error
    if exit_status != 0:
        print("Error occurred during 'sam build' command")
        sys.exit(1)


def sam_deploy():
    """
    SAM Deploy
    """
    print("deploying sam stack")
    # Issue a sam deploy
    run_commands = [
        "sam", "deploy",
        "--stack-name",  deployment_aws_stack_name,
        "--template-file", "./.aws-sam/build/template.yaml",
        "--capabilities", "CAPABILITY_IAM", "CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND",
        "--region", deployment_aws_region,
        "--no-fail-on-empty-changeset",
        "--no-confirm-changeset",
        "--s3-bucket", deployment_aws_sam_s3_bucket_name,
        "--s3-prefix", f"pipeline/{environment}/{application_name}/" \
            f"{deployment_aws_account_id}/{deployment_aws_region}",        
        "--parameter-overrides",
        f"ParameterKey=AppName,ParameterValue={application_name}",
        f"ParameterKey=Environment,ParameterValue={environment}",
        f"ParameterKey=CustomerName,ParameterValue={customer_name}",
        f"ParameterKey=CdnDomainName,ParameterValue={domain_name}",
        f"ParameterKey=AcmCertificateArn,ParameterValue={acm_certificate_arn}",
    ]

    if deployment_aws_profile:
        # we need a conainer to build it so that it gets the correct dependancies
        run_commands.append("--profile")
        run_commands.append(deployment_aws_profile)

    exit_status = subprocess.run(run_commands, check=False).returncode

    print(f"exit status {exit_status}")
    # Check if the exit status indicates an error
    if exit_status != 0:
        print("Error occurred during 'sam build' command")
    else:
        print("sam deployed successfully")

    return exit_status

if __name__ == "__main__":
    validate_check_variables()
    create_deployment_bucket()
    sam_build()
    code = sam_deploy()

    sys.exit(code)
