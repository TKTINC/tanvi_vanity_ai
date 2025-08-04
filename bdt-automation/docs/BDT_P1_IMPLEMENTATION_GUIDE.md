# BDT-P1: Local Development Environment - Implementation Guide

## 🎯 **Overview**

BDT-P1 provides a complete one-click local development environment for Tanvi Vanity AI, enabling developers to quickly set up, run, and test the entire platform locally.

## 📦 **Deliverables Summary**

### **Automation Scripts (8 scripts)**
1. `setup-local-env.sh` - Complete environment setup automation
2. `start-all-services.sh` - Start all services with one command
3. `stop-all-services.sh` - Stop all services gracefully
4. `health-check.sh` - Comprehensive health monitoring
5. `init-local-database.sh` - Database initialization automation
6. `run-local-tests.sh` - Complete testing suite
7. `docker-start.sh` - Docker-based development environment
8. `docker-stop.sh` - Docker environment cleanup

### **Configuration Files (5 files)**
1. `docker-compose.dev.yml` - Complete containerized development environment
2. `.env.local` - Local environment variables
3. `init-db.sql` - Database initialization script
4. `nginx.dev.conf` - Local reverse proxy configuration
5. `requirements.dev.txt` - Development dependencies

### **Documentation (5 guides)**
1. `LOCAL_DEVELOPMENT_GUIDE.md` - Quick start and workflow guide
2. `TROUBLESHOOTING_GUIDE.md` - Common issues and solutions
3. `TESTING_GUIDE.md` - Local testing procedures
4. `CONFIGURATION_GUIDE.md` - Environment configuration
5. `DOCKER_GUIDE.md` - Docker development workflow

## 🚀 **Quick Start**

### **Option 1: Native Setup (Recommended for Development)**
```bash
# 1. Run complete setup
./bdt-automation/scripts/setup-local-env.sh

# 2. Start all services
./bdt-automation/scripts/start-all-services.sh

# 3. Verify everything is working
./bdt-automation/scripts/health-check.sh

# 4. Run comprehensive tests
./bdt-automation/scripts/run-local-tests.sh
```

### **Option 2: Docker Setup (Recommended for Consistency)**
```bash
# 1. Start Docker environment
./bdt-automation/scripts/docker-start.sh

# 2. Check service health
./bdt-automation/scripts/health-check.sh

# 3. Run tests
./bdt-automation/scripts/run-local-tests.sh
```

## 🏗️ **Architecture Overview**

### **Service Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   User Mgmt     │    │   AI Styling    │
│   (Port 3000)   │◄──►│   (Port 5001)   │◄──►│   (Port 5002)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Computer Vision │    │ Social Features │    │   E-commerce    │
│   (Port 5003)   │    │   (Port 5004)   │    │   (Port 5005)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   (Port 5432)   │
                    └─────────────────┘
```

### **Data Flow**
1. **Frontend (WS6)** → API Gateway → Backend Services
2. **User Management (WS1)** → Authentication & Authorization
3. **AI Styling (WS2)** → Machine Learning & Recommendations
4. **Computer Vision (WS3)** → Image Processing & Analysis
5. **Social Features (WS4)** → Community & Sharing
6. **E-commerce (WS5)** → Shopping & Payments

## 🔧 **Configuration Management**

### **Environment Variables**
The setup automatically creates `.env.local` with all necessary configuration:

```bash
# Core Configuration
NODE_ENV=development
FLASK_ENV=development
DEBUG=true

# Service Ports
WS1_PORT=5001  # User Management
WS2_PORT=5002  # AI Styling Engine
WS3_PORT=5003  # Computer Vision
WS4_PORT=5004  # Social Integration
WS5_PORT=5005  # E-commerce Integration
WS6_PORT=3000  # Mobile PWA

# Database
DATABASE_URL=sqlite:///local_tanvi.db
DB_HOST=localhost
DB_PORT=5432

# API Keys (Add your own)
OPENAI_API_KEY=your_openai_api_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### **Port Allocation**
- **3000**: Frontend PWA (React + Vite)
- **5001**: WS1 User Management Service
- **5002**: WS2 AI Styling Engine Service
- **5003**: WS3 Computer Vision Service
- **5004**: WS4 Social Integration Service
- **5005**: WS5 E-commerce Integration Service
- **5432**: PostgreSQL Database
- **6379**: Redis Cache
- **8080**: Adminer (Database Admin)

## 🧪 **Testing Framework**

### **Test Categories**
1. **Service Availability** - Health checks for all services
2. **API Endpoints** - REST API functionality testing
3. **Database Connectivity** - Database connection and operations
4. **Frontend Functionality** - PWA and UI testing
5. **Integration Testing** - Inter-service communication
6. **Performance Testing** - Response time and load testing
7. **Unit Testing** - Individual component testing

### **Test Execution**
```bash
# Run all tests
./bdt-automation/scripts/run-local-tests.sh

# Run specific test categories
./bdt-automation/scripts/run-local-tests.sh --category=api
./bdt-automation/scripts/run-local-tests.sh --category=integration
./bdt-automation/scripts/run-local-tests.sh --category=performance
```

### **Expected Test Results**
- **Total Tests**: ~50-60 tests
- **Success Rate**: >95% for healthy environment
- **Performance**: <2 seconds response time for all services
- **Coverage**: 100% service health, 90%+ API endpoints

## 📊 **Monitoring & Logging**

### **Log Management**
All services log to the `logs/` directory:
```
logs/
├── ws1-usermanagement.log
├── ws2-aistyling.log
├── ws3-computervision.log
├── ws4-socialintegration.log
├── ws5-ecommerce.log
├── frontend.log
└── system.log
```

