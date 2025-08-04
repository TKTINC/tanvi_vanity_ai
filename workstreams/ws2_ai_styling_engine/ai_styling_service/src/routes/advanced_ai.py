from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import requests
import json
from src.models.advanced_ai import (
    TrendForecast, WardrobeOptimization, StyleCompatibility, 
    PredictiveRecommendation, AdvancedAIEngine, db
)

advanced_ai_bp = Blueprint('advanced_ai', __name__)

# WS1 User Management Service Integration
WS1_BASE_URL = 'http://localhost:5001'  # WS1 service endpoint

def get_user_data(user_id, auth_token):
    """Fetch user data from WS1 User Management Service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Get user profile
        profile_response = requests.get(f'{WS1_BASE_URL}/api/profile', headers=headers, timeout=5)
        if profile_response.status_code != 200:
            return None
        
        profile_data = profile_response.json()
        
        # Get wardrobe data
        wardrobe_response = requests.get(f'{WS1_BASE_URL}/api/profile/wardrobe', headers=headers, timeout=5)
        wardrobe_data = []
        if wardrobe_response.status_code == 200:
            wardrobe_data = wardrobe_response.json().get('items', [])
        
        return {
            'profile': profile_data,
            'wardrobe': wardrobe_data
        }
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None

def verify_auth_token(auth_token):
    """Verify authentication token with WS1 service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.post(f'{WS1_BASE_URL}/api/auth/verify-token', headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

@advanced_ai_bp.route('/trend-forecast', methods=['GET'])
def get_trend_forecast():
    """
    Get AI-powered trend forecasts
    "We girls have no time" - Know trends before they happen!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get query parameters
        trend_type = request.args.get('type', 'all')  # all, current, emerging, predicted
        limit = request.args.get('limit', 10, type=int)
        
        # Generate fresh trend forecasts
        fresh_forecasts = AdvancedAIEngine.generate_trend_forecast()
        
        # Get trends based on type
        if trend_type == 'current':
            trends = TrendForecast.get_current_trends(limit)
        elif trend_type == 'emerging':
            trends = TrendForecast.get_emerging_trends(limit)
        elif trend_type == 'predicted':
            trends = TrendForecast.get_predicted_trends(limit)
        else:
            # Get all trends, sorted by confidence and strength
            trends = TrendForecast.query.order_by(
                TrendForecast.confidence_score.desc(),
                TrendForecast.trend_strength.desc()
            ).limit(limit).all()
        
        # Convert to dict format
        trend_data = [trend.to_dict() for trend in trends]
        
        # Add trend insights
        insights = {
            'total_trends_tracked': TrendForecast.query.count(),
            'trending_now': TrendForecast.query.filter_by(status='trending').count(),
            'emerging_trends': TrendForecast.query.filter_by(status='emerging').count(),
            'predicted_trends': TrendForecast.query.filter_by(status='predicted').count(),
            'top_categories': ['style', 'color', 'pattern', 'fabric'],
            'forecast_accuracy': '78%',  # In production, calculate from historical data
            'next_update': (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Trend forecasts retrieved successfully',
            'trends': trend_data,
            'insights': insights,
            'forecast_type': trend_type,
            'total_results': len(trend_data),
            'tagline': 'We girls have no time - Know trends before they happen!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve trend forecasts',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@advanced_ai_bp.route('/wardrobe-optimization', methods=['POST'])
def analyze_wardrobe_optimization():
    """
    Perform comprehensive wardrobe optimization analysis
    "We girls have no time" - Optimize your wardrobe intelligently!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Fetch user wardrobe data from WS1
        user_data = get_user_data(user_id, auth_token)
        if not user_data:
            return jsonify({'error': 'Unable to fetch user data'}), 500
        
        wardrobe_data = user_data.get('wardrobe', [])
        if not wardrobe_data:
            return jsonify({
                'status': 'no_wardrobe',
                'message': 'No wardrobe items found for optimization',
                'recommendation': 'Start by adding basic wardrobe items',
                'tagline': 'We girls have no time - But we need clothes first!'
            }), 400
        
        # Perform optimization analysis
        optimization_result = AdvancedAIEngine.analyze_wardrobe_optimization(user_id, wardrobe_data)
        
        # Generate optimization insights
        insights = {
            'overall_score': (
                optimization_result['versatility_score'] + 
                optimization_result['completeness_score'] + 
                optimization_result['efficiency_score'] + 
                optimization_result['style_coherence_score']
            ) / 4,
            'strongest_area': max([
                ('versatility', optimization_result['versatility_score']),
                ('completeness', optimization_result['completeness_score']),
                ('efficiency', optimization_result['efficiency_score']),
                ('style_coherence', optimization_result['style_coherence_score'])
            ], key=lambda x: x[1])[0],
            'improvement_area': min([
                ('versatility', optimization_result['versatility_score']),
                ('completeness', optimization_result['completeness_score']),
                ('efficiency', optimization_result['efficiency_score']),
                ('style_coherence', optimization_result['style_coherence_score'])
            ], key=lambda x: x[1])[0],
            'optimization_priority': 'high' if optimization_result['completeness_score'] < 0.6 else 'medium' if optimization_result['versatility_score'] < 0.7 else 'low'
        }
        
        # Generate actionable recommendations
        action_plan = {
            'immediate_actions': [],
            'short_term_goals': [],
            'long_term_vision': []
        }
        
        if optimization_result['missing_essentials']:
            action_plan['immediate_actions'].append(f"Add {len(optimization_result['missing_essentials'])} essential items")
        
        if optimization_result['color_gaps']:
            action_plan['short_term_goals'].append(f"Fill {len(optimization_result['color_gaps'])} color gaps")
        
        if optimization_result['versatility_score'] < 0.7:
            action_plan['long_term_vision'].append("Build a more versatile wardrobe foundation")
        
        return jsonify({
            'status': 'success',
            'message': 'Wardrobe optimization analysis completed',
            'optimization': optimization_result,
            'insights': insights,
            'action_plan': action_plan,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Wardrobe optimized intelligently!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Wardrobe optimization analysis failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@advanced_ai_bp.route('/style-compatibility', methods=['POST'])
def analyze_style_compatibility():
    """
    Analyze compatibility between style items
    "We girls have no time" - Perfect style matching every time!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        item1_data = data.get('item1')
        item2_data = data.get('item2')
        
        if not item1_data or not item2_data:
            return jsonify({'error': 'Both item1 and item2 data required'}), 400
        
        # Analyze compatibility
        compatibility_result = AdvancedAIEngine.analyze_style_compatibility(item1_data, item2_data)
        
        # Generate compatibility insights
        compatibility_level = 'excellent' if compatibility_result['overall_compatibility'] > 0.8 else \
                            'good' if compatibility_result['overall_compatibility'] > 0.6 else \
                            'fair' if compatibility_result['overall_compatibility'] > 0.4 else 'poor'
        
        styling_confidence = 'high' if compatibility_result['styling_difficulty'] == 'easy' else \
                           'medium' if compatibility_result['styling_difficulty'] == 'medium' else 'low'
        
        insights = {
            'compatibility_level': compatibility_level,
            'styling_confidence': styling_confidence,
            'best_aspect': max([
                ('color', compatibility_result['color_compatibility']),
                ('style', compatibility_result['style_compatibility']),
                ('formality', compatibility_result['formality_compatibility'])
            ], key=lambda x: x[1])[0],
            'improvement_needed': min([
                ('color', compatibility_result['color_compatibility']),
                ('style', compatibility_result['style_compatibility']),
                ('formality', compatibility_result['formality_compatibility'])
            ], key=lambda x: x[1])[0] if compatibility_result['overall_compatibility'] < 0.7 else None
        }
        
        # Generate styling tips
        styling_tips = []
        if compatibility_result['overall_compatibility'] > 0.7:
            styling_tips.append("This combination works beautifully together!")
        elif compatibility_result['overall_compatibility'] > 0.5:
            styling_tips.append("Good combination with some styling considerations")
        else:
            styling_tips.append("Challenging combination - consider adding bridging pieces")
        
        if compatibility_result['color_compatibility'] < 0.5:
            styling_tips.append("Consider adding a neutral accessory to bridge the colors")
        
        if compatibility_result['styling_difficulty'] == 'advanced':
            styling_tips.append("This is an advanced styling combination - confidence is key!")
        
        return jsonify({
            'status': 'success',
            'message': 'Style compatibility analysis completed',
            'compatibility': compatibility_result,
            'insights': insights,
            'styling_tips': styling_tips,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Perfect style matching delivered!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Style compatibility analysis failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@advanced_ai_bp.route('/predictive-recommendations', methods=['POST'])
def get_predictive_recommendations():
    """
    Generate predictive AI recommendations
    "We girls have no time" - AI that predicts what you'll love!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        context = data.get('context', {})  # weather, season, upcoming events, etc.
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Generate predictive recommendations
        predictions = AdvancedAIEngine.generate_predictive_recommendations(user_id, context)
        
        if not predictions:
            return jsonify({
                'status': 'insufficient_data',
                'message': 'Not enough data for predictive recommendations',
                'recommendation': 'Continue using the app to build your style profile',
                'tagline': 'We girls have no time - But we need more data first!'
            }), 400
        
        # Analyze prediction patterns
        prediction_insights = {
            'total_predictions': len(predictions),
            'high_confidence_predictions': len([p for p in predictions if p['prediction_confidence'] > 0.7]),
            'trend_influenced': len([p for p in predictions if p['trend_influence'] > 0.5]),
            'style_influenced': len([p for p in predictions if p['personal_style_influence'] > 0.5]),
            'seasonal_influenced': len([p for p in predictions if p['seasonal_influence'] > 0.5]),
            'prediction_types': list(set(p['recommendation_type'] for p in predictions))
        }
        
        # Generate prediction summary
        summary = {
            'primary_influence': 'trends' if prediction_insights['trend_influenced'] > prediction_insights['style_influenced'] else 'personal_style',
            'confidence_level': 'high' if prediction_insights['high_confidence_predictions'] > len(predictions) / 2 else 'medium',
            'prediction_focus': prediction_insights['prediction_types'][0] if prediction_insights['prediction_types'] else 'general'
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Predictive recommendations generated successfully',
            'predictions': predictions,
            'insights': prediction_insights,
            'summary': summary,
            'context_used': context,
            'generation_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - AI predictions ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Predictive recommendations failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@advanced_ai_bp.route('/shopping-intelligence', methods=['POST'])
def get_shopping_intelligence():
    """
    Generate intelligent shopping recommendations
    "We girls have no time" - Smart shopping made simple!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        budget = data.get('budget', 500)  # Default budget
        shopping_goal = data.get('goal', 'general')  # general, work, casual, formal, seasonal
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get user wardrobe data
        user_data = get_user_data(user_id, auth_token)
        if not user_data:
            return jsonify({'error': 'Unable to fetch user data'}), 500
        
        wardrobe_data = user_data.get('wardrobe', [])
        
        # Get wardrobe optimization data
        optimization = WardrobeOptimization.query.filter_by(user_id=user_id).first()
        if not optimization:
            # Generate optimization if not exists
            optimization_result = AdvancedAIEngine.analyze_wardrobe_optimization(user_id, wardrobe_data)
            optimization = WardrobeOptimization.query.filter_by(user_id=user_id).first()
        
        # Get current trends
        current_trends = TrendForecast.get_current_trends(5)
        
        # Generate shopping recommendations
        shopping_recommendations = {
            'priority_items': [],
            'trend_items': [],
            'investment_pieces': [],
            'budget_allocation': {},
            'shopping_strategy': {}
        }
        
        # Priority items from wardrobe optimization
        if optimization and optimization.priority_purchases:
            priority_purchases = json.loads(optimization.priority_purchases)
            for item in priority_purchases[:5]:  # Top 5 priorities
                shopping_recommendations['priority_items'].append({
                    'item': item['item'],
                    'priority': item['priority'],
                    'reason': item['reason'],
                    'estimated_cost': item['estimated_cost'],
                    'wardrobe_impact': 'high' if item['priority'] == 'high' else 'medium'
                })
        
        # Trend-based recommendations
        for trend in current_trends[:3]:
            trend_data = trend.to_dict()
            if trend_data['confidence_score'] > 0.7:
                shopping_recommendations['trend_items'].append({
                    'trend_name': trend_data['trend_name'],
                    'category': trend_data['trend_category'],
                    'confidence': trend_data['confidence_score'],
                    'styling_tips': trend_data['styling_tips'][:2],  # Top 2 tips
                    'estimated_cost': '$50-200',  # Would be more specific in production
                    'trend_strength': trend_data['trend_strength']
                })
        
        # Investment pieces recommendations
        investment_pieces = [
            {'item': 'Quality blazer', 'reason': 'Versatile for work and casual', 'cost_range': '$150-400'},
            {'item': 'Classic handbag', 'reason': 'Daily essential with longevity', 'cost_range': '$200-600'},
            {'item': 'Well-fitted jeans', 'reason': 'Foundation piece for casual looks', 'cost_range': '$100-300'}
        ]
        shopping_recommendations['investment_pieces'] = investment_pieces
        
        # Budget allocation
        shopping_recommendations['budget_allocation'] = {
            'essentials': f"${int(budget * 0.4)}",
            'trends': f"${int(budget * 0.3)}",
            'investment_pieces': f"${int(budget * 0.3)}"
        }
        
        # Shopping strategy
        shopping_recommendations['shopping_strategy'] = {
            'approach': 'essentials_first' if optimization and optimization.completeness_score < 0.6 else 'balanced',
            'timing': 'immediate' if shopping_goal == 'urgent' else 'planned',
            'focus': shopping_goal,
            'key_advice': [
                'Prioritize versatile pieces that work with existing wardrobe',
                'Invest in quality for frequently worn items',
                'Consider cost-per-wear when making decisions'
            ]
        }
        
        # Generate shopping insights
        insights = {
            'wardrobe_readiness': optimization.completeness_score if optimization else 0.5,
            'shopping_urgency': 'high' if not optimization or optimization.completeness_score < 0.5 else 'medium',
            'trend_alignment': len(shopping_recommendations['trend_items']),
            'budget_efficiency': 'optimized' if budget > 300 else 'focused',
            'recommended_stores': ['Versatile retailers', 'Quality basics stores', 'Trend-forward boutiques']
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Shopping intelligence generated successfully',
            'recommendations': shopping_recommendations,
            'insights': insights,
            'budget': budget,
            'shopping_goal': shopping_goal,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Smart shopping made simple!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Shopping intelligence generation failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@advanced_ai_bp.route('/style-insights', methods=['GET'])
def get_advanced_style_insights():
    """
    Get advanced AI-powered style insights
    "We girls have no time" - Deep style intelligence revealed!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get comprehensive user data
        user_data = get_user_data(user_id, auth_token)
        if not user_data:
            return jsonify({'error': 'Unable to fetch user data'}), 500
        
        # Get wardrobe optimization
        optimization = WardrobeOptimization.query.filter_by(user_id=user_id).first()
        
        # Get recent predictions
        recent_predictions = PredictiveRecommendation.query.filter_by(
            user_id=user_id, status='active'
        ).order_by(PredictiveRecommendation.created_date.desc()).limit(5).all()
        
        # Get current trends
        current_trends = TrendForecast.get_current_trends(3)
        
        # Generate advanced insights
        advanced_insights = {
            'style_maturity': {
                'level': 'developing' if not optimization or optimization.style_coherence_score < 0.5 else 
                        'established' if optimization.style_coherence_score < 0.8 else 'sophisticated',
                'coherence_score': optimization.style_coherence_score if optimization else 0.3,
                'areas_for_growth': []
            },
            'wardrobe_intelligence': {
                'efficiency_rating': optimization.efficiency_score if optimization else 0.4,
                'versatility_rating': optimization.versatility_score if optimization else 0.4,
                'optimization_potential': 'high' if not optimization or optimization.completeness_score < 0.6 else 'medium',
                'smart_gaps': optimization.missing_essentials if optimization else []
            },
            'trend_alignment': {
                'trend_awareness': len(recent_predictions) / 5.0,  # Normalize to 0-1
                'trend_adoption_style': 'early_adopter' if len(recent_predictions) > 3 else 'selective',
                'compatible_trends': [trend.trend_name for trend in current_trends[:2]],
                'trend_confidence': sum(trend.confidence_score for trend in current_trends) / len(current_trends) if current_trends else 0
            },
            'predictive_profile': {
                'prediction_accuracy': 0.75,  # Would be calculated from historical data
                'style_predictability': 'high' if len(recent_predictions) > 2 else 'medium',
                'recommendation_receptivity': 'open' if len(recent_predictions) > 1 else 'selective',
                'future_style_direction': 'evolving' if len(recent_predictions) > 3 else 'stable'
            }
        }
        
        # Generate growth recommendations
        if optimization:
            if optimization.style_coherence_score < 0.6:
                advanced_insights['style_maturity']['areas_for_growth'].append('Develop signature style elements')
            if optimization.versatility_score < 0.6:
                advanced_insights['style_maturity']['areas_for_growth'].append('Build more versatile wardrobe foundation')
            if optimization.efficiency_score < 0.6:
                advanced_insights['style_maturity']['areas_for_growth'].append('Focus on cost-per-wear optimization')
        
        # Generate style intelligence summary
        intelligence_summary = {
            'overall_style_iq': (
                advanced_insights['style_maturity']['coherence_score'] +
                advanced_insights['wardrobe_intelligence']['efficiency_rating'] +
                advanced_insights['trend_alignment']['trend_awareness']
            ) / 3,
            'strongest_area': max([
                ('style_maturity', advanced_insights['style_maturity']['coherence_score']),
                ('wardrobe_efficiency', advanced_insights['wardrobe_intelligence']['efficiency_rating']),
                ('trend_awareness', advanced_insights['trend_alignment']['trend_awareness'])
            ], key=lambda x: x[1])[0],
            'growth_opportunity': min([
                ('style_maturity', advanced_insights['style_maturity']['coherence_score']),
                ('wardrobe_efficiency', advanced_insights['wardrobe_intelligence']['efficiency_rating']),
                ('trend_awareness', advanced_insights['trend_alignment']['trend_awareness'])
            ], key=lambda x: x[1])[0],
            'style_archetype': 'Style Explorer' if advanced_insights['trend_alignment']['trend_awareness'] > 0.7 else
                             'Classic Curator' if advanced_insights['style_maturity']['coherence_score'] > 0.7 else
                             'Emerging Stylist'
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Advanced style insights generated successfully',
            'advanced_insights': advanced_insights,
            'intelligence_summary': intelligence_summary,
            'analysis_depth': 'comprehensive',
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Deep style intelligence revealed!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Advanced style insights generation failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

