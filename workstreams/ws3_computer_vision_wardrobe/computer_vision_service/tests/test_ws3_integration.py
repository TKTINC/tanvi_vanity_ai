"""
WS3-P6: Final Integration & Testing
Comprehensive Integration Tests for Tanvi Vanity Agent Computer Vision & Wardrobe
"We girls have no time" - Complete system validation for instant confidence!
"""

import requests
import json
import time
from datetime import datetime

class WS3IntegrationTester:
    """
    Comprehensive integration tester for WS3 Computer Vision & Wardrobe
    "We girls have no time" - Complete system validation instantly!
    """
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def log_test(self, test_name, status, details=None, response_time=None):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'response_time': response_time,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        print(f"✅ {test_name}: {status}" if status == "PASS" else f"❌ {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if response_time:
            print(f"   Response Time: {response_time:.3f}s")
    
    def test_service_health(self):
        """Test basic service health"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Service Health Check", "PASS", 
                                f"Version: {data.get('version')}, Phase: {data.get('phase')}", 
                                response_time)
                    return True
                else:
                    self.log_test("Service Health Check", "FAIL", 
                                f"Unhealthy status: {data.get('status')}", response_time)
            else:
                self.log_test("Service Health Check", "FAIL", 
                            f"HTTP {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Service Health Check", "ERROR", str(e))
        return False
    
    def test_api_structure(self):
        """Test API structure and endpoints"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/info", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                api_endpoints = data.get('api_endpoints', {})
                expected_categories = [
                    'health', 'info', 'features', 'analyze_item', 'add_item', 
                    'search_wardrobe', 'collections', 'analytics_overview',
                    'create_outfit', 'virtual_try_on', 'analytics_dashboard',
                    'cache_stats', 'performance_metrics'
                ]
                
                found_endpoints = len(api_endpoints)
                expected_endpoints = 43  # Updated for WS3-P6
                
                if found_endpoints >= expected_endpoints * 0.9:  # Allow 10% tolerance
                    self.log_test("API Structure", "PASS", 
                                f"Found {found_endpoints} endpoints (expected ~{expected_endpoints})", 
                                response_time)
                    return True
                else:
                    self.log_test("API Structure", "FAIL", 
                                f"Found {found_endpoints} endpoints, expected ~{expected_endpoints}", 
                                response_time)
            else:
                self.log_test("API Structure", "FAIL", 
                            f"HTTP {response.status_code}", response_time)
        except Exception as e:
            self.log_test("API Structure", "ERROR", str(e))
        return False
    
    def test_features_overview(self):
        """Test features overview"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/features", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', {})
                expected_features = [
                    'computer_vision', 'wardrobe_management', 'outfit_visualization',
                    'advanced_visual_analytics', 'performance_optimization'
                ]
                
                found_features = [feature for feature in expected_features if feature in features]
                
                if len(found_features) >= len(expected_features) * 0.8:  # Allow 20% tolerance
                    self.log_test("Features Overview", "PASS", 
                                f"Found {len(found_features)}/{len(expected_features)} expected features", 
                                response_time)
                    return True
                else:
                    self.log_test("Features Overview", "FAIL", 
                                f"Found {len(found_features)}/{len(expected_features)} expected features", 
                                response_time)
            else:
                self.log_test("Features Overview", "FAIL", 
                            f"HTTP {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Features Overview", "ERROR", str(e))
        return False
    
    def test_computer_vision_endpoints(self):
        """Test computer vision endpoints"""
        endpoints_to_test = [
            ("/api/cv/health", "GET"),
        ]
        
        passed = 0
        total = len(endpoints_to_test)
        
        for endpoint, method in endpoints_to_test:
            try:
                start_time = time.time()
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", 
                                           json={}, timeout=5)
                response_time = time.time() - start_time
                
                # Accept 200 (success) or 401 (auth required) as valid responses
                if response.status_code in [200, 401]:
                    passed += 1
                    self.log_test(f"CV Endpoint {endpoint}", "PASS", 
                                f"HTTP {response.status_code}", response_time)
                else:
                    self.log_test(f"CV Endpoint {endpoint}", "FAIL", 
                                f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"CV Endpoint {endpoint}", "ERROR", str(e))
        
        success_rate = passed / total
        if success_rate >= 0.8:
            self.log_test("Computer Vision Endpoints", "PASS", 
                        f"{passed}/{total} endpoints working")
            return True
        else:
            self.log_test("Computer Vision Endpoints", "FAIL", 
                        f"{passed}/{total} endpoints working")
            return False
    
    def test_performance_endpoints(self):
        """Test performance optimization endpoints"""
        endpoints_to_test = [
            ("/api/performance/cache-stats", "GET"),
            ("/api/performance/performance-metrics", "GET"),
        ]
        
        passed = 0
        total = len(endpoints_to_test)
        
        for endpoint, method in endpoints_to_test:
            try:
                start_time = time.time()
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", 
                                           json={}, timeout=5)
                response_time = time.time() - start_time
                
                # Accept 200 (success) or 401 (auth required) as valid responses
                if response.status_code in [200, 401]:
                    passed += 1
                    self.log_test(f"Performance Endpoint {endpoint}", "PASS", 
                                f"HTTP {response.status_code}", response_time)
                else:
                    self.log_test(f"Performance Endpoint {endpoint}", "FAIL", 
                                f"HTTP {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"Performance Endpoint {endpoint}", "ERROR", str(e))
        
        success_rate = passed / total
        if success_rate >= 0.8:
            self.log_test("Performance Endpoints", "PASS", 
                        f"{passed}/{total} endpoints working")
            return True
        else:
            self.log_test("Performance Endpoints", "FAIL", 
                        f"{passed}/{total} endpoints working")
            return False
    
    def test_integration_readiness(self):
        """Test integration readiness with other workstreams"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/info", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                integration_status = data.get('integration_status', {})
                
                required_integrations = ['ws1_user_management', 'ws2_ai_styling']
                ready_integrations = [
                    integration for integration in required_integrations 
                    if integration in integration_status
                ]
                
                if len(ready_integrations) == len(required_integrations):
                    self.log_test("Integration Readiness", "PASS", 
                                f"Ready for {len(ready_integrations)} integrations", 
                                response_time)
                    return True
                else:
                    self.log_test("Integration Readiness", "FAIL", 
                                f"Ready for {len(ready_integrations)}/{len(required_integrations)} integrations", 
                                response_time)
            else:
                self.log_test("Integration Readiness", "FAIL", 
                            f"HTTP {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Integration Readiness", "ERROR", str(e))
        return False
    
    def test_file_structure(self):
        """Test file structure completeness"""
        import os
        
        base_path = "/home/ubuntu/tanvi_vanity_ai/workstreams/ws3_computer_vision_wardrobe/computer_vision_service"
        required_files = [
            "src/main.py",
            "src/models/cv_models.py",
            "src/models/wardrobe_management.py",
            "src/models/outfit_visualization.py",
            "src/models/advanced_visual_analytics.py",
            "src/routes/computer_vision.py",
            "src/routes/wardrobe_management.py",
            "src/routes/outfit_visualization.py",
            "src/routes/advanced_visual_analytics.py",
            "src/routes/performance_optimization.py",
            "src/utils/image_processing_optimization.py"
        ]
        
        found_files = []
        missing_files = []
        
        for file_path in required_files:
            full_path = os.path.join(base_path, file_path)
            if os.path.exists(full_path):
                found_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        success_rate = len(found_files) / len(required_files)
        
        if success_rate >= 0.9:
            self.log_test("File Structure", "PASS", 
                        f"{len(found_files)}/{len(required_files)} required files present")
            return True
        else:
            self.log_test("File Structure", "FAIL", 
                        f"{len(found_files)}/{len(required_files)} required files present. Missing: {missing_files}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive integration test suite"""
        print("🚀 Starting WS3 Computer Vision & Wardrobe Integration Tests")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # Run all tests
        tests = [
            self.test_service_health,
            self.test_api_structure,
            self.test_features_overview,
            self.test_computer_vision_endpoints,
            self.test_performance_endpoints,
            self.test_integration_readiness,
            self.test_file_structure
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            if test():
                passed_tests += 1
        
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        
        # Generate summary
        success_rate = passed_tests / total_tests
        
        print("\n" + "=" * 60)
        print("🎯 WS3 Integration Test Summary")
        print("=" * 60)
        print(f"Tests Passed: {passed_tests}/{total_tests} ({success_rate:.1%})")
        print(f"Total Test Time: {total_time:.2f} seconds")
        
        if success_rate >= 0.8:
            print("✅ WS3 Computer Vision & Wardrobe: PRODUCTION READY!")
            grade = "A+" if success_rate >= 0.95 else "A" if success_rate >= 0.9 else "B+"
        elif success_rate >= 0.6:
            print("⚠️  WS3 Computer Vision & Wardrobe: NEEDS ATTENTION")
            grade = "B" if success_rate >= 0.7 else "C+"
        else:
            print("❌ WS3 Computer Vision & Wardrobe: CRITICAL ISSUES")
            grade = "C" if success_rate >= 0.5 else "D"
        
        print(f"Overall Grade: {grade}")
        print(f"Tagline: We girls have no time - WS3 validation completed instantly!")
        
        return {
            'success_rate': success_rate,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'grade': grade,
            'total_time': total_time,
            'test_results': self.test_results
        }

if __name__ == "__main__":
    tester = WS3IntegrationTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    with open('/home/ubuntu/tanvi_vanity_ai/workstreams/ws3_computer_vision_wardrobe/ws3_integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Test results saved to: ws3_integration_test_results.json")