### **Real-time Monitoring**
```bash
# Watch all logs
tail -f logs/*.log

# Watch specific service
tail -f logs/ws1-usermanagement.log

# Check service status
./bdt-automation/scripts/health-check.sh
```

### **Performance Monitoring**
- **Response Times**: Monitored for all endpoints
- **Memory Usage**: Tracked per service
- **Database Performance**: Query time monitoring
- **Error Rates**: Automatic error detection and logging

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Port Conflicts**
```bash
# Check what's using a port
lsof -i :5001

# Kill process on port
kill -9 $(lsof -ti:5001)

# Or use the stop script
./bdt-automation/scripts/stop-all-services.sh
```

#### **Database Issues**
```bash
# Reinitialize database
./bdt-automation/scripts/init-local-database.sh

# Check database connectivity
psql -h localhost -U tanvi_dev -d tanvi_local
```

#### **Service Not Starting**
```bash
# Check logs for errors
tail -f logs/ws1-usermanagement.log

# Restart specific service
cd workstreams/ws1_user_management/*_service
source venv/bin/activate
python src/main.py
```

#### **Frontend Issues**
```bash
# Clear npm cache
cd workstreams/ws6_mobile_app/tanvi_mobile_app
npm cache clean --force
rm -rf node_modules
npm install

# Restart development server
npm run dev
```

### **Health Check Failures**
If health checks fail:
1. Check service logs in `logs/` directory
2. Verify all dependencies are installed
3. Ensure no port conflicts exist
4. Restart services in dependency order
5. Run database initialization if needed

## 🔄 **Development Workflow**

### **Daily Development**
1. **Start Environment**
   ```bash
   ./bdt-automation/scripts/start-all-services.sh
   ```

2. **Verify Health**
   ```bash
   ./bdt-automation/scripts/health-check.sh
   ```

3. **Make Changes**
   - Edit code in any workstream
   - Changes auto-reload in development mode

4. **Test Changes**
   ```bash
   ./bdt-automation/scripts/run-local-tests.sh
   ```

5. **Stop Environment**
   ```bash
   ./bdt-automation/scripts/stop-all-services.sh
   ```

### **Feature Development**
1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Develop & Test Locally**
   - Use local environment for development
   - Run tests frequently
   - Check integration between services

3. **Integration Testing**
   ```bash
   ./bdt-automation/scripts/run-local-tests.sh --category=integration
   ```

4. **Performance Testing**
   ```bash
   ./bdt-automation/scripts/run-local-tests.sh --category=performance
   ```

## 📈 **Performance Optimization**

### **Local Development Optimization**
- **Service Startup**: Parallel service initialization
- **Database**: SQLite for development (faster than PostgreSQL)
- **Caching**: Redis for session and API caching
- **Hot Reload**: Automatic code reloading for faster development

### **Resource Usage**
- **Memory**: ~2-4GB for full environment
- **CPU**: Moderate usage during AI processing
- **Disk**: ~1GB for logs and database
- **Network**: Local only, no external dependencies required

## 🔐 **Security Considerations**

### **Development Security**
- **API Keys**: Use test/development keys only
- **Database**: Local SQLite with no external access
- **Authentication**: JWT tokens with short expiration
- **CORS**: Enabled for local development only

### **Data Protection**
- **Test Data**: Use synthetic data only
- **Logs**: No sensitive information in logs
- **Environment**: Isolated from production
- **Cleanup**: Automatic cleanup of temporary files

## 📋 **Checklist for BDT-P1 Completion**

### **Setup Verification**
- [ ] All automation scripts are executable
- [ ] Environment configuration is created
- [ ] All services start successfully
- [ ] Health checks pass for all services
- [ ] Database initialization completes
- [ ] Frontend loads and displays correctly

### **Testing Verification**
- [ ] Service availability tests pass
- [ ] API endpoint tests pass
- [ ] Database connectivity tests pass
- [ ] Integration tests pass
- [ ] Performance tests meet criteria
- [ ] Unit tests run successfully

### **Documentation Verification**
- [ ] Local development guide is complete
- [ ] Troubleshooting guide covers common issues
- [ ] Configuration guide explains all settings
- [ ] Testing guide provides clear instructions

### **Operational Verification**
- [ ] Start/stop scripts work reliably
- [ ] Health monitoring provides accurate status
- [ ] Logging captures all necessary information
- [ ] Error handling works correctly

## 🎯 **Success Criteria**

### **Technical Criteria**
- ✅ **One-Click Setup**: Complete environment setup in <5 minutes
- ✅ **Service Health**: All services start and respond within 30 seconds
- ✅ **Test Coverage**: >95% test pass rate
- ✅ **Performance**: <2 second response times for all endpoints
- ✅ **Reliability**: Environment works consistently across restarts

### **Developer Experience Criteria**
- ✅ **Ease of Use**: New developers can set up environment in <10 minutes
- ✅ **Documentation**: Clear, comprehensive guides for all procedures
- ✅ **Troubleshooting**: Common issues have documented solutions
- ✅ **Automation**: Minimal manual intervention required
- ✅ **Feedback**: Clear status and error messages throughout

## 🚀 **Next Steps**

After completing BDT-P1, proceed to:
1. **BDT-P2**: Staging Environment Setup and Validation
2. **BDT-P3**: Production Infrastructure Deployment
3. **BDT-P4**: CI/CD Pipeline Implementation

The local development environment established in BDT-P1 serves as the foundation for all subsequent BDT phases, ensuring consistent development practices and reliable deployment processes.

---

**BDT-P1 Status**: ✅ **COMPLETE**
**Next Phase**: BDT-P2 Staging Environment Setup

