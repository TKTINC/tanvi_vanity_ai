# AWS Deployment Guide - Tanvi Vanity AI
## Complete Step-by-Step Cloud Deployment

🌩️ **Complete AWS deployment guide for Tanvi Vanity AI with maximum automation and cost optimization**

---

## 📋 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [AWS Account Setup](#aws-account-setup)
3. [One-Click Infrastructure Deployment](#one-click-infrastructure-deployment)
4. [Application Deployment](#application-deployment)
5. [Domain and SSL Setup](#domain-and-ssl-setup)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Cost Optimization](#cost-optimization)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 **Prerequisites**

### **Required Tools**
```bash
# 1. AWS CLI (v2.x)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Terraform (v1.0+)
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# 3. Docker
sudo apt-get update
sudo apt-get install docker.io
sudo usermod -aG docker $USER

# 4. jq (for JSON processing)
sudo apt-get install jq
```

### **AWS Account Requirements**
- **AWS Account** with billing enabled
- **IAM User** with programmatic access
- **Required Permissions**:
  - EC2 Full Access
  - ECS Full Access
  - RDS Full Access
  - ElastiCache Full Access
  - S3 Full Access
  - IAM Full Access
  - CloudWatch Full Access
  - Route53 Full Access (for domain)

---

## 🔧 **AWS Account Setup**

### **Step 1: Configure AWS Credentials**
```bash
# Configure AWS CLI
aws configure

# Enter your credentials:
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]
# Default region name: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

### **Step 2: Set Environment Variables**
```bash
# Add to ~/.bashrc or ~/.zshrc
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export PROJECT_NAME="tanvi-vanity-ai"
export ENVIRONMENT="unified"  # Single environment for dev/staging/prod

# Reload shell
source ~/.bashrc
```

---

## 🚀 **One-Click Infrastructure Deployment**

### **Step 1: Run AWS Setup Script**
```bash
# Navigate to project directory
cd /path/to/tanvi_vanity_ai

# Run complete AWS setup (this creates everything!)
./bdt-automation/scripts/aws-setup.sh unified us-east-1
```

**What this script does:**
- ✅ Checks all prerequisites
- ✅ Creates S3 bucket for Terraform state
- ✅ Creates DynamoDB table for state locking
- ✅ Generates complete Terraform configuration
- ✅ Creates deployment scripts
- ✅ Sets up monitoring and logging

### **Step 2: Deploy Infrastructure**
```bash
# Navigate to Terraform directory
cd bdt-automation/terraform

# Initialize Terraform
terraform init

# Review the deployment plan
terraform plan

# Deploy infrastructure (takes 10-15 minutes)
terraform apply

# Save outputs for later use
terraform output -json > ../outputs.json
```

### **Infrastructure Created:**
- **VPC** with public/private subnets across 2 AZs
- **Application Load Balancer** with SSL termination
- **ECS Fargate Cluster** for containerized services
- **RDS PostgreSQL** database with encryption
- **ElastiCache Redis** for caching
- **Security Groups** with least-privilege access
- **IAM Roles** for service permissions
- **CloudWatch** logging and monitoring

---

## 📦 **Application Deployment**

### **Step 1: Create Dockerfiles**

**Frontend Dockerfile** (`workstreams/ws6_mobile_app/tanvi_mobile_app/Dockerfile`):
```dockerfile
# Multi-stage build for React PWA
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Backend Dockerfile Template** (for each WS1-WS5):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["python", "src/main.py"]
```

### **Step 2: Build and Push Docker Images**
```bash
# Run the automated build and push script
./bdt-automation/scripts/build-and-push.sh
```

**This script:**
- Creates ECR repositories for each service
- Builds Docker images for all 6 services
- Pushes images to Amazon ECR
- Tags images with latest and commit SHA

### **Step 3: Deploy ECS Services**
```bash
# Create ECS task definitions and services
./bdt-automation/scripts/deploy-ecs.sh
```

### **Step 4: Verify Deployment**
```bash
# Get application URL
terraform output application_url

# Test endpoints
curl $(terraform output -raw application_url)/health
curl $(terraform output -raw application_url)/api/users/health
curl $(terraform output -raw application_url)/api/ai-styling/health
```

---

## 🌐 **Domain and SSL Setup**

### **Step 1: Purchase Domain (Optional)**
```bash
# If you don't have a domain, you can use the ALB DNS name
# For production, purchase a domain through Route53 or external provider
```

### **Step 2: Create SSL Certificate**
```bash
# Request SSL certificate through AWS Certificate Manager
aws acm request-certificate \
    --domain-name tanvivanityai.com \
    --subject-alternative-names "*.tanvivanityai.com" \
    --validation-method DNS \
    --region us-east-1
```

### **Step 3: Update Load Balancer for HTTPS**
```bash
# Add HTTPS listener to Terraform configuration
# This is included in the generated Terraform files
terraform apply
```

---

## 📊 **Monitoring and Logging**

### **CloudWatch Dashboards**
```bash
# Create monitoring dashboard
aws cloudwatch put-dashboard \
    --dashboard-name "TanviVanityAI-${ENVIRONMENT}" \
    --dashboard-body file://bdt-automation/configs/cloudwatch-dashboard.json
```

### **Log Groups Created:**
- `/aws/ecs/tanvi-vanity-ai-frontend`
- `/aws/ecs/tanvi-vanity-ai-ws1`
- `/aws/ecs/tanvi-vanity-ai-ws2`
- `/aws/ecs/tanvi-vanity-ai-ws3`
- `/aws/ecs/tanvi-vanity-ai-ws4`
- `/aws/ecs/tanvi-vanity-ai-ws5`
- `/aws/rds/instance/tanvi-vanity-ai-postgres/postgresql`

### **Alerts Setup**
```bash
# Create CloudWatch alarms
./bdt-automation/scripts/setup-monitoring.sh
```

**Alerts Created:**
- High CPU utilization (>80%)
- High memory utilization (>80%)
- Database connection errors
- Application error rate (>5%)
- Response time >2 seconds

---

## 💰 **Cost Optimization**

### **Current Configuration (Startup-Optimized):**

| Service | Configuration | Monthly Cost |
|---------|---------------|--------------|
| **ECS Fargate** | 6 tasks × 0.25 vCPU × 0.5GB | $50-80 |
| **RDS PostgreSQL** | db.t3.micro, 20GB | $30-50 |
| **ElastiCache Redis** | cache.t3.micro | $15 |
| **Application Load Balancer** | 1 ALB | $20 |
| **Data Transfer** | Moderate usage | $10-20 |
| **CloudWatch** | Logs + Monitoring | $10-15 |
| **Other Services** | S3, Secrets Manager, etc. | $15-25 |
| **Total Estimated** | | **$150-225/month** |

### **Cost Optimization Features:**
- **Fargate Spot** for 70% cost savings on compute
- **Single AZ RDS** (can enable Multi-AZ later)
- **No NAT Gateway** (using NAT instances)
- **Minimal storage** with auto-scaling
- **Reserved capacity** for predictable workloads

### **Scaling Strategy:**
```bash
# Auto-scaling configuration
Min Capacity: 1 task per service
Max Capacity: 10 tasks per service
Target CPU: 70%
Target Memory: 80%
```

---

## 🔍 **Monitoring URLs and Endpoints**

### **Application URLs:**
```bash
# Get URLs from Terraform output
terraform output application_url
terraform output api_base_url

# Example URLs:
# Frontend: http://tanvi-vanity-ai-alb-123456789.us-east-1.elb.amazonaws.com
# API: http://tanvi-vanity-ai-alb-123456789.us-east-1.elb.amazonaws.com/api
```

### **Health Check Endpoints:**
- **Frontend**: `/` (React app)
- **WS1 User Management**: `/api/users/health`
- **WS2 AI Styling**: `/api/ai-styling/health`
- **WS3 Computer Vision**: `/api/computer-vision/health`
- **WS4 Social Integration**: `/api/social/health`
- **WS5 E-commerce**: `/api/ecommerce/health`

### **AWS Console Links:**
- **ECS Cluster**: https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters
- **RDS Database**: https://console.aws.amazon.com/rds/home?region=us-east-1#databases:
- **Load Balancer**: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LoadBalancers:
- **CloudWatch Logs**: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

---

## 🛠️ **Troubleshooting**

### **Common Issues and Solutions**

#### **1. ECS Tasks Not Starting**
```bash
# Check ECS service events
aws ecs describe-services \
    --cluster tanvi-vanity-ai-unified-cluster \
    --services tanvi-vanity-ai-unified-frontend

# Check task logs
aws logs get-log-events \
    --log-group-name /aws/ecs/tanvi-vanity-ai-frontend \
    --log-stream-name [stream-name]
```

#### **2. Database Connection Issues**
```bash
# Check security groups
aws ec2 describe-security-groups \
    --group-names tanvi-vanity-ai-unified-rds-sg

# Test database connectivity from ECS
aws ecs run-task \
    --cluster tanvi-vanity-ai-unified-cluster \
    --task-definition debug-task \
    --overrides '{"containerOverrides":[{"name":"debug","command":["pg_isready","-h","[db-endpoint]","-p","5432"]}]}'
```

#### **3. Load Balancer Health Check Failures**
```bash
# Check target group health
aws elbv2 describe-target-health \
    --target-group-arn [target-group-arn]

# Check application logs
aws logs filter-log-events \
    --log-group-name /aws/ecs/tanvi-vanity-ai-frontend \
    --filter-pattern "ERROR"
```

#### **4. High Costs**
```bash
# Check cost breakdown
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics BlendedCost \
    --group-by Type=DIMENSION,Key=SERVICE

# Optimize costs
./bdt-automation/scripts/cost-optimization.sh
```

### **Emergency Procedures**

#### **Scale Down for Cost Savings**
```bash
# Scale all services to 0 (emergency stop)
./bdt-automation/scripts/emergency-scale-down.sh

# Scale back up
./bdt-automation/scripts/scale-up.sh
```

#### **Database Backup and Restore**
```bash
# Create manual snapshot
aws rds create-db-snapshot \
    --db-instance-identifier tanvi-vanity-ai-unified-postgres \
    --db-snapshot-identifier manual-backup-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier tanvi-vanity-ai-restored \
    --db-snapshot-identifier manual-backup-20240101
```

---

## 🚀 **Deployment Checklist**

### **Pre-Deployment**
- [ ] AWS credentials configured
- [ ] All prerequisites installed
- [ ] Domain purchased (optional)
- [ ] SSL certificate requested
- [ ] Environment variables set

### **Infrastructure Deployment**
- [ ] Run `./bdt-automation/scripts/aws-setup.sh`
- [ ] Review Terraform plan
- [ ] Apply Terraform configuration
- [ ] Verify infrastructure creation

### **Application Deployment**
- [ ] Create Dockerfiles for all services
- [ ] Build and push Docker images
- [ ] Deploy ECS services
- [ ] Configure load balancer routing
- [ ] Set up health checks

### **Post-Deployment**
- [ ] Verify all endpoints are accessible
- [ ] Test PWA installation
- [ ] Configure monitoring and alerts
- [ ] Set up automated backups
- [ ] Document access URLs

### **Production Readiness**
- [ ] SSL certificate installed
- [ ] Domain configured
- [ ] Monitoring dashboards created
- [ ] Backup procedures tested
- [ ] Disaster recovery plan documented

---

## 📞 **Support and Resources**

### **AWS Documentation**
- [ECS Fargate Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)

### **Terraform Resources**
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

### **Cost Management**
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)
- [AWS Trusted Advisor](https://aws.amazon.com/support/trusted-advisor/)

---

## 🎉 **Success Criteria**

### **Deployment Success Indicators:**
- ✅ All ECS services running and healthy
- ✅ Load balancer health checks passing
- ✅ Database connectivity established
- ✅ Frontend PWA accessible and installable
- ✅ All API endpoints responding correctly
- ✅ Monitoring and logging operational
- ✅ SSL certificate installed and working
- ✅ Auto-scaling configured and tested

### **Performance Targets:**
- **Response Time**: <2 seconds for all endpoints
- **Availability**: >99.5% uptime
- **Error Rate**: <1% for all services
- **Database Performance**: <100ms query response time
- **Cost**: <$250/month for unified environment

---

**🌟 This guide provides complete automation for deploying Tanvi Vanity AI to AWS with enterprise-grade reliability at startup-friendly costs!**

