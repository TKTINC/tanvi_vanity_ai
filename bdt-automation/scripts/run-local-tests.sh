#!/bin/bash

# Tanvi Vanity AI - Local Testing Suite
# BDT-P1: Comprehensive automated testing for local development

set -e

echo "🧪 Tanvi Vanity AI - Local Testing Suite"
echo "========================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test results
print_test_result() {
    local test_name="$1"
    local result="$2"
    local details="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS${NC} $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC} $test_name"
        if [ -n "$details" ]; then
            echo -e "${RED}   Details: $details${NC}"
        fi
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to test HTTP endpoint
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    local response=$(curl -s -w "%{http_code}" -o /dev/null "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected_status" ]; then
        print_test_result "$name" "PASS"
    else
        print_test_result "$name" "FAIL" "Expected $expected_status, got $response"
    fi
}

# Function to test service health
test_service_health() {
    local service_name="$1"
    local health_url="$2"
    
    local response=$(curl -s "$health_url" 2>/dev/null || echo "")
    
    if echo "$response" | grep -q "healthy\|ok\|running"; then
        print_test_result "$service_name Health Check" "PASS"
    else
        print_test_result "$service_name Health Check" "FAIL" "Health endpoint not responding correctly"
    fi
}

# Function to test database connectivity
test_database() {
    local ws_name="$1"
    local ws_path="$2"
    
    if [ -d "$ws_path" ]; then
        cd "$ws_path"
        service_dir=$(find . -name "*_service" -type d | head -1)
        
        if [ -n "$service_dir" ]; then
            cd "$service_dir"
            
            if [ -d "venv" ]; then
                source venv/bin/activate
                
                # Test database connection
                python -c "
try:
    from src.main import app, db
    with app.app_context():
        db.engine.execute('SELECT 1')
    print('DB_CONNECTION_SUCCESS')
except Exception as e:
    print(f'DB_CONNECTION_FAILED: {e}')
" > /tmp/db_test_result 2>&1
                
                if grep -q "DB_CONNECTION_SUCCESS" /tmp/db_test_result; then
                    print_test_result "$ws_name Database Connection" "PASS"
                else
                    local error=$(grep "DB_CONNECTION_FAILED" /tmp/db_test_result | cut -d: -f2-)
                    print_test_result "$ws_name Database Connection" "FAIL" "$error"
                fi
                
                deactivate
            else
                print_test_result "$ws_name Database Connection" "FAIL" "Virtual environment not found"
            fi
            
            cd ../../..
        else
            print_test_result "$ws_name Database Connection" "FAIL" "Service directory not found"
        fi
    else
        print_test_result "$ws_name Database Connection" "FAIL" "Workstream directory not found"
    fi
}

# Function to test API endpoints
test_api_endpoints() {
    local service_name="$1"
    local base_url="$2"
    
    # Test common endpoints
    test_endpoint "$service_name /health" "$base_url/health" "200"
    test_endpoint "$service_name /api/health" "$base_url/api/health" "200"
    
    # Test service-specific endpoints
    case $service_name in
        "WS1")
            test_endpoint "$service_name /api/users/health" "$base_url/api/users/health" "200"
            ;;
        "WS2")
            test_endpoint "$service_name /api/ai-styling/health" "$base_url/api/ai-styling/health" "200"
            ;;
        "WS3")
            test_endpoint "$service_name /api/computer-vision/health" "$base_url/api/computer-vision/health" "200"
            ;;
        "WS4")
            test_endpoint "$service_name /api/social/health" "$base_url/api/social/health" "200"
            ;;
        "WS5")
            test_endpoint "$service_name /api/ecommerce/health" "$base_url/api/ecommerce/health" "200"
            ;;
    esac
}

# Function to test frontend functionality
test_frontend() {
    echo -e "${BLUE}[INFO]${NC} Testing frontend functionality..."
    
    # Test main page
    test_endpoint "Frontend Main Page" "http://localhost:3000" "200"
    
    # Test PWA manifest
    test_endpoint "PWA Manifest" "http://localhost:3000/manifest.json" "200"
    
    # Test service worker
    test_endpoint "Service Worker" "http://localhost:3000/sw.js" "200"
    
    # Test static assets
    test_endpoint "Frontend Assets" "http://localhost:3000/assets" "200"
}

# Function to run unit tests for a workstream
run_unit_tests() {
    local ws_name="$1"
    local ws_path="$2"
    
    if [ -d "$ws_path" ]; then
        cd "$ws_path"
        service_dir=$(find . -name "*_service" -type d | head -1)
        
        if [ -n "$service_dir" ]; then
            cd "$service_dir"
            
            if [ -d "venv" ] && [ -d "tests" ]; then
                source venv/bin/activate
                
                # Install pytest if not already installed
                pip install pytest pytest-flask > /dev/null 2>&1
                
                # Run tests
                if python -m pytest tests/ -v > /tmp/pytest_result 2>&1; then
                    local test_count=$(grep -c "PASSED" /tmp/pytest_result || echo "0")
                    print_test_result "$ws_name Unit Tests ($test_count tests)" "PASS"
                else
                    local failed_count=$(grep -c "FAILED" /tmp/pytest_result || echo "unknown")
                    print_test_result "$ws_name Unit Tests" "FAIL" "$failed_count tests failed"
                fi
                
                deactivate
            else
                print_test_result "$ws_name Unit Tests" "FAIL" "Tests directory or venv not found"
            fi
            
            cd ../../..
        fi
    fi
}

