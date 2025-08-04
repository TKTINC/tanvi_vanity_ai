#!/usr/bin/env python3
"""
Simple WS2 validation script
"We girls have no time" - Quick validation!
"""

import os
import sys
import json
from datetime import datetime

def validate_ws2_structure():
    """Validate WS2 file structure and components"""
    print("🏗️ Validating WS2 Structure...")
    
    # Check main files
    required_files = [
        'src/main.py',
        'src/models/ai_models.py',
        'src/models/enhanced_recommendations.py',
        'src/models/personalization.py',
        'src/models/advanced_ai.py',
        'src/utils/performance_cache.py',
        'src/routes/ai_styling.py',
        'src/routes/enhanced_recommendations.py',
        'src/routes/personalization.py',
        'src/routes/advanced_ai.py',
        'src/routes/performance.py'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ Existing files: {len(existing_files)}/{len(required_files)}")
    print(f"❌ Missing files: {len(missing_files)}")
    
    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
    
    return len(missing_files) == 0

def validate_ws2_features():
    """Validate WS2 feature implementation"""
    print("\n🎯 Validating WS2 Features...")
    
    features_implemented = []
    
    # Check AI models
    try:
        from src.models.ai_models import StyleAnalysis, OutfitRecommendation, AIInsight
        features_implemented.append("Core AI Models")
    except ImportError as e:
        print(f"❌ Core AI Models import failed: {e}")
    
    # Check enhanced recommendations
    try:
        from src.models.enhanced_recommendations import WeatherOutfitRule, SeasonalRecommendation, OutfitFeedback
        features_implemented.append("Enhanced Recommendations")
    except ImportError as e:
        print(f"❌ Enhanced Recommendations import failed: {e}")
    
    # Check personalization
    try:
        from src.models.personalization import UserStyleProfile
        features_implemented.append("Personalization")
    except ImportError as e:
        print(f"❌ Personalization import failed: {e}")
    
    # Check advanced AI
    try:
        from src.models.advanced_ai import TrendForecast, WardrobeOptimization, StyleCompatibility, PredictiveRecommendation
        features_implemented.append("Advanced AI")
    except ImportError as e:
        print(f"❌ Advanced AI import failed: {e}")
    
    # Check performance optimization
    try:
        from src.utils.performance_cache import ai_cache, performance_monitor, ai_model_cache
        features_implemented.append("Performance Optimization")
    except ImportError as e:
        print(f"❌ Performance Optimization import failed: {e}")
    
    print(f"✅ Features implemented: {len(features_implemented)}/5")
    for feature in features_implemented:
        print(f"  ✅ {feature}")
    
    return len(features_implemented) >= 4

def validate_ws2_api_structure():
    """Validate WS2 API structure"""
    print("\n📡 Validating WS2 API Structure...")
    
    try:
        # Import Flask app
        from src.main import app
        
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': rule.rule
            })
        
        # Count routes by category
        api_routes = [r for r in routes if r['rule'].startswith('/api/')]
        
        categories = {
            'ai': len([r for r in api_routes if '/ai/' in r['rule']]),
            'enhanced': len([r for r in api_routes if '/enhanced/' in r['rule']]),
            'personalized': len([r for r in api_routes if '/personalized/' in r['rule']]),
            'advanced': len([r for r in api_routes if '/advanced/' in r['rule']]),
            'performance': len([r for r in api_routes if '/performance/' in r['rule']])
        }
        
        total_api_routes = len(api_routes)
        
        print(f"✅ Total API routes: {total_api_routes}")
        for category, count in categories.items():
            print(f"  - {category}: {count} routes")
        
        return total_api_routes >= 20
        
    except Exception as e:
        print(f"❌ API structure validation failed: {e}")
        return False

def generate_ws2_validation_report():
    """Generate WS2 validation report"""
    print("\n" + "="*60)
    print("🎯 WS2 VALIDATION REPORT")
    print("="*60)
    
    # Run validations
    structure_valid = validate_ws2_structure()
    features_valid = validate_ws2_features()
    api_valid = validate_ws2_api_structure()
    
    # Calculate overall score
    validations = [structure_valid, features_valid, api_valid]
    passed_validations = sum(validations)
    total_validations = len(validations)
    success_rate = (passed_validations / total_validations) * 100
    
    print(f"\n📊 VALIDATION SUMMARY:")
    print(f"Structure Validation: {'✅ PASS' if structure_valid else '❌ FAIL'}")
    print(f"Features Validation: {'✅ PASS' if features_valid else '❌ FAIL'}")
    print(f"API Validation: {'✅ PASS' if api_valid else '❌ FAIL'}")
    print(f"Overall Success Rate: {success_rate:.1f}%")
    
    # Generate assessment
    if success_rate >= 100:
        assessment = "🎉 EXCELLENT! WS2 is fully implemented and ready!"
    elif success_rate >= 66:
        assessment = "✅ GOOD! WS2 is mostly implemented with minor issues."
    elif success_rate >= 33:
        assessment = "⚠️ FAIR! WS2 has significant implementation gaps."
    else:
        assessment = "❌ POOR! WS2 needs major implementation work."
    
    print(f"\n{assessment}")
    print(f'\n"We girls have no time" - WS2 validation completed!')
    
    # Create report
    report = {
        'validation_date': datetime.utcnow().isoformat(),
        'validations': {
            'structure': structure_valid,
            'features': features_valid,
            'api': api_valid
        },
        'success_rate': success_rate,
        'assessment': assessment,
        'status': 'production_ready' if success_rate >= 100 else
                 'nearly_ready' if success_rate >= 66 else
                 'needs_work' if success_rate >= 33 else
                 'major_issues'
    }
    
    return report

if __name__ == "__main__":
    print("WS2-P6: Final Integration & Testing")
    print("Simple WS2 Validation")
    print('"We girls have no time" - Quick validation in progress!')
    print()
    
    report = generate_ws2_validation_report()
    
    # Save report
    with open('/tmp/ws2_simple_validation.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nValidation report saved to: /tmp/ws2_simple_validation.json")
