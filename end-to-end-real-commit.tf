# Sample Terraform file with security issues for testing
resource "aws_s3_bucket" "example" {
  bucket = "my-test-bucket"
  
  # Issue: Public read access - security vulnerability
  acl = "public-read"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  
  # Issue: No security group specified
  # Issue: No key pair for SSH access
  
  tags = {
    Name = "HelloWorld"
  }
}

# Issue: Security group allows all traffic
resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Issue: RDS instance without encryption
resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = "mydb"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"  # Issue: Hardcoded password
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}