# Function to test integration between services
test_integration() {
    echo -e "${BLUE}[INFO]${NC} Testing service integration..."
    
    # Test WS1 -> WS2 integration (User to AI Styling)
    local user_token=$(curl -s -X POST "http://localhost:5001/api/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"email":"test@example.com","password":"testpass"}' | \
        grep -o '"access_token":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "")
    
    if [ -n "$user_token" ]; then
        local styling_response=$(curl -s -H "Authorization: Bearer $user_token" \
            "http://localhost:5002/api/ai-styling/recommendations" 2>/dev/null || echo "")
        
        if echo "$styling_response" | grep -q "recommendations\|styles"; then
            print_test_result "WS1->WS2 Integration" "PASS"
        else
            print_test_result "WS1->WS2 Integration" "FAIL" "AI styling not responding to authenticated request"
        fi
    else
        print_test_result "WS1->WS2 Integration" "FAIL" "Could not obtain authentication token"
    fi
    
    # Test WS5 -> WS1 integration (E-commerce to User)
    local ecommerce_response=$(curl -s "http://localhost:5005/api/ecommerce/user-verification" 2>/dev/null || echo "")
    if echo "$ecommerce_response" | grep -q "verification\|user"; then
        print_test_result "WS5->WS1 Integration" "PASS"
    else
        print_test_result "WS5->WS1 Integration" "FAIL" "E-commerce user verification not working"
    fi
}

# Function to test performance
test_performance() {
    echo -e "${BLUE}[INFO]${NC} Testing performance..."
    
    # Test response times
    for service in "Frontend:3000" "WS1:5001" "WS2:5002" "WS3:5003" "WS4:5004" "WS5:5005"; do
        local name=$(echo $service | cut -d: -f1)
        local port=$(echo $service | cut -d: -f2)
        
        local response_time=$(curl -s -w "%{time_total}" -o /dev/null "http://localhost:$port/health" 2>/dev/null || echo "999")
        local response_time_ms=$(echo "$response_time * 1000" | bc 2>/dev/null || echo "999")
        
        if (( $(echo "$response_time < 2.0" | bc -l 2>/dev/null || echo "0") )); then
            print_test_result "$name Response Time (${response_time_ms}ms)" "PASS"
        else
            print_test_result "$name Response Time (${response_time_ms}ms)" "FAIL" "Response time > 2 seconds"
        fi
    done
}

# Main testing sequence
echo -e "${BLUE}[INFO]${NC} Starting comprehensive test suite..."
echo ""

# 1. Test service availability
echo -e "${YELLOW}=== Service Availability Tests ===${NC}"
test_service_health "WS1 User Management" "http://localhost:5001/health"
test_service_health "WS2 AI Styling" "http://localhost:5002/health"
test_service_health "WS3 Computer Vision" "http://localhost:5003/health"
test_service_health "WS4 Social Integration" "http://localhost:5004/health"
test_service_health "WS5 E-commerce" "http://localhost:5005/health"
test_service_health "WS6 Frontend" "http://localhost:3000"

echo ""

# 2. Test API endpoints
echo -e "${YELLOW}=== API Endpoint Tests ===${NC}"
test_api_endpoints "WS1" "http://localhost:5001"
test_api_endpoints "WS2" "http://localhost:5002"
test_api_endpoints "WS3" "http://localhost:5003"
test_api_endpoints "WS4" "http://localhost:5004"
test_api_endpoints "WS5" "http://localhost:5005"

echo ""

# 3. Test frontend
echo -e "${YELLOW}=== Frontend Tests ===${NC}"
test_frontend

echo ""

# 4. Test database connectivity
echo -e "${YELLOW}=== Database Connectivity Tests ===${NC}"
test_database "WS1" "workstreams/ws1_user_management"
test_database "WS2" "workstreams/ws2_ai_styling_engine"
test_database "WS3" "workstreams/ws3_computer_vision_wardrobe"
test_database "WS4" "workstreams/ws4_social_integration"
test_database "WS5" "workstreams/ws5_ecommerce_integration"

echo ""

# 5. Run unit tests
echo -e "${YELLOW}=== Unit Tests ===${NC}"
run_unit_tests "WS1" "workstreams/ws1_user_management"
run_unit_tests "WS2" "workstreams/ws2_ai_styling_engine"
run_unit_tests "WS3" "workstreams/ws3_computer_vision_wardrobe"
run_unit_tests "WS4" "workstreams/ws4_social_integration"
run_unit_tests "WS5" "workstreams/ws5_ecommerce_integration"

echo ""

# 6. Test integration
echo -e "${YELLOW}=== Integration Tests ===${NC}"
test_integration

echo ""

# 7. Test performance
echo -e "${YELLOW}=== Performance Tests ===${NC}"
test_performance

echo ""

# Final results
echo -e "${YELLOW}=== Test Results Summary ===${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Local environment is ready.${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED_TESTS tests failed. Please check the issues above.${NC}"
    exit 1
fi

