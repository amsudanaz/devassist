#!/usr/bin/env python3
"""
AWS CDK Infrastructure Code - S3 Bucket WITH Server-Side Encryption
This creates an S3 bucket with server-side encryption enabled using Amazon S3-managed encryption keys (SSE-S3).
"""

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy,
    CfnOutput,
    App,
)
from constructs import Construct


class S3BucketWithEncryptionStack(Stack):
    """
    CDK Stack that creates an S3 bucket with server-side encryption enabled.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket WITH server-side encryption
        bucket = s3.Bucket(
            self,
            "EncryptedBucket",
            bucket_name=None,  # Auto-generate bucket name
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable server-side encryption with Amazon S3-managed keys
            versioned=True,  # Enable versioning
            public_read_access=False,  # Keep it private
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            removal_policy=RemovalPolicy.RETAIN,  # Retain bucket on stack deletion
            auto_delete_objects=False,  # Do not delete objects when stack is deleted
        )

        # Output the bucket name
        CfnOutput(
            self,
            "BucketName",
            value=bucket.bucket_name,
            description="Name of the S3 bucket with server-side encryption",
            export_name="EncryptedBucketName",
        )

        # Output the bucket ARN
        CfnOutput(
            self,
            "BucketArn",
            value=bucket.bucket_arn,
            description="ARN of the S3 bucket with server-side encryption",
            export_name="EncryptedBucketArn",
        )


# CDK App
app = App()

S3BucketWithEncryptionStack(
    app,
    "S3BucketWithEncryptionStack",
    description="Creates an S3 bucket with server-side encryption enabled",
)

app.synth()
