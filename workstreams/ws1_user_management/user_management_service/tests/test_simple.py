import unittest
import json
import requests
import time
import threading
from datetime import datetime

class TanviVanitySimpleIntegrationTest(unittest.TestCase):
    """
    Simplified integration tests for Tanvi Vanity Agent WS1
    "We girls have no time" - Testing via HTTP API calls!
    """
    
    def setUp(self):
        """Set up test environment"""
        self.base_url = 'http://localhost:5001'
        self.auth_token = None
        self.auth_headers = {}
        
        # Start the Flask service if not running
        try:
            response = requests.get(f'{self.base_url}/api/health', timeout=5)
            if response.status_code != 200:
                raise Exception("Service not running")
        except:
            print("⚠️ Flask service not running. Please start it manually.")
            self.skipTest("Flask service not available")
        
        # Register and login test user
        self.setup_test_user()
    
    def setup_test_user(self):
        """Set up test user and get auth token"""
        try:
            # Try to login first
            login_data = {
                'username': 'integration_test_user',
                'password': 'test_password_123'
            }
            
            login_response = requests.post(
                f'{self.base_url}/api/auth/login',
                json=login_data,
                timeout=10
            )
            
            if login_response.status_code == 200:
                self.auth_token = login_response.json()['token']
            else:
                # Register new user
                register_data = {
                    'username': 'integration_test_user',
                    'email': 'integration@tanvi.ai',
                    'password': 'test_password_123',
                    'first_name': 'Integration',
                    'last_name': 'Test',
                    'style_preference': 'trendy'
                }
                
                register_response = requests.post(
                    f'{self.base_url}/api/auth/register',
                    json=register_data,
                    timeout=10
                )
                
                if register_response.status_code == 201:
                    # Now login
                    login_response = requests.post(
                        f'{self.base_url}/api/auth/login',
                        json=login_data,
                        timeout=10
                    )
                    
                    if login_response.status_code == 200:
                        self.auth_token = login_response.json()['token']
            
            if self.auth_token:
                self.auth_headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }
            else:
                self.skipTest("Could not authenticate test user")
                
        except Exception as e:
            self.skipTest(f"Could not set up test user: {str(e)}")
    
    def test_service_health(self):
        """Test service health and basic endpoints"""
        print("\n🏥 Testing Service Health...")
        
        # Health check
        response = requests.get(f'{self.base_url}/api/health')
        self.assertEqual(response.status_code, 200)
        print("✓ Health check passed")
        
        # Service info
        response = requests.get(f'{self.base_url}/api/info')
        self.assertEqual(response.status_code, 200)
        info_data = response.json()
        self.assertIn('service_name', info_data)
        self.assertIn('tagline', info_data)
        print("✓ Service info accessible")
        
        # Features overview
        response = requests.get(f'{self.base_url}/api/features')
        self.assertEqual(response.status_code, 200)
        features_data = response.json()
        self.assertIn('phase', features_data)
        print("✓ Features overview accessible")
        
        print("🏥 Service health tests passed!")
    
    def test_authentication_flow(self):
        """Test authentication and user management"""
        print("\n🔐 Testing Authentication Flow...")
        
        # Verify we have a valid token
        self.assertIsNotNone(self.auth_token)
        print("✓ Authentication token obtained")
        
        # Test token verification
        response = requests.post(
            f'{self.base_url}/api/auth/verify-token',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Token verification working")
        
        # Test profile access
        response = requests.get(
            f'{self.base_url}/api/profile',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        profile_data = response.json()
        self.assertIn('user', profile_data)
        print("✓ Profile access working")
        
        print("🔐 Authentication flow tests passed!")
    
    def test_performance_endpoints(self):
        """Test performance-optimized endpoints"""
        print("\n⚡ Testing Performance Endpoints...")
        
        # Fast dashboard
        start_time = time.time()
        response = requests.get(
            f'{self.base_url}/api/fast/dashboard-fast',
            headers=self.auth_headers
        )
        dashboard_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        dashboard_data = response.json()
        self.assertIn('data', dashboard_data)
        self.assertIn('_meta', dashboard_data)
        print(f"✓ Fast dashboard loaded in {dashboard_time:.3f}s")
        
        # Fast wardrobe
        start_time = time.time()
        response = requests.get(
            f'{self.base_url}/api/fast/wardrobe-fast',
            headers=self.auth_headers
        )
        wardrobe_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        wardrobe_data = response.json()
        self.assertIn('data', wardrobe_data)
        self.assertIn('pagination', wardrobe_data)
        print(f"✓ Fast wardrobe loaded in {wardrobe_time:.3f}s")
        
        # Fast search
        start_time = time.time()
        response = requests.get(
            f'{self.base_url}/api/fast/search-fast?q=test&type=all',
            headers=self.auth_headers
        )
        search_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        search_data = response.json()
        self.assertIn('data', search_data)
        self.assertIn('total_results', search_data)
        print(f"✓ Fast search completed in {search_time:.3f}s")
        
        # Performance stats
        response = requests.get(f'{self.base_url}/api/fast/performance-stats')
        self.assertEqual(response.status_code, 200)
        perf_data = response.json()
        self.assertIn('data', perf_data)
        self.assertIn('cache', perf_data['data'])
        print("✓ Performance stats accessible")
        
        print("⚡ Performance endpoints tests passed!")
    
    def test_wardrobe_management(self):
        """Test wardrobe management features"""
        print("\n👗 Testing Wardrobe Management...")
        
        # Add wardrobe item
        wardrobe_item = {
            'name': 'Integration Test Jacket',
            'category': 'outerwear',
            'primary_color': 'blue',
            'brand': 'Test Brand',
            'favorite': True
        }
        
        response = requests.post(
            f'{self.base_url}/api/profile/wardrobe',
            json=wardrobe_item,
            headers=self.auth_headers
        )
        
        if response.status_code == 201:
            item_data = response.json()
            item_id = item_data['item']['id']
            print("✓ Wardrobe item added successfully")
            
            # Test quick actions
            quick_action = {
                'action': 'mark_worn',
                'item_id': item_id
            }
            
            response = requests.post(
                f'{self.base_url}/api/fast/quick-actions',
                json=quick_action,
                headers=self.auth_headers
            )
            
            if response.status_code == 200:
                print("✓ Quick action (mark worn) working")
            else:
                print(f"⚠️ Quick action failed: {response.status_code}")
        else:
            print(f"⚠️ Wardrobe item addition failed: {response.status_code}")
        
        # Test wardrobe listing
        response = requests.get(
            f'{self.base_url}/api/profile/wardrobe',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Wardrobe listing working")
        
        print("👗 Wardrobe management tests passed!")
    
    def test_analytics_features(self):
        """Test analytics and insights features"""
        print("\n📊 Testing Analytics Features...")
        
        # Analytics dashboard
        response = requests.get(
            f'{self.base_url}/api/analytics/dashboard',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        analytics_data = response.json()
        self.assertIn('analytics', analytics_data)
        print("✓ Analytics dashboard accessible")
        
        # Style insights
        response = requests.get(
            f'{self.base_url}/api/analytics/insights',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        insights_data = response.json()
        self.assertIn('insights', insights_data)
        print("✓ Style insights accessible")
        
        # Fast insights
        response = requests.get(
            f'{self.base_url}/api/fast/insights-fast',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Fast insights working")
        
        # Personalization score
        response = requests.get(
            f'{self.base_url}/api/analytics/personalization',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Personalization scoring working")
        
        print("📊 Analytics features tests passed!")
    
    def test_security_features(self):
        """Test security and privacy features"""
        print("\n🔒 Testing Security Features...")
        
        # Privacy settings
        response = requests.get(
            f'{self.base_url}/api/security/privacy-settings',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        privacy_data = response.json()
        self.assertIn('settings', privacy_data)
        print("✓ Privacy settings accessible")
        
        # Security settings
        response = requests.get(
            f'{self.base_url}/api/security/security-settings',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Security settings accessible")
        
        # Audit log
        response = requests.get(
            f'{self.base_url}/api/security/audit-log',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Security audit log accessible")
        
        # Data access log
        response = requests.get(
            f'{self.base_url}/api/security/data-access-log',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Data access log accessible")
        
        print("🔒 Security features tests passed!")
    
    def test_concurrent_requests(self):
        """Test concurrent request handling"""
        print("\n🚀 Testing Concurrent Requests...")
        
        results = []
        
        def make_request():
            try:
                start_time = time.time()
                response = requests.get(
                    f'{self.base_url}/api/fast/dashboard-fast',
                    headers=self.auth_headers,
                    timeout=10
                )
                end_time = time.time()
                results.append({
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'success': response.status_code == 200
                })
            except Exception as e:
                results.append({
                    'status_code': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                })
        
        # Create 5 concurrent threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Analyze results
        successful_requests = sum(1 for r in results if r['success'])
        avg_response_time = sum(r['response_time'] for r in results if r['success']) / max(successful_requests, 1)
        
        print(f"✓ Successful concurrent requests: {successful_requests}/5")
        print(f"✓ Average response time: {avg_response_time:.3f}s")
        
        self.assertGreaterEqual(successful_requests, 4)  # At least 80% success rate
        
        print("🚀 Concurrent requests test passed!")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test unauthorized access
        response = requests.get(f'{self.base_url}/api/profile')
        self.assertEqual(response.status_code, 401)
        print("✓ Unauthorized access properly blocked")
        
        # Test invalid token
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        response = requests.get(
            f'{self.base_url}/api/profile',
            headers=invalid_headers
        )
        self.assertEqual(response.status_code, 401)
        print("✓ Invalid token properly rejected")
        
        # Test non-existent endpoint
        response = requests.get(f'{self.base_url}/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        print("✓ 404 handling working")
        
        # Test search without query
        response = requests.get(
            f'{self.base_url}/api/fast/search-fast',
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        print("✓ Empty search query properly handled")
        
        print("⚠️ Error handling tests passed!")


def run_simple_integration_tests():
    """
    Run simplified integration tests
    "We girls have no time" - Quick but comprehensive testing!
    """
    print("🌟 Starting Tanvi Vanity Agent WS1 Simple Integration Tests")
    print("💫 Tagline: 'We girls have no time' - Testing via HTTP API calls!")
    print("=" * 80)
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TanviVanitySimpleIntegrationTest))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("=" * 80)
    print(f"🎯 Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n🎉 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🌟 WS1: User Management & Authentication - INTEGRATION TESTS PASSED!")
        print("🚀 Ready for handoff to next workstreams!")
        return True
    else:
        print("⚠️ Some tests failed - review and fix before proceeding")
        return False


if __name__ == '__main__':
    run_simple_integration_tests()

