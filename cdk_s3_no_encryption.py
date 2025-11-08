#!/usr/bin/env python3

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_kms as kms,
    RemovalPolicy,
    CfnOutput,
    App,
)
from constructs import Construct


class S3BucketEncryptedStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a KMS key for S3 bucket encryption
        kms_key = kms.Key(
            self,
            "BucketKey",
            description="KMS key for S3 bucket encryption",
            removal_policy=RemovalPolicy.RETAIN,
        )

        # Create S3 bucket WITH server-side encryption using the KMS key
        bucket = s3.Bucket(
            self,
            "EncryptedBucket",
            bucket_name=None,  # Auto-generate bucket name
            encryption=s3.BucketEncryption.KMS,  # Enable KMS encryption
            encryption_key=kms_key.key_arn,  # Specify the KMS key
            versioned=True,  # Enable versioning
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            removal_policy=RemovalPolicy.RETAIN,  # Retain bucket on stack deletion
            auto_delete_objects=False,  # Don't delete objects on stack deletion
        )

        # Output the bucket name
        CfnOutput(
            self,
            "BucketName",
            value=bucket.bucket_name,
            description="Name of the encrypted S3 bucket",
            export_name="EncryptedBucketName",
        )

        # Output the bucket ARN
        CfnOutput(
            self,
            "BucketArn",
            value=bucket.bucket_arn,
            description="ARN of the encrypted S3 bucket",
            export_name="EncryptedBucketArn",
        )


# CDK App
app = App()

S3BucketEncryptedStack(
    app,
    "S3BucketEncryptedStack",
    description="Creates an S3 bucket with server-side encryption using KMS key",
)

app.synth()
