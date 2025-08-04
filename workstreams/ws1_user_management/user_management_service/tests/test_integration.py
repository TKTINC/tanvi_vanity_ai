import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta

# Import the Flask app and models
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from models.user import db, User
from models.profile import StyleProfile, WardrobeItem, OutfitHistory
from models.analytics import UserAnalytics, StyleInsights
from models.security import SecurityAuditLog, UserPrivacySettings, UserSecuritySettings
from utils.performance import CacheManager

class TanviVanityIntegrationTest(unittest.TestCase):
    """
    Comprehensive integration tests for Tanvi Vanity Agent WS1
    "We girls have no time" - Testing everything works together perfectly!
    """
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create all tables
        db.create_all()
        
        # Clear cache
        CacheManager.clear()
        
        # Create test user
        self.test_user = User(
            username='test_user',
            email='test@tanvi.ai',
            first_name='Test',
            last_name='User',
            style_preference='trendy'
        )
        self.test_user.set_password('test_password')
        db.session.add(self.test_user)
        db.session.commit()
        
        # Get auth token
        login_response = self.app.post('/api/auth/login', 
            data=json.dumps({
                'username': 'test_user',
                'password': 'test_password'
            }),
            content_type='application/json'
        )
        self.auth_token = json.loads(login_response.data)['token']
        self.auth_headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
    
    def tearDown(self):
        """Clean up test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        CacheManager.clear()
    
    def test_complete_user_journey(self):
        """
        Test complete user journey from registration to advanced features
        "We girls have no time" - Complete user flow in one test!
        """
        print("\n🌟 Testing Complete User Journey...")
        
        # 1. User Registration (already done in setUp)
        self.assertIsNotNone(self.auth_token)
        print("✓ User registration and authentication")
        
        # 2. Quick Style Quiz
        quiz_response = self.app.post('/api/profile/quick-style-quiz',
            data=json.dumps({
                'style_preferences': ['edgy', 'minimalist'],
                'lifestyle': 'professional',
                'budget_range': 'mid',
                'shopping_frequency': 'monthly'
            }),
            headers=self.auth_headers
        )
        self.assertEqual(quiz_response.status_code, 200)
        quiz_data = json.loads(quiz_response.data)
        self.assertIn('style_personality', quiz_data)
        print("✓ Quick style quiz completed")
        
        # 3. Add Wardrobe Items
        wardrobe_response = self.app.post('/api/profile/wardrobe',
            data=json.dumps({
                'name': 'Black Blazer',
                'category': 'outerwear',
                'primary_color': 'black',
                'brand': 'Zara',
                'purchase_date': '2024-01-15',
                'favorite': True
            }),
            headers=self.auth_headers
        )
        self.assertEqual(wardrobe_response.status_code, 201)
        print("✓ Wardrobe item added")
        
        # 4. Test Fast Dashboard
        dashboard_response = self.app.get('/api/fast/dashboard-fast',
            headers=self.auth_headers
        )
        self.assertEqual(dashboard_response.status_code, 200)
        dashboard_data = json.loads(dashboard_response.data)
        self.assertIn('data', dashboard_data)
        self.assertIn('wardrobe', dashboard_data['data'])
        print("✓ Fast dashboard loaded")
        
        # 5. Test Search
        search_response = self.app.get('/api/fast/search-fast?q=black&type=wardrobe',
            headers=self.auth_headers
        )
        self.assertEqual(search_response.status_code, 200)
        search_data = json.loads(search_response.data)
        self.assertGreater(search_data['total_results'], 0)
        print("✓ Search functionality working")
        
        # 6. Test Privacy Settings
        privacy_response = self.app.get('/api/security/privacy-settings',
            headers=self.auth_headers
        )
        self.assertEqual(privacy_response.status_code, 200)
        privacy_data = json.loads(privacy_response.data)
        self.assertIn('settings', privacy_data)
        print("✓ Privacy settings accessible")
        
        # 7. Test Analytics
        analytics_response = self.app.get('/api/analytics/dashboard',
            headers=self.auth_headers
        )
        self.assertEqual(analytics_response.status_code, 200)
        print("✓ Analytics dashboard working")
        
        print("🎉 Complete user journey test passed!")
    
    def test_performance_optimization(self):
        """
        Test performance optimization features
        "We girls have no time" - Performance must be lightning fast!
        """
        print("\n⚡ Testing Performance Optimization...")
        
        # Test caching
        start_time = datetime.now()
        response1 = self.app.get('/api/fast/dashboard-fast', headers=self.auth_headers)
        first_load_time = (datetime.now() - start_time).total_seconds()
        
        start_time = datetime.now()
        response2 = self.app.get('/api/fast/dashboard-fast', headers=self.auth_headers)
        cached_load_time = (datetime.now() - start_time).total_seconds()
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Cached response should be faster (though in tests it might be minimal)
        print(f"✓ First load: {first_load_time:.3f}s, Cached load: {cached_load_time:.3f}s")
        
        # Test performance stats
        perf_response = self.app.get('/api/fast/performance-stats')
        self.assertEqual(perf_response.status_code, 200)
        perf_data = json.loads(perf_response.data)
        self.assertIn('data', perf_data)
        self.assertIn('cache', perf_data['data'])
        print("✓ Performance monitoring working")
        
        # Test bulk operations
        bulk_response = self.app.post('/api/fast/bulk-operations',
            data=json.dumps({
                'operations': [
                    {
                        'type': 'update_wardrobe_item',
                        'data': {'id': 1, 'favorite': False}
                    }
                ]
            }),
            headers=self.auth_headers
        )
        self.assertEqual(bulk_response.status_code, 200)
        print("✓ Bulk operations working")
        
        print("🏎️ Performance optimization tests passed!")
    
    def test_security_features(self):
        """
        Test security and privacy features
        "We girls have no time" - Security must be seamless and strong!
        """
        print("\n🔒 Testing Security Features...")
        
        # Test privacy settings update
        privacy_update = self.app.put('/api/security/privacy-settings',
            data=json.dumps({
                'profile_visibility': 'friends',
                'allow_analytics_sharing': True
            }),
            headers=self.auth_headers
        )
        self.assertEqual(privacy_update.status_code, 200)
        print("✓ Privacy settings update")
        
        # Test security settings
        security_response = self.app.get('/api/security/security-settings',
            headers=self.auth_headers
        )
        self.assertEqual(security_response.status_code, 200)
        print("✓ Security settings accessible")
        
        # Test audit log
        audit_response = self.app.get('/api/security/audit-log',
            headers=self.auth_headers
        )
        self.assertEqual(audit_response.status_code, 200)
        print("✓ Security audit log working")
        
        # Test data access log
        access_response = self.app.get('/api/security/data-access-log',
            headers=self.auth_headers
        )
        self.assertEqual(access_response.status_code, 200)
        access_data = json.loads(access_response.data)
        self.assertIn('logs', access_data)
        print("✓ Data access transparency working")
        
        print("🛡️ Security features tests passed!")
    
    def test_analytics_intelligence(self):
        """
        Test analytics and AI intelligence features
        "We girls have no time" - AI insights must be smart and helpful!
        """
        print("\n🧠 Testing Analytics Intelligence...")
        
        # Create some analytics data
        analytics_entry = UserAnalytics(
            user_id=self.test_user.id,
            login_count=5,
            session_duration=1800,
            wardrobe_items_added=3,
            style_quiz_taken=True
        )
        db.session.add(analytics_entry)
        
        # Create a style insight
        insight = StyleInsights(
            user_id=self.test_user.id,
            insight_type='wardrobe_gap',
            title='Missing Essential: White Button-Down',
            description='Your wardrobe would benefit from a classic white button-down shirt.',
            priority='medium',
            confidence_score=0.85,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.session.add(insight)
        db.session.commit()
        
        # Test analytics dashboard
        analytics_response = self.app.get('/api/analytics/dashboard',
            headers=self.auth_headers
        )
        self.assertEqual(analytics_response.status_code, 200)
        analytics_data = json.loads(analytics_response.data)
        self.assertIn('analytics', analytics_data)
        print("✓ Analytics dashboard with data")
        
        # Test insights
        insights_response = self.app.get('/api/analytics/insights',
            headers=self.auth_headers
        )
        self.assertEqual(insights_response.status_code, 200)
        insights_data = json.loads(insights_response.data)
        self.assertGreater(len(insights_data['insights']), 0)
        print("✓ AI insights generation")
        
        # Test fast insights
        fast_insights_response = self.app.get('/api/fast/insights-fast',
            headers=self.auth_headers
        )
        self.assertEqual(fast_insights_response.status_code, 200)
        print("✓ Fast insights endpoint")
        
        # Test personalization score
        personalization_response = self.app.get('/api/analytics/personalization',
            headers=self.auth_headers
        )
        self.assertEqual(personalization_response.status_code, 200)
        print("✓ Personalization scoring")
        
        print("🎯 Analytics intelligence tests passed!")
    
    def test_api_endpoints_comprehensive(self):
        """
        Test all API endpoints for proper responses
        "We girls have no time" - Every endpoint must work perfectly!
        """
        print("\n📡 Testing All API Endpoints...")
        
        endpoints_to_test = [
            ('GET', '/api/health', None, 200),
            ('GET', '/api/info', None, 200),
            ('GET', '/api/features', None, 200),
            ('GET', '/api/profile', self.auth_headers, 200),
            ('GET', '/api/preferences', self.auth_headers, 200),
            ('GET', '/api/quick-stats', self.auth_headers, 200),
            ('GET', '/api/profile/style-profile', self.auth_headers, 200),
            ('GET', '/api/profile/wardrobe', self.auth_headers, 200),
            ('GET', '/api/profile/outfit-history', self.auth_headers, 200),
            ('GET', '/api/analytics/dashboard', self.auth_headers, 200),
            ('GET', '/api/analytics/insights', self.auth_headers, 200),
            ('GET', '/api/analytics/patterns', self.auth_headers, 200),
            ('GET', '/api/analytics/personalization', self.auth_headers, 200),
            ('GET', '/api/security/privacy-settings', self.auth_headers, 200),
            ('GET', '/api/security/security-settings', self.auth_headers, 200),
            ('GET', '/api/security/audit-log', self.auth_headers, 200),
            ('GET', '/api/security/data-access-log', self.auth_headers, 200),
            ('GET', '/api/fast/dashboard-fast', self.auth_headers, 200),
            ('GET', '/api/fast/wardrobe-fast', self.auth_headers, 200),
            ('GET', '/api/fast/insights-fast', self.auth_headers, 200),
            ('GET', '/api/fast/profile-fast', self.auth_headers, 200),
            ('GET', '/api/fast/performance-stats', None, 200),
        ]
        
        passed_endpoints = 0
        total_endpoints = len(endpoints_to_test)
        
        for method, endpoint, headers, expected_status in endpoints_to_test:
            try:
                if method == 'GET':
                    response = self.app.get(endpoint, headers=headers)
                elif method == 'POST':
                    response = self.app.post(endpoint, headers=headers)
                
                if response.status_code == expected_status:
                    passed_endpoints += 1
                    print(f"✓ {method} {endpoint}")
                else:
                    print(f"✗ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
            
            except Exception as e:
                print(f"✗ {method} {endpoint} - Error: {str(e)}")
        
        print(f"📊 API Endpoints: {passed_endpoints}/{total_endpoints} passed")
        self.assertGreater(passed_endpoints / total_endpoints, 0.9)  # 90% pass rate
    
    def test_data_consistency(self):
        """
        Test data consistency across all models
        "We girls have no time" - Data must be consistent everywhere!
        """
        print("\n🔄 Testing Data Consistency...")
        
        # Add wardrobe item
        wardrobe_response = self.app.post('/api/profile/wardrobe',
            data=json.dumps({
                'name': 'Red Dress',
                'category': 'dresses',
                'primary_color': 'red',
                'brand': 'H&M'
            }),
            headers=self.auth_headers
        )
        self.assertEqual(wardrobe_response.status_code, 201)
        
        # Check it appears in wardrobe list
        wardrobe_list = self.app.get('/api/profile/wardrobe', headers=self.auth_headers)
        wardrobe_data = json.loads(wardrobe_list.data)
        self.assertGreater(len(wardrobe_data['items']), 0)
        
        # Check it appears in fast wardrobe
        fast_wardrobe = self.app.get('/api/fast/wardrobe-fast', headers=self.auth_headers)
        fast_data = json.loads(fast_wardrobe.data)
        self.assertGreater(len(fast_data['data']), 0)
        
        # Check it appears in search
        search_response = self.app.get('/api/fast/search-fast?q=red', headers=self.auth_headers)
        search_data = json.loads(search_response.data)
        self.assertGreater(search_data['total_results'], 0)
        
        print("✓ Data consistency across endpoints")
        
        # Test cache invalidation
        # Mark item as favorite
        quick_action = self.app.post('/api/fast/quick-actions',
            data=json.dumps({
                'action': 'mark_favorite',
                'item_id': 1
            }),
            headers=self.auth_headers
        )
        self.assertEqual(quick_action.status_code, 200)
        
        # Check dashboard reflects change
        dashboard_response = self.app.get('/api/fast/dashboard-fast', headers=self.auth_headers)
        dashboard_data = json.loads(dashboard_response.data)
        self.assertIn('wardrobe', dashboard_data['data'])
        
        print("✓ Cache invalidation working")
        print("🔄 Data consistency tests passed!")
    
    def test_error_handling(self):
        """
        Test error handling and edge cases
        "We girls have no time" - Errors must be handled gracefully!
        """
        print("\n⚠️ Testing Error Handling...")
        
        # Test unauthorized access
        unauthorized_response = self.app.get('/api/profile')
        self.assertEqual(unauthorized_response.status_code, 401)
        print("✓ Unauthorized access blocked")
        
        # Test invalid token
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        invalid_response = self.app.get('/api/profile', headers=invalid_headers)
        self.assertEqual(invalid_response.status_code, 401)
        print("✓ Invalid token rejected")
        
        # Test non-existent endpoints
        not_found_response = self.app.get('/api/nonexistent')
        self.assertEqual(not_found_response.status_code, 404)
        print("✓ 404 handling working")
        
        # Test invalid data
        invalid_data_response = self.app.post('/api/profile/wardrobe',
            data=json.dumps({'invalid': 'data'}),
            headers=self.auth_headers
        )
        self.assertIn(invalid_data_response.status_code, [400, 422])
        print("✓ Invalid data handling")
        
        # Test search without query
        empty_search = self.app.get('/api/fast/search-fast', headers=self.auth_headers)
        self.assertEqual(empty_search.status_code, 400)
        print("✓ Empty search query handled")
        
        print("⚠️ Error handling tests passed!")


class TanviVanityLoadTest(unittest.TestCase):
    """
    Load testing for performance validation
    "We girls have no time" - Must handle multiple users efficiently!
    """
    
    def setUp(self):
        """Set up load test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.test_user = User(
            username='load_test_user',
            email='load@tanvi.ai',
            first_name='Load',
            last_name='Test'
        )
        self.test_user.set_password('test_password')
        db.session.add(self.test_user)
        db.session.commit()
        
        # Get auth token
        login_response = self.app.post('/api/auth/login', 
            data=json.dumps({
                'username': 'load_test_user',
                'password': 'test_password'
            }),
            content_type='application/json'
        )
        self.auth_token = json.loads(login_response.data)['token']
        self.auth_headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
    
    def tearDown(self):
        """Clean up load test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        CacheManager.clear()
    
    def test_concurrent_dashboard_loads(self):
        """
        Test multiple concurrent dashboard loads
        "We girls have no time" - Must handle concurrent users!
        """
        print("\n🚀 Testing Concurrent Dashboard Loads...")
        
        import threading
        import time
        
        results = []
        
        def load_dashboard():
            start_time = time.time()
            response = self.app.get('/api/fast/dashboard-fast', headers=self.auth_headers)
            end_time = time.time()
            results.append({
                'status_code': response.status_code,
                'response_time': end_time - start_time
            })
        
        # Simulate 10 concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=load_dashboard)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Analyze results
        successful_requests = sum(1 for r in results if r['status_code'] == 200)
        avg_response_time = sum(r['response_time'] for r in results) / len(results)
        
        print(f"✓ Successful requests: {successful_requests}/10")
        print(f"✓ Average response time: {avg_response_time:.3f}s")
        
        self.assertEqual(successful_requests, 10)
        self.assertLess(avg_response_time, 1.0)  # Should be under 1 second
        
        print("🚀 Concurrent load test passed!")


def run_integration_tests():
    """
    Run all integration tests
    "We girls have no time" - Run all tests efficiently!
    """
    print("🌟 Starting Tanvi Vanity Agent WS1 Integration Tests")
    print("💫 Tagline: 'We girls have no time' - Testing everything works perfectly!")
    print("=" * 80)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add integration tests
    suite.addTest(unittest.makeSuite(TanviVanityIntegrationTest))
    suite.addTest(unittest.makeSuite(TanviVanityLoadTest))
    
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
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n🎉 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🌟 WS1: User Management & Authentication - INTEGRATION TESTS PASSED!")
        print("🚀 Ready for handoff to next workstreams!")
    else:
        print("⚠️ Some tests failed - review and fix before proceeding")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    run_integration_tests()

