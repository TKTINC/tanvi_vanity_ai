#!/bin/bash

# Tanvi Vanity AI - AWS Cloud Deployment Setup
# BDT-P2/P3: Complete AWS infrastructure deployment automation
# Usage: ./aws-setup.sh [environment] [region]

set -e

echo "🌩️ Tanvi Vanity AI - AWS Cloud Deployment"
echo "=========================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
ENVIRONMENT=${1:-"unified"}  # unified environment for dev/staging/prod
AWS_REGION=${2:-"us-east-1"}
PROJECT_NAME="tanvi-vanity-ai"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is required but not installed"
        print_status "Install AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi
    print_success "AWS CLI found: $(aws --version)"
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is required but not installed"
        print_status "Install Terraform: https://learn.hashicorp.com/tutorials/terraform/install-cli"
        exit 1
    fi
    print_success "Terraform found: $(terraform --version | head -1)"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed"
        print_status "Install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker found: $(docker --version)"
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured"
        print_status "Configure AWS credentials: aws configure"
        exit 1
    fi
    
    local aws_account=$(aws sts get-caller-identity --query Account --output text)
    local aws_user=$(aws sts get-caller-identity --query Arn --output text)
    print_success "AWS credentials configured for account: $aws_account"
    print_success "AWS user: $aws_user"
}

# Function to create S3 bucket for Terraform state
create_terraform_backend() {
    print_status "Setting up Terraform backend..."
    
    local bucket_name="${PROJECT_NAME}-terraform-state-${AWS_REGION}"
    
    # Create S3 bucket for Terraform state
    if aws s3 ls "s3://$bucket_name" 2>&1 | grep -q 'NoSuchBucket'; then
        print_status "Creating S3 bucket for Terraform state: $bucket_name"
        aws s3 mb "s3://$bucket_name" --region "$AWS_REGION"
        
        # Enable versioning
        aws s3api put-bucket-versioning \
            --bucket "$bucket_name" \
            --versioning-configuration Status=Enabled
        
        # Enable encryption
        aws s3api put-bucket-encryption \
            --bucket "$bucket_name" \
            --server-side-encryption-configuration '{
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256"
                        }
                    }
                ]
            }'
        
        print_success "Terraform state bucket created: $bucket_name"
    else
        print_success "Terraform state bucket already exists: $bucket_name"
    fi
    
    # Create DynamoDB table for state locking
    local table_name="${PROJECT_NAME}-terraform-locks"
    
    if ! aws dynamodb describe-table --table-name "$table_name" &> /dev/null; then
        print_status "Creating DynamoDB table for Terraform locks: $table_name"
        aws dynamodb create-table \
            --table-name "$table_name" \
            --attribute-definitions AttributeName=LockID,AttributeType=S \
            --key-schema AttributeName=LockID,KeyType=HASH \
            --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
            --region "$AWS_REGION"
        
        # Wait for table to be active
        aws dynamodb wait table-exists --table-name "$table_name" --region "$AWS_REGION"
        print_success "DynamoDB table created: $table_name"
    else
        print_success "DynamoDB table already exists: $table_name"
    fi
}

