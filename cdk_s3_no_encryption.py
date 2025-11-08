#!/usr/bin/env python3
"""
AWS CDK Infrastructure Code - S3 Bucket WITHOUT Encryption
WARNING: This creates an insecure S3 bucket without encryption enabled.
This is for demonstration/testing purposes only and should NOT be used in production.
"""

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy,
    CfnOutput,
    App,
)
from constructs import Construct


class S3BucketNoEncryptionStack(Stack):
    """
    CDK Stack that creates an S3 bucket without encryption enabled.
    
    WARNING: This is intentionally insecure and violates AWS security best practices.
    Use only for testing or demonstration purposes.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket WITHOUT encryption
        # This explicitly disables encryption which is NOT recommended
        bucket = s3.Bucket(
            self,
            "NoEncryptionBucket",
            bucket_name=None,  # Auto-generate bucket name
            encryption=s3.BucketEncryption.UNENCRYPTED,  # Explicitly disable encryption
            versioned=False,  # No versioning
            public_read_access=False,  # Keep it private at least
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            removal_policy=RemovalPolicy.DESTROY,  # Allow deletion
            auto_delete_objects=True,  # Delete objects when stack is deleted
        )

        # Output the bucket name
        CfnOutput(
            self,
            "BucketName",
            value=bucket.bucket_name,
            description="Name of the S3 bucket without encryption",
            export_name="NoEncryptionBucketName",
        )

        # Output the bucket ARN
        CfnOutput(
            self,
            "BucketArn",
            value=bucket.bucket_arn,
            description="ARN of the S3 bucket without encryption",
            export_name="NoEncryptionBucketArn",
        )

        # Warning output
        CfnOutput(
            self,
            "SecurityWarning",
            value="WARNING: This bucket has NO encryption enabled!",
            description="Security warning about unencrypted bucket",
        )


# CDK App
app = App()

S3BucketNoEncryptionStack(
    app,
    "S3BucketNoEncryptionStack",
    description="Creates an S3 bucket without encryption (INSECURE - for testing only)",
)

app.synth()
