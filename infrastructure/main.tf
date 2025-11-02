# Corrected Terraform configuration with security best practices
resource "aws_s3_bucket" "example" {
  bucket = "my-test-bucket"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  key_name      = var.key_pair_name
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tags = {
    Name = "HelloWorld"
  }
}

# Secure security group with restricted access
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Restrict to private networks
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Restrict to private networks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-security-group"
  }
}

# RDS instance with encryption and secure configuration
resource "aws_db_instance" "default" {
  allocated_storage       = 10
  db_name                = "mydb"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  username               = "admin"
  manage_master_user_password = true  # Use AWS managed password
  parameter_group_name   = "default.mysql8.0"
  skip_final_snapshot    = false
  final_snapshot_identifier = "mydb-final-snapshot"
  
  # Security improvements
  storage_encrypted      = true
  backup_retention_period = 7
  backup_window         = "03:00-04:00"
  maintenance_window    = "sun:04:00-sun:05:00"
  
  tags = {
    Name = "secure-database"
  }
}

# Variables for sensitive values
variable "key_pair_name" {
  description = "Name of the EC2 Key Pair"
  type        = string
}