# Function to generate Terraform configuration
generate_terraform_config() {
    print_status "Generating Terraform configuration..."
    
    mkdir -p bdt-automation/terraform
    
    # Main Terraform configuration
    cat > bdt-automation/terraform/main.tf << EOF
# Tanvi Vanity AI - AWS Infrastructure
# BDT-P2/P3: Complete AWS deployment infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "${PROJECT_NAME}-terraform-state-${AWS_REGION}"
    key            = "${ENVIRONMENT}/terraform.tfstate"
    region         = "${AWS_REGION}"
    dynamodb_table = "${PROJECT_NAME}-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "TanviVanityAI"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "TanviTeam"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# Local values
locals {
  name_prefix = "\${var.project_name}-\${var.environment}"
  
  common_tags = {
    Project     = "TanviVanityAI"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
EOF

    # Variables
    cat > bdt-automation/terraform/variables.tf << EOF
# Tanvi Vanity AI - Terraform Variables

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "${AWS_REGION}"
}

variable "environment" {
  description = "Environment name (unified for dev/staging/prod)"
  type        = string
  default     = "${ENVIRONMENT}"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "${PROJECT_NAME}"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "tanvivanityai.com"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

# Database Configuration
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"  # Cost-optimized for startup
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

# ECS Configuration
variable "ecs_task_cpu" {
  description = "CPU units for ECS tasks"
  type        = number
  default     = 256  # 0.25 vCPU
}

variable "ecs_task_memory" {
  description = "Memory for ECS tasks in MB"
  type        = number
  default     = 512  # 0.5 GB
}

variable "ecs_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 1  # Start with 1, auto-scale as needed
}

# Auto Scaling Configuration
variable "min_capacity" {
  description = "Minimum number of ECS tasks"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of ECS tasks"
  type        = number
  default     = 10
}

# Cost Optimization
variable "enable_nat_gateway" {
  description = "Enable NAT Gateway (costs ~\$45/month)"
  type        = bool
  default     = false  # Use NAT instances for cost savings
}

variable "enable_multi_az" {
  description = "Enable Multi-AZ for RDS (costs extra)"
  type        = bool
  default     = false  # Single AZ for cost savings
}
EOF

    # VPC and Networking
    cat > bdt-automation/terraform/vpc.tf << EOF
# VPC and Networking Configuration

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-vpc"
  })
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-igw"
  })
}

# Public Subnets
resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-public-subnet-\${count.index + 1}"
    Type = "Public"
  })
}

# Private Subnets
resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-private-subnet-\${count.index + 1}"
    Type = "Private"
  })
}

# NAT Gateway (cost-optimized)
resource "aws_eip" "nat" {
  count = var.enable_nat_gateway ? 1 : 0
  
  domain = "vpc"
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-nat-eip"
  })
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? 1 : 0
  
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-nat-gateway"
  })
  
  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-public-rt"
  })
}

resource "aws_route_table" "private" {
  count = var.enable_nat_gateway ? 1 : 0
  
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[0].id
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-private-rt"
  })
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = var.enable_nat_gateway ? length(aws_subnet.private) : 0
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[0].id
}
EOF

    print_success "Terraform configuration generated"
}

# Function to create ECS and Application Load Balancer configuration
generate_ecs_config() {
    print_status "Generating ECS configuration..."
    
    cat > bdt-automation/terraform/ecs.tf << EOF
# ECS Cluster and Services Configuration

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "\${local.name_prefix}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = local.common_tags
}

# ECS Cluster Capacity Providers
resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name
  
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  
  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = "FARGATE_SPOT"  # Cost optimization
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "\${local.name_prefix}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = false  # Allow deletion for dev environment
  
  tags = local.common_tags
}

