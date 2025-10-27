import os
import sys
import logging
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# --- Configuration & Setup ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("s3_setup.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    # AWS S3 Configuration from .env file
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    AWS_REGION = os.environ['AWS_REGION']
except KeyError as e:
    logging.critical(f"FATAL: Missing required configuration in .env file: {e}")
    sys.exit(1)

def get_s3_client():
    """Initializes and returns a boto3 S3 client."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        # Test credentials
        s3_client.list_buckets()
        logging.info("✅ Successfully created and validated AWS S3 client.")
        return s3_client
    except NoCredentialsError:
        logging.critical("FATAL: AWS credentials not found. Please configure your .env file.")
        sys.exit(1)
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidAccessKeyId':
            logging.critical("FATAL: Invalid AWS Access Key ID. Please check your .env file.")
        elif e.response['Error']['Code'] == 'SignatureDoesNotMatch':
            logging.critical("FATAL: Invalid AWS Secret Access Key. Please check your .env file.")
        else:
            logging.critical(f"FATAL: An unexpected AWS error occurred: {e}")
        sys.exit(1)

def setup_s3_bucket(s3_client, bucket_name, region):
    """Checks for, creates, and configures the S3 bucket."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logging.info(f"Bucket '{bucket_name}' already exists. Enforcing configuration...")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.info(f"Bucket '{bucket_name}' not found. Creating it...")
            try:
                create_kwargs = {'Bucket': bucket_name}
                # For regions other than us-east-1, a LocationConstraint must be specified
                if region != 'us-east-1':
                    create_kwargs['CreateBucketConfiguration'] = {'LocationConstraint': region}
                s3_client.create_bucket(**create_kwargs)
                logging.info(f"✅ Bucket '{bucket_name}' created successfully.")
            except ClientError as create_error:
                logging.critical(f"FATAL: Could not create bucket '{bucket_name}'. Error: {create_error}")
                sys.exit(1)
        else:
            logging.critical(f"FATAL: Error checking for bucket. Error: {e}")
            sys.exit(1)

    # --- Enforce Configuration ---
    # Req1: Object Ownership: ACLs enabled with Object writer ownership
    try:
        s3_client.put_bucket_ownership_controls(
            Bucket=bucket_name,
            OwnershipControls={'Rules': [{'ObjectOwnership': 'ObjectWriter'}]}
        )
        logging.info("  - ✅ Enforced Object Ownership to 'ObjectWriter' (ACLs enabled).")
    except ClientError as e:
        logging.error(f"  - ❌ Could not set Object Ownership. Error: {e}")

    # Req2-5: Public Access Block settings
    try:
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False, # Req 5
                'IgnorePublicAcls': False, # Req 4
                'BlockPublicPolicy': True, # Req 3
                'RestrictPublicBuckets': True # Req 2
            }
        )
        logging.info("  - ✅ Configured Public Access Block settings.")
    except ClientError as e:
        logging.error(f"  - ❌ Could not set Public Access Block settings. Error: {e}")

    # Req6: Lifecycle Rule to delete objects after 1 day
    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                'Rules': [
                    {
                        'ID': 'delete-images-after-1-day',
                        'Filter': {'Prefix': ''}, # Apply to all objects
                        'Status': 'Enabled',
                        'Expiration': {'Days': 1}
                    },
                ]
            }
        )
        logging.info("  - ✅ Set lifecycle rule to expire objects after 1 day.")
    except ClientError as e:
        logging.error(f"  - ❌ Could not set lifecycle configuration. Error: {e}")


if __name__ == "__main__":
    logging.info("--- Starting S3 Bucket Setup ---")
    s3_client = get_s3_client()
    setup_s3_bucket(s3_client, S3_BUCKET_NAME, AWS_REGION)
    logging.info("--- S3 Bucket Setup Finished ---")