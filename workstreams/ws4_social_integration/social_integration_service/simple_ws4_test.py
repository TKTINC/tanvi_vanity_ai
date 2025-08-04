#!/usr/bin/env python3
"""
Simple WS4 Validation Script
Tests basic WS4 Social Integration functionality
"""

import os
import sys

def validate_ws4_structure():
    """Validate WS4 file structure"""
    print("🔍 Validating WS4 Structure...")
    
    base_path = "/home/ubuntu/tanvi_vanity_ai/workstreams/ws4_social_integration/social_integration_service"
    
    required_files = [
        "src/main.py",
        "src/models/social_models.py",
        "src/models/content_sharing.py", 
        "src/models/community_features.py",
        "src/models/style_inspiration.py",
        "src/routes/social_foundation.py",
        "src/routes/content_sharing.py",
        "src/routes/community_features.py",
        "src/routes/style_inspiration.py",
        "src/routes/social_performance.py",
        "src/utils/social_performance_optimization.py"
    ]
    
    missing_files = []
    present_files = []
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            present_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ Files Present: {len(present_files)}/{len(required_files)}")
    print(f"❌ Files Missing: {len(missing_files)}")
    
    if missing_files:
        print("Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
    
    return len(missing_files) == 0

def validate_ws4_features():
    """Validate WS4 feature implementation"""
    print("\n🎯 Validating WS4 Features...")
    
    main_file = "/home/ubuntu/tanvi_vanity_ai/workstreams/ws4_social_integration/social_integration_service/src/main.py"
    
    if not os.path.exists(main_file):
        print("❌ Main application file not found")
        return False
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    required_features = [
        'social_foundation_bp',
        'content_sharing_bp', 
        'community_features_bp',
        'style_inspiration_bp',
        'social_performance_bp'
    ]
    
    present_features = []
    missing_features = []
    
    for feature in required_features:
        if feature in content:
            present_features.append(feature)
        else:
            missing_features.append(feature)
    
    print(f"✅ Features Present: {len(present_features)}/{len(required_features)}")
    print(f"❌ Features Missing: {len(missing_features)}")
    
    if missing_features:
        print("Missing features:")
        for feature in missing_features:
            print(f"  - {feature}")
    
    return len(missing_features) == 0

def validate_ws4_models():
    """Validate WS4 database models"""
    print("\n🗄️ Validating WS4 Models...")
    
    models_dir = "/home/ubuntu/tanvi_vanity_ai/workstreams/ws4_social_integration/social_integration_service/src/models"
    
    if not os.path.exists(models_dir):
        print("❌ Models directory not found")
        return False
    
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.py') and f != '__init__.py']
    
    print(f"✅ Model Files: {len(model_files)}")
    
    expected_models = [
        'social_models.py',
        'content_sharing.py',
        'community_features.py', 
        'style_inspiration.py'
    ]
    
    present_models = [f for f in expected_models if f in model_files]
    missing_models = [f for f in expected_models if f not in model_files]
    
    print(f"✅ Expected Models Present: {len(present_models)}/{len(expected_models)}")
    
    if missing_models:
        print("Missing models:")
        for model in missing_models:
            print(f"  - {model}")
    
    return len(missing_models) == 0

def main():
    """Run WS4 validation"""
    print("🎉 WS4: Social Integration - Validation Script")
    print("=" * 50)
    print("'We girls have no time' - Quick validation check!")
    print()
    
    # Run validation tests
    structure_valid = validate_ws4_structure()
    features_valid = validate_ws4_features()
    models_valid = validate_ws4_models()
    
    # Calculate overall success
    total_tests = 3
    passed_tests = sum([structure_valid, features_valid, models_valid])
    success_rate = (passed_tests / total_tests) * 100
    
    print("\n" + "=" * 50)
    print("🎯 WS4 Validation Results")
    print("=" * 50)
    print(f"Structure Validation: {'✅ PASS' if structure_valid else '❌ FAIL'}")
    print(f"Features Validation: {'✅ PASS' if features_valid else '❌ FAIL'}")
    print(f"Models Validation: {'✅ PASS' if models_valid else '❌ FAIL'}")
    print()
    print(f"Overall Success Rate: {success_rate:.0f}%")
    
    if success_rate == 100:
        print("🎉 EXCELLENT! WS4 structure is complete!")
        print("'We girls have no time' - Ready for integration testing!")
    elif success_rate >= 75:
        print("✅ GOOD! WS4 structure is mostly complete.")
    else:
        print("⚠️ NEEDS WORK! WS4 structure has issues.")
    
    print("\n" + "=" * 50)
    print("WS4 Validation Complete!")
    print("=" * 50)
    
    return success_rate >= 75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