# ALB Target Groups for each service
resource "aws_lb_target_group" "frontend" {
  name     = "\${local.name_prefix}-frontend-tg"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "ws1" {
  name     = "\${local.name_prefix}-ws1-tg"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "ws2" {
  name     = "\${local.name_prefix}-ws2-tg"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "ws3" {
  name     = "\${local.name_prefix}-ws3-tg"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "ws4" {
  name     = "\${local.name_prefix}-ws4-tg"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

resource "aws_lb_target_group" "ws5" {
  name     = "\${local.name_prefix}-ws5-tg"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = local.common_tags
}

# ALB Listeners
resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

# ALB Listener Rules for API routing
resource "aws_lb_listener_rule" "ws1" {
  listener_arn = aws_lb_listener.main.arn
  priority     = 100
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ws1.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/users/*", "/api/auth/*"]
    }
  }
}

resource "aws_lb_listener_rule" "ws2" {
  listener_arn = aws_lb_listener.main.arn
  priority     = 200
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ws2.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/ai-styling/*", "/api/recommendations/*"]
    }
  }
}

resource "aws_lb_listener_rule" "ws3" {
  listener_arn = aws_lb_listener.main.arn
  priority     = 300
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ws3.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/computer-vision/*", "/api/wardrobe/*"]
    }
  }
}

resource "aws_lb_listener_rule" "ws4" {
  listener_arn = aws_lb_listener.main.arn
  priority     = 400
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ws4.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/social/*", "/api/community/*"]
    }
  }
}

resource "aws_lb_listener_rule" "ws5" {
  listener_arn = aws_lb_listener.main.arn
  priority     = 500
  
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ws5.arn
  }
  
  condition {
    path_pattern {
      values = ["/api/ecommerce/*", "/api/payments/*"]
    }
  }
}
EOF

    print_success "ECS configuration generated"
}

# Function to create RDS and security groups
generate_database_config() {
    print_status "Generating database configuration..."
    
    cat > bdt-automation/terraform/database.tf << EOF
# Database Configuration

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "\${local.name_prefix}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-db-subnet-group"
  })
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier = "\${local.name_prefix}-postgres"
  
  # Engine configuration
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  # Storage configuration
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  # Database configuration
  db_name  = "tanvi_db"
  username = "tanvi_admin"
  password = random_password.db_password.result
  
  # Network configuration
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  
  # Backup configuration
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # High availability (disabled for cost optimization)
  multi_az = var.enable_multi_az
  
  # Monitoring
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring.arn
  
  # Performance Insights
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  
  # Deletion protection (disabled for dev environment)
  deletion_protection = false
  skip_final_snapshot = true
  
  tags = local.common_tags
}

# Random password for database
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Store database password in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "\${local.name_prefix}-db-password"
  
  tags = local.common_tags
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = aws_db_instance.main.username
    password = random_password.db_password.result
    endpoint = aws_db_instance.main.endpoint
    port     = aws_db_instance.main.port
    dbname   = aws_db_instance.main.db_name
  })
}

# RDS Monitoring Role
resource "aws_iam_role" "rds_monitoring" {
  name = "\${local.name_prefix}-rds-monitoring-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
  
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# ElastiCache for Redis (for caching)
resource "aws_elasticache_subnet_group" "main" {
  name       = "\${local.name_prefix}-cache-subnet"
  subnet_ids = aws_subnet.private[*].id
  
  tags = local.common_tags
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "\${local.name_prefix}-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"  # Cost-optimized
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]
  
  tags = local.common_tags
}
EOF

    print_success "Database configuration generated"
}

# Function to create security groups
generate_security_groups() {
    print_status "Generating security groups..."
    
    cat > bdt-automation/terraform/security.tf << EOF
# Security Groups Configuration

# ALB Security Group
resource "aws_security_group" "alb" {
  name        = "\${local.name_prefix}-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-alb-sg"
  })
}

# ECS Security Group
resource "aws_security_group" "ecs" {
  name        = "\${local.name_prefix}-ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "HTTP from ALB"
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  ingress {
    description     = "Flask services from ALB"
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-ecs-sg"
  })
}

# RDS Security Group
resource "aws_security_group" "rds" {
  name        = "\${local.name_prefix}-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "PostgreSQL from ECS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-rds-sg"
  })
}

# Redis Security Group
resource "aws_security_group" "redis" {
  name        = "\${local.name_prefix}-redis-sg"
  description = "Security group for Redis cache"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "Redis from ECS"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  
  tags = merge(local.common_tags, {
    Name = "\${local.name_prefix}-redis-sg"
  })
}
EOF

    print_success "Security groups configuration generated"
}

# Function to create outputs
generate_outputs() {
    print_status "Generating outputs..."
    
    cat > bdt-automation/terraform/outputs.tf << EOF
# Terraform Outputs

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the load balancer"
  value       = aws_lb.main.zone_id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "database_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "redis_port" {
  description = "Redis cluster port"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].port
}

output "secrets_manager_secret_name" {
  description = "Name of the Secrets Manager secret containing database credentials"
  value       = aws_secretsmanager_secret.db_password.name
}

# Application URLs
output "application_url" {
  description = "URL to access the application"
  value       = "http://\${aws_lb.main.dns_name}"
}

output "api_base_url" {
  description = "Base URL for API endpoints"
  value       = "http://\${aws_lb.main.dns_name}/api"
}

# Cost estimation
output "estimated_monthly_cost" {
  description = "Estimated monthly cost in USD"
  value = "Estimated cost: \$150-250/month (ECS Fargate: \$50-80, RDS: \$30-50, ALB: \$20, ElastiCache: \$15, Data Transfer: \$10-20, Other: \$25-75)"
}
EOF

    print_success "Outputs configuration generated"
}

# Function to deploy infrastructure
deploy_infrastructure() {
    print_status "Deploying AWS infrastructure..."
    
    cd bdt-automation/terraform
    
    # Initialize Terraform
    print_status "Initializing Terraform..."
    terraform init
    
    # Plan deployment
    print_status "Planning Terraform deployment..."
    terraform plan -out=tfplan
    
    # Apply deployment
    print_status "Applying Terraform deployment..."
    terraform apply tfplan
    
    # Save outputs
    terraform output -json > ../outputs.json
    
    cd ../..
    
    print_success "Infrastructure deployment completed"
}

# Function to create deployment scripts
create_deployment_scripts() {
    print_status "Creating deployment scripts..."
    
    # Docker build and push script
    cat > bdt-automation/scripts/build-and-push.sh << 'EOF'
#!/bin/bash

# Build and push Docker images to ECR
set -e

AWS_REGION=${AWS_REGION:-"us-east-1"}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
PROJECT_NAME="tanvi-vanity-ai"

echo "🐳 Building and pushing Docker images..."

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Function to build and push image
build_and_push() {
    local service_name=$1
    local dockerfile_path=$2
    local context_path=$3
    
    echo "Building $service_name..."
    
    # Create ECR repository if it doesn't exist
    aws ecr describe-repositories --repository-names "${PROJECT_NAME}-${service_name}" --region $AWS_REGION 2>/dev/null || \
    aws ecr create-repository --repository-name "${PROJECT_NAME}-${service_name}" --region $AWS_REGION
    
    # Build and tag image
    docker build -t "${PROJECT_NAME}-${service_name}" -f "$dockerfile_path" "$context_path"
    docker tag "${PROJECT_NAME}-${service_name}:latest" "${ECR_REGISTRY}/${PROJECT_NAME}-${service_name}:latest"
    
    # Push image
    docker push "${ECR_REGISTRY}/${PROJECT_NAME}-${service_name}:latest"
    
    echo "✅ $service_name image pushed successfully"
}

# Build all services
build_and_push "frontend" "workstreams/ws6_mobile_app/tanvi_mobile_app/Dockerfile" "workstreams/ws6_mobile_app/tanvi_mobile_app"
build_and_push "ws1" "workstreams/ws1_user_management/Dockerfile" "workstreams/ws1_user_management"
build_and_push "ws2" "workstreams/ws2_ai_styling_engine/Dockerfile" "workstreams/ws2_ai_styling_engine"
build_and_push "ws3" "workstreams/ws3_computer_vision_wardrobe/Dockerfile" "workstreams/ws3_computer_vision_wardrobe"
build_and_push "ws4" "workstreams/ws4_social_integration/Dockerfile" "workstreams/ws4_social_integration"
build_and_push "ws5" "workstreams/ws5_ecommerce_integration/Dockerfile" "workstreams/ws5_ecommerce_integration"

echo "🎉 All images built and pushed successfully!"
EOF

    chmod +x bdt-automation/scripts/build-and-push.sh
    
    print_success "Deployment scripts created"
}

# Main execution
main() {
    print_status "Starting AWS deployment setup for Tanvi Vanity AI..."
    print_status "Environment: $ENVIRONMENT"
    print_status "Region: $AWS_REGION"
    print_status "Stack: $STACK_NAME"
    
    # Execute setup steps
    check_prerequisites
    create_terraform_backend
    generate_terraform_config
    generate_ecs_config
    generate_database_config
    generate_security_groups
    generate_outputs
    create_deployment_scripts
    
    print_success "AWS setup completed successfully!"
    print_status ""
    print_status "Next steps:"
    print_status "1. Review Terraform configuration in bdt-automation/terraform/"
    print_status "2. Deploy infrastructure: cd bdt-automation/terraform && terraform apply"
    print_status "3. Build and push Docker images: ./bdt-automation/scripts/build-and-push.sh"
    print_status "4. Deploy ECS services: ./bdt-automation/scripts/deploy-ecs.sh"
    print_status ""
    print_status "Estimated monthly cost: \$150-250 (startup-optimized)"
}

# Run main function
main "$@"

